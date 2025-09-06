import sys
import json

def find_blocks(node, tags):
    found = []
    if node.get("tag") in tags and node.get("text"):
        found.append(node["text"])
    for child in node.get("children", []):
        found.extend(find_blocks(child, tags))
    return found

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python analyze_dom_json.py estructura.json pre code ...")
        sys.exit(1)
    with open(sys.argv[1], encoding='utf-8') as f:
        dom_json = json.load(f)
    tags = sys.argv[2:]
    blocks = find_blocks(dom_json, tags)
    for i, block in enumerate(blocks, 1):
        print(f"\n--- Bloque {i} ({', '.join(tags)}): ---\n{block}\n")