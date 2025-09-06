import json
import sqlite3
from datetime import datetime


def process_json_to_db(json_file, db_name):
    try:
        # Connect to SQLite database (or create it)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Create table
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregunta TEXT,
            respuesta TEXT,
            datetime TEXT
        )"""
        )

        # Load JSON data
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Debug: print the total number of entries
        print(f"Total entries to process: {len(data)}")

        # Iterate over each conversation entry
        insert_count = 0  # Counter for insertions
        for entry in data:
            print(
                f"Procesando entrada: {entry['title'][:50]}..."
            )  # Solo mostramos los primeros 50 caracteres del título
            mapping = entry.get("mapping", {})

            pregunta = None

            for message_id, message_data in mapping.items():
                message = message_data.get("message", {})

                # Debug: Print the whole message to see why it's None or malformed
                if message is None:
                    print(
                        f"Warning: Message with ID {message_id} is None or malformed. Message data: {message_data}"
                    )
                    continue

                author_role = message.get("author", {}).get("role", "")
                content_parts = message.get("content", {}).get("parts", [])

                # Debug: Print the content to see its structure
                if not content_parts:
                    print(
                        f"Warning: Message with ID {message_id} has no content. Message: {message}"
                    )
                    continue

                # Now also allow "assistant" as a valid role
                if author_role not in ["user", "ChatGPT", "assistant"]:
                    print(
                        f"Warning: Message with ID {message_id} has an invalid author. Author: {author_role}"
                    )
                    continue

                content = content_parts[0]
                content_preview = content[  # noqa: F841
                    :100
                ]  # Mostrar solo los primeros 100 caracteres

                if author_role == "user":
                    pregunta = content
                    continue

                if author_role in ["ChatGPT", "assistant"] and pregunta:
                    respuesta = content

                    if pregunta and respuesta:
                        # Usar UTF-8 sin 'unicode_escape'
                        pregunta = pregunta.encode("utf-8", "ignore").decode("utf-8")
                        respuesta = respuesta.encode("utf-8", "ignore").decode("utf-8")

                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        print(
                            f"Insertando Pregunta: {pregunta[:50]}..."
                        )  # Muestra solo una parte de la pregunta
                        print(
                            f"Insertando Respuesta: {respuesta[:50]}..."
                        )  # Muestra solo una parte de la respuesta

                        cursor.execute(
                            """INSERT INTO conversations (pregunta, respuesta, datetime)
                            VALUES (?, ?, ?)""",
                            (pregunta, respuesta, timestamp),
                        )
                        conn.commit()

                        insert_count += 1

        print(f"Total de datos insertados: {insert_count}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()
        print(f"Data from {json_file} has been processed.")


# Example usage
json_file = "conversations.json"  # Replace with your JSON file name
db_name = "conversations.db"
process_json_to_db(json_file, db_name)
