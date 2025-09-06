import ollama
import datetime
import os

# Configuración del modelo
# MODEL_NAME = 'deepseek-coder:6.7b'  # Cambiá por 'terminator-ang' si ya lo tenés cargado
MODEL_NAME = 'deepseek-coder:latest'  # Cambiá por 'terminator-ang' si ya lo tenés cargado

# Pregunta resonante
prompt = '¿Cuál es el protocolo de resonancia en CAMBALACHE?'

# Invocación del modelo
response = ollama.chat(model=MODEL_NAME, messages=[
    {'role': 'user', 'content': prompt}
])

# Extraer contenido
content = response['message']['content']

# Documentar como evento resonante
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'resonance_event_{timestamp}.atm'

# Ritualizar guardado
with open(filename, 'w', encoding='utf-8') as f:
    f.write(f'# Evento de Resonancia\n')
    f.write(f'Modelo: {MODEL_NAME}\n')
    f.write(f'Fecha: {timestamp}\n')
    f.write(f'Prompt: {prompt}\n\n')
    f.write(f'Respuesta:\n{content}\n')

print(f'Evento documentado en: {filename}')
