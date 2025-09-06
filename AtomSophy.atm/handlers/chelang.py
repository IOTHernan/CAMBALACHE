# ▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░
# funciones lenguaje
# ▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░ 

def detect_language_and_set_voice(engine, text):
	"""
	Detecta el idioma del texto y establece la voz correspondiente.
	:param engine: Instancia del motor pyttsx3.
	:param text: Texto del cual se detectará el idioma.
	:return: True si se pudo establecer la voz, False en caso contrario.
	"""
	try:
		language = detect(text)
		voices = engine.getProperty('voices')
		# mapear idiomas detectados
		lang_to_voice = {
			'en': 'english',
			'es': 'spanish',
			'fr': 'french',
		}
		# Buscar una voz que coincida con el idioma detectado
		for voice in voices:
			if lang_to_voice.get(language) in voice.name.lower():
				print(f"Idioma detectado: {language}")
				engine.setProperty('voice', voice.id)
				return True

		# Si no se encuentra, usar el idioma predeterminado
		messagebox.showinfo("Idioma no soportado",f"No se encontro voz: {language}")
		return False

	except LangDetectException:
		messagebox.showerror("Error", f"No se pudo detectar el idioma")  # noqa: F541
		return False



def read_text_by_language(text):
	"""
	Lee el texto
	"""
	try:
		engine = pyttsx3.init()
		engine.setProperty('rate', 150)
		engine.setProperty('volume', 0.9)

		lines = text.splitlines() # Dividir el texto por lineas
		for line in lines:
			words = line.split()
			for word in words:
				if detect_language_and_set_voice(engine, word):
					engine.say(word)
				else:
					messagebox.showinfo("Advertencia",f"No se pudo")  # noqa: F541

		engine.runAndWait()
	except Exception as e:
		messagebox.showerror("Error", f"No se pudo leer el texto: {e}")



def read_file_aloud(file_path):
	"""
	Lee el contenido de un archivo y lo reproduce en voz alta.

	:param file_path: Ruta al archivo que se desea leer.
	"""
	try:
		# Abrir y leer el archivo
		with open(file_path, 'r', encoding='utf-8') as file:
			content = file.read()
		read_text_by_language(content)
	except Exception as e:
		messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")


