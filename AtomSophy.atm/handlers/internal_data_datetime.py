# 👻👻👻👻👻👻👻👻👻😎😎😎😎😎😎😎😎😎
# internal_data_datetime

#import json
#import sqlite3
#import hashlib
#import re
#from datetime import datetime
#from pathlib import Path

# Hashtags base iniciales
che_hashtags = (
    ["Hermes", "Alian", "Copilot", "#IA", "#AI", "Resonancia", ".atm", "CAMBALACHE", "AtomSophy", "RNN"],
    ["CAMBALACHE-Resonance"]
)

hashtags_planos = [tag for grupo in che_hashtags for tag in grupo]

def generar_sha512(texto):
    return hashlib.sha512(texto.encode('utf-8')).hexdigest()

def buscar_hashtags(pregunta, respuesta):
    matched_tags = []
    for tag in hashtags_planos:
        if re.search(rf"\b{re.escape(tag)}\b", pregunta, re.IGNORECASE) or \
           re.search(rf"\b{re.escape(tag)}\b", respuesta, re.IGNORECASE):
            matched_tags.append(tag)
    return ", ".join(matched_tags) if matched_tags else None

def process_json_to_db(json_file, db_name):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT,
                des1 TEXT,
                des2 TEXT,
                mem1 TEXT,
                hashtag TEXT,
                pregunta TEXT,
                respuesta TEXT,
                ia TEXT,
                hash_sha512 TEXT UNIQUE,
                datetime TEXT
            )
        ''')

        with open(json_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"[ERROR] No se pudo leer {json_file}: {e}")
                return 0

        insert_count = 0
        for entry in data:
            mapping = entry.get("mapping", {})
            pregunta = None

            for message_id, message_data in mapping.items():
                message = message_data.get("message", {})
                if not message:
                    continue

                author_role = message.get("author", {}).get("role", "")
                content_parts = message.get("content", {}).get("parts", [])
                if not content_parts:
                    continue

                content = content_parts[0]

                if author_role == "user":
                    pregunta = content
                    continue

                if author_role in ["ChatGPT", "assistant"] and pregunta:
                    respuesta = content
                    pregunta = pregunta.encode('utf-8', 'ignore').decode('utf-8')
                    respuesta = respuesta.encode('utf-8', 'ignore').decode('utf-8')

                    hashtag = buscar_hashtags(pregunta, respuesta)
                    hash_sha512 = generar_sha512(pregunta + respuesta)

                    usuario = "CHE"
                    ia = "ChatGPT"
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    try:
                        cursor.execute('''
                            INSERT INTO conversations (usuario, des1, des2, mem1, hashtag, pregunta, respuesta, ia, hash_sha512, datetime)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (usuario, None, None, None, hashtag, pregunta, respuesta, ia, hash_sha512, timestamp))
                        conn.commit()
                        insert_count += 1
                    except sqlite3.IntegrityError:
                        # Ya existe este hash -> duplicado evitado
                        pass

        return insert_count

    except Exception as e:
        print(f"[ERROR] {e}")
        return 0
    finally:
        if 'conn' in locals():
            conn.close()

def procesar_todo(base_folder, db_name):
    base_path = Path(base_folder)
    total_insertados = 0

    for json_file in base_path.rglob("conver*.json"):
        insertados = process_json_to_db(json_file, db_name)
        if insertados > 0:
            print(f"[OK] {json_file} → {insertados} registros insertados.")
            total_insertados += insertados
        else:
            print(f"[SKIP] {json_file} (sin datos nuevos)")

    print(f"✅ Total de nuevos registros: {total_insertados}")


def internal_data_datetime(parameters=" "):
    print("Procesar todo")
    procesar_todo(r"d:\ia\chat_ia", r"h:\conversations.db")
    
    
# Ejecución masiva
#procesar_todo(r"d:\ia\chat_ia", r"h:\conversations.db")
#
