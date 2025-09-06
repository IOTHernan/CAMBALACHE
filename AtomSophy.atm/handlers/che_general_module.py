#import sys
#import pygame
#from markdown import Markdown
# Configuración inicial de Pygame
#pygame.init()
#ventana = None
#ARK= None

import pyttsx3

def speak_text(text="Error. Falta el texto"):
    """
    Función para sintetizar y reproducir voz a partir de texto.
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()



# @memory_monitor
def translate_text(text, src='en', dest='es'):
    """
    Traduce un texto.
    :param text:
    :param src:
    :param dest:
    :return:
    """
    translator2 = Translator()
#    return translator2.translate(text1, src=src, dest=dest).text1
    return translator2.translate(text, src=src, dest=dest)


# def translate_text_gcp(text, target='es'):
#     """Función para traducir texto usando Google Cloud Translate."""
#     client = translate.Client()
#     result = client.translate(text, target_language=target)
#     return result['translatedText']


def read_file_to_speaker(file_path):
    """
    Read text file to Speaker
    :param file_path:
    :return:
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            speak_text(file.read())

    except FileNotFoundError:
        print(f"El archivo {file_path} no fue encontrado.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return None

         

def che_author():
    print("CHEHEC")
    
# Configuración inicial de Pygame
#pygame.init()
#ventana = None
#ARK= None

def configura_ventana(tamao):
    global ventana, ARK
    ventana = pygame.display.set_mode(tamao)
    pygame.display.set_caption("Markov Editor")
    ARK = pygame.key.get_pressed()

# ---------------------------------------------------------------------------------

def maneja(evento):
    global ARK
    if evento.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif evento.type == pygame.KEYDOWN:
        ARK.add(evento.key)

# -----------------------------------------------------------------------------------------

def muestra_archivo_marked(fuente, fuente_de_lectura, fuente_extrapolado):
    try:
        with open(fuente_de_lectura, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()

        # Convertir el contenido en formato Markdown
        convertidor = Markdown()
        texto_limpio = convertidor.convertir(contenido)

        pygame.init()
        configura_ventana((ancho, alto))
        pantalla = pygame.display.set_mode( (ancho, alto) )

        fuente = pygame.font.Font(None, 20)
        fuente_extrapolado = pygame.font.Font(None, 16)

        texto = fuente_de_lectura + "\n" + texto_limpio
        surface = fuente_de_lectura + fuente_extrapolado + texto

        while True:
            pygame.time.Clock().tick(60)
            pantalla.blit(surface, (0, 0))
            pygame.display.flip()

    except Exception as e:
        print("Error:", str(e))

# ----------------------------------------------------------

#def chemarkmain():
#    ancho = 800
#    alto = 600
#
#    # Busqueda de archivos
#    def busqueda_archivos():
#        pygame.init()
#        configura_ventana((ancho, alto))
#        pantalla = pygame.display.set_mode( (ancho, alto) )
#
#        # Variable para almacenar los resultados
#        resultados = []
#
#        # Ruta para buscar los archivos
#        rutaBuscar = "C:/"  # Asegurarse de que la ruta sea correcta
#
#        while True:
#            for event in pygame.event.get():
#                if event.type == pygame.QUIT:
#                    pygame.quit()
#                    sys.exit()
#                elif event.type == pygame.MOUSEBUTTONDOWN:
#                    busqueda_archivos.estado = not busqueda_archivos.estado
#                    break
#
#            pantalla.fill((0, 0, 0))
#
#            # Verificar si el botón está activo
#            if busqueda_archivos.estado:
#                texto_busqueda = "Buscar archivo .md..."
#                fuente_busqueda = pygame.font.Font(None, 24)
#                surface_busqueda = pygame.draw.rect(pantalla, (255, 0, 0), [ancho//2 - 100, alto - 300, 200, 300])
#                pantalla.blit(fuente_busqueda.render(texto_buspta...), (ancho//2 - 90, alto - 250))
#
#            pygame.display.flip()
#
#    # Principal de la aplicación
#    pygame.init()
#    configura_ventana((ancho, alto))
#    pantalla = pygame.display.set_mode( (ancho, alto) )
#
#    state = False
#
#    while True:
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                pygame.quit()
#                sys.exit()
#            elif event.type == pygame.KEYDOWN:
#                if event.key == pygame.K_SPACE:
#                    state = not state
#
#        pantalla.fill((0, 0, 0))
#
#        if state:
#            # Mostrar ventana de busqueda
#            busqueda_archivos.estado = True
#            pantalla.blit(busqueda_archivos surface, (0, 0), (0, 0, ancho, alto))
#        else:
#            # Mostrar ventana principal
#            surface = pygame.Surface( (ancho, alto) )
#            surface.fill( (255, 255, 255) )
#
#            fuente = pygame.font.Font(None, 48)
#            fuente_extrapolado = pygame.font.Font(None, 36)
#
#            texto = "Welcome to Markov Editor"
#            surface.blit(fuente.render(texto, True, (0, 0, 0)), (ancho//2 - 150, alto//2 - 75))
#
#            botón_buscar = pygame.Rect( ancho//2 - 100, alto - 300, 200, 300 )
#            pygame.draw.rect(surface, (255, 0, 0), botón_buscar)
#            pygame.draw.rect(surface, (0, 255, 0), botón_buscar, 5)
#
#            pygame.display.flip()
#
        # Manejar FPS
#        pygame.time.Clock().tick(60)

#import pygame
from functools import partial

def chemarkmain():
    ancho = 800
    alto = 600

    class BusquedaArchivos:
        def __init__(self):
            self.estado = False
            self.surface = None

        @property
        def get_surface(self):
            if not self.estado:
                self.surface = pygame.Surface((ancho, alto))
                self.surface.fill((255, 0, 0))
                return self.surface
            else:
                self.surface = pygame.Surface((ancho, alto))
                self.surface.fill((0, 255, 0))
                return self.surface

    def configura_ventanaDimensiones():
        pygame.init()
        pantalla = pygame.display.set_mode( (ancho, alto) )
        pygame.display.set_caption("Markov Editor")
        return pantalla

    pantalla = configura_ventanaDimensiones()

    state = False
#    surface 
    Principal = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state = not state

        current_surface = BusquedaArchivos().get_surface if state else None
        Principal = current_surface()

        pygame.display.flip()

    pygame.quit()


### **Script Python para HTML**
def generar_html(d,outf):
    
	#import os
	#from datetime import datetime
	# Ruta al archivo y disco
	#directorio = d.split(d)
    #	archivo_salida = 'outf'
    directorio = "h:/atomsophy/data"
    archivo_salida = 'h:/atomsophy/data/html/tabla_archivos.html'

    # Generar lista de archivos
    archivos = []
    for root, dirs, files in os.walk(directorio):
        for file in files:
            ruta_completa = os.path.join(root, file)
        tamaño = os.path.getsize(ruta_completa)  # Tamaño en bytes
        fecha_mod = datetime.fromtimestamp(os.path.getmtime(ruta_completa)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        archivos.append((ruta_completa, tamaño, fecha_mod))

	# Crear tabla HTML
    html = """
	<!DOCTYPE html>
	<html lang="es">
	<head>
        <meta charset="UTF-8">
        <title>Lista de Archivos</title>
        <style>
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid black; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
        </style>
	</head>
	<body>
        <h1>Lista de Archivos</h1>
        <table>
            <tr>
                <th>Archivo</th>
                <th>Tamaño (bytes)</th>
                <th>Última Modificación</th>
            </tr>
	"""

    for ruta, tamaño, fecha in archivos:
        html += f"<tr><td>{ruta}</td><td>{tamaño}</td><td>{fecha}</td></tr>\n"

    html += """
        </table>
    </body>
    </html>
    """

    # Guardar el archivo HTML
    with open(archivo_salida, "w", encoding="utf-8") as file:
        file.write(html)

        print(f"Tabla generada: {archivo_salida}")


# Voces 
def voces():
#from TTS.api import TTS

    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

    # Para femenino
    tts.tts_to_file(text="Hello, this is a female voice.", file_path="female.wav")

    # Para masculino (usando otro modelo)
    tts_male = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False, gpu=False)
    tts_male.tts_to_file(text="Hello, this is a male voice.", file_path="male.wav")
    
    
def speak2(self, texto: str, voz: str = "femenina", idioma: str = "es"):
    key = f"{idioma}_{voz}"
    if key not in self.tts_instances:
        print(f"[Warn] Voz '{voz}' con idioma '{idioma}' no disponible. Usando voz por defecto.")
        key = f"{idioma}_femenina"
    tts = self.tts_instances[key]
    filename = "temp_output.wav"
    tts.tts_to_file(text=texto, file_path=filename)
    os.system(f"aplay {filename}")  # Linux; cambia según SO

# Ejemplo de uso:
#if __name__ == "__main__":
def test_speak():
    sp = SpeakEngine()
    sp.speak2("Hola, soy una voz femenina.", voz="femenina", idioma="es")
    sp.speak2("Hola, soy una voz masculina.", voz="masculina", idioma="es")


def pdf_a_txt_limited(pdf_path: str, txt_path: str, line_width: int = 80):
    """
    Extrae texto de un PDF y lo guarda en un archivo TXT,
    limitando cada línea a un ancho máximo (por defecto 80 caracteres).
    """
    reader = PdfReader(pdf_path)
    with open(txt_path, "w", encoding="utf-8") as f:
        for page in reader.pages:
            text = page.extract_text() or ""
            # Dividir texto en párrafos y luego en líneas con límite
            paragraphs = text.split("\n")
            for para in paragraphs:
                wrapped_lines = textwrap.wrap(para, width=line_width)
                for line in wrapped_lines:
                    f.write(line + "\n")
            f.write("\n")  # línea en blanco entre páginas


def pdf_a_txt_limpio(pdf_path: str, txt_path: str, line_width: int = 80):
    reader = PdfReader(pdf_path)
    with open(txt_path, "w", encoding="utf-8") as f:
        for page in reader.pages:
            raw_text = page.extract_text() or ""
            # Limpiar múltiples espacios y tabs
            cleaned = re.sub(r"\s+", " ", raw_text).strip()
            paragraphs = cleaned.split(". ")  # Dividir en oraciones
            for para in paragraphs:
                wrapped_lines = textwrap.wrap(para, width=line_width)
                for line in wrapped_lines:
                    f.write(line + "\n")
            f.write("\n")


# def pdf_a_txt_limited(pdf_path: str, line_width: int = 80) -> str:  # noqa: F811
#     """
#     Extrae texto del PDF y devuelve un string con líneas limitadas a line_width.
#     """
#     reader = PdfReader(pdf_path)
#     texto_completo = []
#     for page in reader.pages:
#         raw_text = page.extract_text() or ""
#         cleaned = re.sub(r"\s+", " ", raw_text).strip()
#         paragraphs = cleaned.split(". ")
#         for para in paragraphs:
#             wrapped_lines = textwrap.wrap(para, width=line_width)
#             texto_completo.extend(wrapped_lines)
#         texto_completo.append("")  # línea en blanco entre páginas
#     return "\n".join(texto_completo)


def traducir_y_guardar(texto_ingles: str, archivo_salida: str):
    traductor = TraductorOffline()
    lineas = texto_ingles.split("\n")
    traducido_total = []
    for linea in lineas:
        if linea.strip():
            traducido = traductor.traducir(linea)
            traducido_total.append(traducido)
        else:
            traducido_total.append("")
    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write("\n".join(traducido_total))


def getfile(filetypes=(("VDI files", "*.vdi"), ("All files", "*.*"))):
    """
    Selecciona un archivo mediante un cuadro de diálogo.
    Devuelve la ruta del archivo seleccionado o -1 si se cancela.
    """
    Tk().withdraw()  # Ocultar la ventana principal de Tkinter
    file_path = filedialog.askopenfilename(filetypes=filetypes)
    return file_path if file_path else -1


# def mount_vdi(vdi_path: str, drive_letter: str = "Z"):  # noqa: F811
#     """
#     Convierte un archivo VDI a formato RAW y lo monta como una unidad.
#     """
#     if not os.path.isfile(vdi_path):
#         print(f"[Error] El archivo {vdi_path} no existe.")
#         return False

#     # Ruta al archivo RAW convertido
#     raw_path = vdi_path.replace(".vdi", ".raw")

#     # Paso 1: Convertir VDI a RAW
#     print(f"[*] Convirtiendo {vdi_path} a {raw_path}...")
#     convert_cmd = ["VBoxManage", "clonehd", vdi_path, raw_path, "--format", "RAW"]
#     try:
#         subprocess.run(convert_cmd, check=True, capture_output=True, text=True)
#         print(f"[*] Conversión exitosa: {raw_path}")
#     except subprocess.CalledProcessError as e:
#         print(f"[Error] Falló la conversión del VDI: {e.stderr}")
#         return False

#     # Paso 2: Montar RAW usando PowerShell
#     print(f"[*] Montando {raw_path} en la unidad {drive_letter}...")
#     mount_cmd = f"""
#     PowerShell -Command "
#     Mount-DiskImage -ImagePath '{raw_path}' | Get-Disk | 
#     Set-Partition -NewDriveLetter {drive_letter}"
#     """
#     try:
#         subprocess.run(
#             mount_cmd, shell=True, check=True, capture_output=True, text=True
#         )
#         print(f"[*] RAW montado correctamente en {drive_letter}:\\")
#         return True
#     except subprocess.CalledProcessError as e:
#         print(f"[Error] Falló el montaje del RAW: {e.stderr}")
#         return False

def generate_java_code(content):
    """
    Genera el código Java Maven a partir del contenido leído.
    """
    # Implementar la lógica para generar el código aquí
    # Esto es solo un ejemplo de cómo podrías empezar
    java_code = "// Generado automáticamente\n"
    java_code += content
    return java_code


def print_hi(name):
    """
    Increíble con la lumbeis.
    :param name:
    :return:
    """
    # Use a breakpoint in the code line below to debug your script.
    print(colored(f"Hi, {name}", "blue"))  # Press Ctrl+F8 to toggle the breakpoint.


def read_binary_file(file_path):
    """
    Lee un archivo vídeo
    :param file_path:
    :return:
    """
    try:
        with open(file_path, "rb") as file:
            return file.read()
    except Exception as e:
        print(f"Error leyendo el archivo binario: {e}")
        return None


def write_binary_file(file_path, data):
    """
    Escribe un archivo binario
    :param file_path:
    :param data:
    :return:
    """
    try:
        with open(file_path, "wb") as file:
            file.write(data)
    except Exception as e:
        print(f"Error escribiendo el archivo binario: {e}")


# ▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░
def che_date():
    """
    Imprime la fecha.
    :return:
    """
    # from datetime import datetime # type: ignore

    print(datetime.now())
    return datetime.now()


# ▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░
def get_user_input():
    """
    Esta función es retorna la entrada por teclado.
    :return:
    """
    user_input_text: str = input()
    return user_input_text


def verifica_audio():
    """
    Esta función verifica el audio entrada.
    :return:
    """
    try:
        pyaudio.PyAudio()
        print("PyAudio está instalado correctamente.")
    except Exception as e:
        print(f"Error con PyAudio: {e}")

    # Verifica si speech_recognition está funcionando
    try:
        # recognizer = sr.Recognizer()
        print("speech_recognition está instalado correctamente.")
    except Exception as e:
        print(f"Error con speech_recognition: {e}")



# if __name__ == "__main__":
    # main()