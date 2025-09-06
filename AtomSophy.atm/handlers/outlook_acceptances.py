import imaplib
import email
import re
import json
import logging
import os

# Configuración - ajustá con tus datos reales
IMAP_SERVER = 'outlook.office365.com'
EMAIL_ACCOUNT = 'tu_email@dominio.com'
PASSWORD = 'tu_password_o_token'
MAILBOX = 'INBOX'
SEARCH_CRITERIA = '(SUBJECT "confirmó como amigo")'

OUTPUT_FILE = 'acceptances.json'
LOG_FILE = 'acceptances.log'

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
        return email_ids
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

def extract_urls(text):
    return re.findall(r'https?://[^\s]+', text)

def parse_email(msg):
    try:
        subject = msg['subject']
        from_ = msg['from']
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_payload(decode=True).decode(errors='ignore')
        else:
            body = msg.get_payload(decode=True).decode(errors='ignore')
        urls = extract_urls(body)
        return {
            'subject': subject,
            'from': from_,
            'urls': urls
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
    existing.extend(data)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)
    logging.info(f"Guardados {len(data)} registros en {OUTPUT_FILE}")

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
            if parsed:
                results.append(parsed)

    if results:
        save_results(results)
    else:
        logging.info("No se encontraron emails para guardar.")

    try:
        mail.logout()
        logging.info("Desconectado del servidor IMAP.")
    except:
        pass

if __name__ == '__main__':
    main()
