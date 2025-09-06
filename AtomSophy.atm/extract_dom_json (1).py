import sys
import json
from bs4 import BeautifulSoup

def element_to_json(element):
    if not hasattr(element, 'name') or element.name is None:
        return None
    return {
        "tag": element.name,
        "attrs": dict(element.attrs),
        "children": [e for e in (element_to_json(child) for child in element.children) if e],
        "text": element.string.strip() if element.string and element.string.strip() else ""
    }

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python extract_dom_json.py archivo.html salida.json")
        sys.exit(1)
    with open(sys.argv[1], encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    body = soup.body or soup
    dom_json = element_to_json(body)
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        json.dump(dom_json, f, ensure_ascii=False, indent=2)
    print(f"Estructura JSON extraída a {sys.argv[2]}")