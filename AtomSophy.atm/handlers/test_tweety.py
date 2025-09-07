
import os
import google.genai as genai
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env para desarrollo local.
# Asegúrate de tener python-dotenv instalado: pip install python-dotenv
load_dotenv()

# Carga la clave de API desde una variable de entorno para mayor seguridad.
# Crea un archivo .env en la raíz de tu proyecto con: GEMINI_API_KEY="TU_CLAVE_DE_API"
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("No se encontró la variable de entorno GEMINI_API_KEY. Por favor, configúrala.")

genai.configure(api_key=api_key)

# El modelo 'gemini-2.5-flash' no parece ser un modelo válido actualmente. Usamos 'gemini-1.5-flash'.
model = genai.GenerativeModel('gemini-1.5-flash')

response = model.generate_content("Explica cómo funciona la inteligencia artificial en pocas palabras")

print(response.text)
