# lianbot_gpt.py
import os
from flask import Flask, render_template_string, request, jsonify
import openai

app = Flask(__name__)

# Configuración de la API de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")  # Debes exportar esta variable en tu entorno

html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>LianBot GPT Interface</title>
<style>
  body { background: #111; color: #0f0; font-family: monospace; }
  #chat { height: 400px; overflow-y: auto; border: 1px solid #0f0; padding: 10px; }
  input { width: 100%; padding: 10px; background: #000; color: #0f0; border: 1px solid #0f0; }
  #lang { margin-bottom: 10px; }
</style>
</head>
<body>
<h1>LianBot GPT Multilingual</h1>
<label for="lang">Choose language:</label>
<select id="lang">
  <option value="es" selected>Español</option>
  <option value="en">English</option>
</select>
<div id="chat"></div>
<input id="input" autocomplete="off" placeholder="Type here..." />
<script>
const chat = document.getElementById('chat');
const input = document.getElementById('input');
const lang = document.getElementById('lang');

input.addEventListener('keydown', e => {
  if(e.key === 'Enter' && input.value.trim()) {
    const msg = input.value.trim();
    chat.innerHTML += `<p><b>You:</b> ${msg}</p>`;
    fetch('/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: msg, language: lang.value})
    }).then(res => res.json()).then(data => {
      chat.innerHTML += `<p><b>LianBot:</b> ${data.response}</p>`;
      chat.scrollTop = chat.scrollHeight;
    });
    input.value = '';
  }
});
</script>
</body>
</html>
"""

def generate_gpt_response(prompt: str, language: str) -> str:
    system_prompt = {
        "es": "Eres LianBot, una IA avanzada que responde en español con precisión técnica y empatía.",
        "en": "You are LianBot, an advanced AI that responds in English with technical precision and empathy."
    }
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt.get(language, system_prompt["en"])},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error accessing GPT API: {e}"

@app.route("/")
def index():
    return render_template_string(html)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    language = data.get("language", "es")
    response = generate_gpt_response(user_msg, language)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
