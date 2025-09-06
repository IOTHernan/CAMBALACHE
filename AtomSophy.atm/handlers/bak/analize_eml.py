import re
import quopri
import requests
from datetime import datetime

HISTORY_FILE = 'history.txt'

def decode_quoted_printable(text):
    return quopri.decodestring(text).decode('utf-8', errors='ignore')

def extract_urls(text):
    url_pattern = re.compile(r'https?://[^\s<>"\'=]+')
    return url_pattern.findall(text)

def load_history():
    try:
        with open(HISTORY_FILE, 'r') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_new_urls(urls):
    existing = load_history()
    new_urls = [url for url in urls if url not in existing]
    if new_urls:
        with open(HISTORY_FILE, 'a') as f:
            for url in new_urls:
                f.write(url + '\n')
    return new_urls

def check_url_active(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def analize_eml(file):
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        raw_email = f.read()
    
    decoded = decode_quoted_printable(raw_email)
    urls = extract_urls(decoded)
    new_urls = save_new_urls(urls)
    timestamp = datetime.now().isoformat()
    
    resumen = {
        'timestamp': timestamp,
        'total_urls_found': len(urls),
        'new_urls': new_urls,
        'url_status': {}
    }
    
    for url in new_urls:
        active = check_url_active(url)
        resumen['url_status'][url] = 'ACTIVA' if active else 'INACTIVA'
    
    return resumen
    pass


if __name__ == "__main__":
    archivo = 'sample_email.eml'
    resultado = analize_eml(archivo)
    print(f"Análisis realizado en: {resultado['timestamp']}")
    print(f"Total URLs encontradas: {resultado['total_urls_found']}")
    print(f"Nuevas URLs guardadas: {len(resultado['new_urls'])}")
    for url, status in resultado['url_status'].items():
        print(f"{url} --> {status}")
