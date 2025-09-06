import imaplib
import email
import re
import json
import logging
import os
from bs4 import BeautifulSoup

# Configuración
IMAP_SERVER = 'outlook.office365.com'
EMAIL_ACCOUNT = 'tu_email@dominio.com'
PASSWORD = 'tu_password_o_token'
MAILBOX = 'INBOX'
SEARCH_CRITERIA = '(SUBJECT "confirmó como amigo")'
OUTPUT_FILE = 'acceptances.json'
LOG_FILE = 'acceptances.log'
MAX_EMAILS = 10  # límite para ahorrar datos

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(LOG_FILE),
                        logging.StreamHandler()])

def connect_mail():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, PASSWORD)
        mail.select(MAILBOX)
        logging.info("Conectado a IMAP.")
        return mail
    except Exception as e:
        logging.error(f"Error conexión IMAP: {e}")
        return None

def search_emails(mail):
    try:
        result, data = mail.search(None, SEARCH_CRITERIA)
        if result != 'OK':
            logging.error("Error en búsqueda de emails.")
            return []
        email_ids = data[0].split()
        logging.info(f"Encontrados {len(email_ids)} emails que coinciden.")
        return email_ids[:MAX_EMAILS]
    except Exception as e:
        logging.error(f"Error en search_emails: {e}")
        return []

def fetch_email(mail, eid):
    try:
        result, msg_data = mail.fetch(eid, '(RFC822)')
        if result != 'OK':
            logging.error(f"Error al obtener email {eid}")
            return None
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        return msg
    except Exception as e:
        logging.error(f"Error en fetch_email {eid}: {e}")
        return None

def extract_urls_from_text(text):
    return re.findall(r'https?://[^\s\'\"<>]+', text)

def extract_urls_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
#        if href.startswith('http'):
        if isinstance(href, str) and href.startswith('http'):

            urls.add(href)
    return list(urls)

def parse_email(msg):
    try:
        subject = msg['subject']
        from_ = msg['from']
        urls = set()
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                try:
                    payload = part.get_payload(decode=True)
                    if not payload:
                        continue
                    charset = part.get_content_charset() or 'utf-8'
                    text = payload.decode(charset, errors='ignore')
                except:
                    continue

                if content_type == "text/plain":
                    urls.update(extract_urls_from_text(text))
                elif content_type == "text/html":
                    urls.update(extract_urls_from_html(text))
        else:
            content_type = msg.get_content_type()
            payload = msg.get_payload(decode=True)
            charset = msg.get_content_charset() or 'utf-8'
            text = payload.decode(charset, errors='ignore')
            if content_type == "text/plain":
                urls.update(extract_urls_from_text(text))
            elif content_type == "text/html":
                urls.update(extract_urls_from_html(text))

        return {
            'subject': subject,
            'from': from_,
            'urls': list(urls)
        }
    except Exception as e:
        logging.error(f"Error parseando email: {e}")
        return None

def save_results(data):
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            existing = json.load(f)
    else:
        existing = []
    # Evitar duplicados en guardado
    existing_urls = {url for entry in existing for url in entry.get('urls', [])}
    new_entries = []
    for entry in data:
        if not any(url in existing_urls for url in entry.get('urls', [])):
            new_entries.append(entry)
    existing.extend(new_entries)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)
    logging.info(f"Guardados {len(new_entries)} registros nuevos en {OUTPUT_FILE}")

def main():
    mail = connect_mail()
    if not mail:
        return

    email_ids = search_emails(mail)
    results = []

    for eid in email_ids:
        msg = fetch_email(mail, eid)
        if msg:
            parsed = parse_email(msg)
            if parsed and parsed.get('urls'):
                results.append(parsed)

    if results:
        save_results(results)
    else:
        logging.info("No se encontraron emails con URLs para guardar.")

    try:
        mail.logout()
        logging.info("Desconectado del servidor IMAP.")
    except:
        pass

if __name__ == '__main__':
    main()
