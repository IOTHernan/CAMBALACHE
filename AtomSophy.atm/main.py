# 👻👻👻👻👻👻👻☠️☠️☠️☠️☠️☠️☠️☠️☠️👮👮👮👮👮👮👮👮
# imports
# 👻👻👻👻👻👻👻☠️☠️☠️☠️☠️☠️☠️☠️☠️👮👮👮👮👮👮👮👮
import requests

from handlers import bot3d_gestures
from handlers import disk
from handlers import chelang
# PERMISOS.PY
from handlers.permisos import restringir_permisos, restaurar_permisos, proteger_archivo, registrar_eventos, has_permission, assign_permission, revoke_permission,  can_access_resource, ssh_execute_command, oauth2_login, verify_token
# CHEVIRTUAL.PY
from handlers.chevirtual import montar_vhd, desmontar_vhd, convertir_vdi_a_raw, montar_raw, desmontar_raw, mount_vdi
# CHETEXT.PY
from handlers.chetext import printcol, printcolor
# CHE_GENERAL_MODULE.PY
from handlers.che_general_module import speak_text, translate_text, read_file_to_speaker, che_author, configura_ventana, maneja, muestra_archivo_marked, chemarkmain, generar_html, voces, speak2, test_speak, pdf_a_txt_limited, pdf_a_txt_limpio, traducir_y_guardar, getfile, generate_java_code, print_hi, read_binary_file, write_binary_file, che_date, get_user_input, verifica_audio
# CHESCREEN.PY
from handlers.chescreen import cargar_y_mostrar_gltf,show_image,select_file,show_random_image,screensaver
# INTERNAL_DATA_DATETIME.PY
from handlers.internal_data_datetime import procesar_todo, internal_data_datetime, process_json_to_db, buscar_hashtags, generar_sha512
# 👮
from tkinter import Tk, filedialog
from PyPDF2 import PdfReader  # noqa: E402
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QComboBox, QMessageBox # type: ignore
from PyQt5.QtCore import Qt, QTimer
from datetime import datetime, time  # type: ignore
import googletrans
from googletrans import Translator

# from googletrans import Translator

from transformers import MarianMTModel, MarianTokenizer  # noqa: E402

# import colorama
# import speech_recognition as sr
import json
import os
import pathlib  # noqa: E402
import pyperclip
import pickle # type: ignore
import platform # type: ignore
import pyaudio  # noqa: E402
import pyttsx3
import pygame
import paramiko
import re # type: ignore
import sys
import shutil # type: ignore
import subprocess # type: ignore
from termcolor import colored  # noqa: E402
import threading  # type: ignore # noqa: E402, F401
import textwrap  # type: ignore # noqa: E402
from vosk import Model, KaldiRecognizer

# import curses
# import mi_libreria.che_disk
# from .mi_libreria.che_text import read_file_to_speaker, translate_text, speak_text
# import disk
# import che_disk
# from mi_libreria.che_disk import  create_directory, delete_directory, rename_directory, type_archivo,list_directory, check_disk_space, get_free_space, get_volume_info, che_if, che_cd
# from che_text import speak_text, translate_text, read_file_to_speaker
# import che_text
#from TTS.api import TTS

os.chdir("H:/AtomSophy")
sys.path.insert(0, "H:/AtomSophy")

if platform.system() == "Windows":
    try:
        import curses
        import win32api
        import win32evtlog
    except ImportError:
        print("Instala 'windows-curses' con pip para usar curses en Windows.")
else:
    pass

# Variables de entorno estilo CP/M+
entorno = {
    "prompt": "ATM> ",
}
#backend = default_backend()
salt_size = 16
key_size = 32  # AES-256
iterations = 100_000
block_size = 128

# Cargar modelo Vosk
# model = Model("I:\Python\vosk\vosk-model-es-0.42\vosk-model-es-0.42")
# model = Model("G:/api/pip/vosk/vosk-model-es-0.42/vosk-model-es-0.42")
model = Model("h:/AtomSophy/vosk_models/vosk-model-small-es-0.42/vosk-model-small-es-0.42")
recognizer = KaldiRecognizer(model, 16000)
#p = pyaudio.PyAudio()
#stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
#stream.start_stream()
#while True:
#    data = stream.read(4000, exception_on_overflow = False)
#    if len(data) == 0:
#        break
#    if rec.AcceptWaveform(data):
#        result = json.loads(rec.Result())
#        print(result['text'])
        
        
# Configurar Googletrans
### **Script Python para HTML**
translator = googletrans.Translator()
global voice_input
bot_window = None

def iniciar_bot3d(*args):
    global bot_window
    if bot_window is None:
        from PyQt5.QtWidgets import QApplication
        import sys

        app = QApplication(sys.argv)
        bot_window = bot3d_gestures.Bot3DWindow("data/ellen_joe_zzz/scene.gltf")
        bot_window.show()
        # Nota: para un entorno real, controlar loop app.exec_() en hilo separado o modo no bloqueante

def gesto_3d(*args):
    if bot_window is None:
        return "Bot 3D no iniciado. Ejecutar 'start_bot3d' primero."
    if not args:
        return "Falta nombre de gesto."
    gesto = args[0]
    if gesto in bot_window.gestures:
        bot_window.gestures[gesto]()
        return f"Gesto '{gesto}' ejecutado."
    else:
        return f"Gesto desconocido: {gesto}"

class SpeakEngine:
    def __init__(self):
        # Pre-cargar modelos para diferentes voces e idiomas
        self.models = {
            "es_femenina": "tts_models/es/mai/tacotron2-DDC",
            "es_masculina": "tts_models/es/mai/vits",
            "en_femenina": "tts_models/en/ljspeech/tacotron2-DDC",
            "en_masculina": "tts_models/en/vctk/vits",
            # Agregar modelos custom para trans/neutro cuando estÃ©n disponibles
        }
        self.tts_instances = {}
        for key, model_name in self.models.items():
            self.tts_instances[key] = TTS(model_name=model_name, progress_bar=False, gpu=False)



class TraductorOffline:
    def __init__(self):
        model_name = "Helsinki-NLP/opus-mt-en-es"
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name)

    def traducir(self, texto: str) -> str:
        batch = self.tokenizer(
            [texto], return_tensors="pt", truncation=True, padding=True
        )
        translated = self.model.generate(**batch)
        traduccion = self.tokenizer.decode(translated[0], skip_special_tokens=True)
        return traduccion

# -----------------------------------------------------------------------


# Guardar y cargar diccionario
def save_dict(data_dict, file_path):
    """
    Salvado bendiciones.
    :param data_dict:
    :param file_path:
    :return:
    """
    # with open(file_path, 'wb') as file:
    #    pickle.dump(data_dict, file)


def load_dict(file_path):
    """
    Lectura del diccionario.
    :param file_path:
    :return:
    """
    try:
        with open(file_path, "rb") as file:
            return pickle.load(file)
    except Exception as e:
        print(f"Error cargando el diccionario: {e}")
        return {}


def copy_to_clipboard(content):
    """
    Copia el contenido proporcionado al portapapeles.
    """
    pyperclip.copy(content)
    print("El contenido ha sido copiado al portapapeles.")


def read_file(file_path):
    """
    Lee el contenido de un archivo y maneja posibles excepciones.
    """
    try:
        # Verificar espacio en disco antes de leer el archivo
        check_disk_space(
            "/", 1024 * 1024 * 100
        )  # Por ejemplo, mÃ­nimo 100MB de espacio libre
        with open(file_path, "r") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no se encontró.")
    except PermissionError:
        print(f"Error: No tienes permisos para leer el archivo '{file_path}'.")
    except IOError as e:
        print(f"Error de E/S: {e}")


def analyze_input(user_input):
    # Aquí puedes agregar la lógica para analizar la entrada y ejecutar la función correspondiente
    print(f"Analizando entrada: {user_input}")
    # Ejemplo: Solo para propósitos de demostración
    if user_input == "saludo":
        print("Hola! ¿Cómo estas?")
    else:
        print("Entrada no reconocida.")


# def recognize_speech():
# recognizer = sr.Recognizer()
# with sr.Microphone() as source:
# print("Recognize_speech Ajustando al ruido ambiente, por favor espere...")
# recognizer.adjust_for_ambient_noise(source)
# print("Recognize_speech Te escucho!")
# audio = recognizer.listen(source)
# try:
# text = recognizer.recognize_google(audio)
# return text
# except sr.UnknownValueError:
# print("Recognize_speech No puede entender el audio.")
# return ""
# except sr.RequestError as e:
# print(f"No pude solicitar resultados del servicio de reconocimiento de voz; {e}")
# return ""

# def entrada_voz():
# TambiÃ©n puedes escuchar entrada por voz
# print(colored("entrada_voz Ahora escuchando...", "yellow"))
# voice_input = recognize_speech()
# print(f"Entrada de voz: {voice_input}")
# if voice_input:
# print(f"Entrada de voz: {voice_input}")
# if voice_input.lower() == "exit":
# print("Saliendo...")

# analyze_input(voice_input)

# Mostrar prompt nuevamente
# print("Ingrese otro comando o diga algo (escriba 'exit' para salir):")


def audio_capture():
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8192,
    )
    stream.start_stream()
    print("Di algo...")
    while True:
        # data = stream.read(4096)
        # if recognizer.AcceptWaveform(data):
        # result = json.loads(recognizer.Result())
        # texto = result['text']
        # if texto:
        # print(f"Texto reconocido: {texto}")
        # #traduccion = translator.translate(texto, src='en', dest='es')
        # #print(f"Traducción: {traduccion.text}")
        return "texto"


# â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–‘â–“â–’â–?
def handle_read_file_to_speaker(parts):
    if len(parts) > 1:
        read_file_to_speaker(parts[1])
    else:
        handle_help("read_file_to_speaker")


def handle_check_disk_space(parts):
    if len(parts) > 2:
        check_disk_space(parts[1], parts[2])
    else:
        handle_help("check_disk_space")


def handle_che_if(parts):
    if len(parts) >= 1:
        handle_help(parts[1])


def handle_cd(parts):
    if len(parts) > 2:
        che_cd(parts[1])
    else:
        handle_help("che_cd")


def handle_md(parts):
    if len(parts) > 2:
        create_directory(parts[1])
    else:
        handle_help("list_directory")


def handle_translate(parts):
    if len(parts) > 2:
        translate_text(parts[1], parts[2], parts[3])
    else:
        print("Uso: traducir <texto> <idioma_origen> <idioma_destiny>")


def handle_help(funcion, parametro=None):
    """
    Muestra la ayuda para la función especificada, filtrando por parÃ¡metro si se proporciona.

    ParÃ¡metros:      funcion (callable): La función para la que se desea mostrar la ayuda.
                        parametro (str, opcional): El nombre del parÃ¡metro a filtrar en la ayuda.
    """
    print(f"funcion: {funcion}")
    doc = funcion.__doc__
    print(f"funcion {doc}")
    if parametro:
        # Buscamos si el parÃ¡metro estÃ¡ mencionado en la docstring
        if parametro in doc:
            print(doc)
        else:
            print(
                f"No se encontró información sobre el parÃ¡metro '{parametro}' en {funcion.__name__}."
            )
    else:
        print(doc)
        print(colored(help.__doc__, "green"))


def handle_date(parts):
    cdate = che_date()
    speak_text("La fecha actual es:")
    print(f"La fecha actual es: ", cdate)  # noqa: F541


def handle_rm(parts):
    """
    Handles the removal of a directory.

    Args:
    parts (list): A list of strings where the second element (parts[1])
    is expected to be the path of the directory to remove.

    Returns:
            None
    """
    directory_path = parts[1]
    delete_directory(directory_path)
    pass


def handle_ren(parts):
    old_directory_path = parts[1]
    new_directory_path = parts[2]
    speak_text("Renombrando {old_directory_path} a {new_directory_path}")
    rename_directory(old_directory_path, new_directory_path)


def handle_audio(parts):
    verifica_audio()


def handle_dir(parts="*.* /a /w"):
    speak_text("Listando archivos")
    list_directory("*.*", True, False)
    p = parts.split()  # noqa: F841
    cpath = "*.*"
    show_all = False
    detailed = True

    for part in parts[1:]:
        if part == "/a":
            show_all = True
        elif part == "/w":
            detailed = False
        elif part == "/l":
            detailed = True
        else:
            cpath = part

    # Llamar a la función con los parÃ¡metros obtenidos
    print("Debug 400 list_dir")
    list_directory(path=cpath, show_all=show_all, detailed=detailed)


def handle_typepdf(parts):
    speak_text("Visualizando archivo ")
    try:
        with open(parts[1], "rb") as f:
            reader = PyPDF2.PdfReader(f)  # type: ignore # noqa: F821
            for page in reader.pages:
                print(page.extract_text())
    except FileNotFoundError:
        print("El archivo no fue encontrado.")
    except Exception as e:
        print(f"Ocurrió un error al leer el PDF: {e}")


def handle_type(parts):
    speak_text("Visualizando archivo")
    archivo = parts[1]
    type_archivo(archivo)


def handle_get_free_space(parts):
    """
    Space
    """
    get_free_space(parts[1])


def handle_get_volume_info(parts):
    p = parts.split()
    if len(p) == 0:
        get_volume_info("c:")
    else:
        get_volume_info(parts[1])


def handle_exists(parts):
    directory_path = parts[1]
    che_if(directory_path)


def handle_che_echo(parts):
    """Echo

    Args:
            parts (_type_): _description_
    """
    che_echo(parts)


def che_echo(parametros):
    """ECHO

    Args:
            parametros (parametros): String to print
    """
    salida = parametros
    protext = colored(f"{salida}", "green")
    colored(protext, "green")
    print(protext, end="\n")


def handle_speak(parametros="Use: speak [TEXT]"):
#    plen = len(parametros)
#    print(f"Debug 464 - Funtion SPEAK: {parametros} len : {plen}")
#    speak_text(parametros)
    if not parametros:
        print("Boludo: Use speak [TEXT]")
        
    #p = parametros.split()
#    p = "   "+join(parametros)
#    print(f"lenp = {plen}")
#    if len(p) > 0:
#        print("mayor a 0")
    speak_text(" ".join(parametros))
#    speak_text(parametros)
#    elif len(p) == 0:
#        print("Use: Speak [TEXT]")


def che_print_split(parametros):
    a = parametros  # noqa: F841
    b = parametros.split()
    if len(b) == 0:
        print("Sin parameters...")
        speak_text("Sin parametros")
        return -1
    else:
        for x in range(len(b)):
            print(f"Numero: {x} String: {b[x]}")


def handle_che_commands(parts=" "):
    """
    Function handle_che_commands
    """
    che_command_list(parts)


def handle_screensaver(parts="i:\wallpaper"):
#    import pygame
#import os
#import random
#import time

    # Inicializa Pygame
    pygame.init()

    # Configura la pantalla del screensaver
    width = 800
    height = 600
    pygame.display.set_caption('Screensaver')

    # Obtiene todas las imÃ¡genes en una carpeta especÃ­fica
    image_folder = 'i:/wallpaper/'
    images = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]

    # Función para mostrar una imagen aleatoria

    #screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    window = pygame.display.set_mode((width,height))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
             # Posicion del mouse en la ventana
            mouse_pos = pygame.mouse.get_pos() #  Position()
            screen_x = int(mouse_pos[0] * width / window[0])
            screen_y = int(mouse_pos[1] * height / window[1])

            # Dibujar algo simple (puedes reemplazar con tu lógica)
    screen = pygame.display.set_mode(window)  # Ojo: Si has definido 'window' antes, usar screen_size
    screen.fill(bg_color)

    # Colocar un mensaje centralizado
    font = pygame.font.Font(None, 50)
    text = font.render(f"Presiona ESC para cerrar", True, text_color)
    text_rect = text.get_rect(center=(width/2, height/2))
    screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()


def handle_translate(parametros):
    p = parametros.split()
    


def show_random_image():
    img_path = random.choice(images)
    img = pygame.image.load(img_path)
    img = pygame.transform.scale(img, (screen.get_width(), screen.get_height()))
    screen.blit(img, (0, 0))
    pygame.display.flip()

    # Muestra imÃ¡genes aleatorias hasta que se presione una tecla
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                running = False

        show_random_image()
        time.sleep(3)  # Muestra cada imagen durante 3 segundos

    # Cierra Pygame
    pygame.quit()


def handle_internal_data_datetime(parameters=" "):
    internal_data_datetime()
    
# 👻👻👻👻👻👻👻☠️☠️☠️☠️☠️☠️☠️☠️☠️👮👮👮👮👮👮👮👮

class JsonApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test PyQt5 + JSON")
        self.resize(400, 300)

        self.layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.button_load = QPushButton("Cargar JSON de ejemplo")
        self.button_load.clicked.connect(self.load_json)

        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.button_load)
        self.setLayout(self.layout)

    def load_json(self):
        # Ejemplo simple de dict a json y mostrarlo
        data = {
            "nombre": "Che GPT",
            "version": 3.10,
            "habilidades": ["PyQt5", "json", "CLI"],
        }
        json_text = json.dumps(data, indent=4, ensure_ascii=False)
        self.text_edit.setText(json_text)

    def che_pip(paquete):
        a = paquete
        if che_if(a):
            pass  # Added a pass statement to fix the indentation error


def lanzar_modo_it():
    app = QApplication(sys.argv)
    ventana = AtomSophyIT()
    ventana.show()
    sys.exit(app.exec_())


def handle_lanzar_modo_it():
    lanzar_modo_it()


def handle_modo_it():
    import platform

    so = platform.system().lower()

    menu_general = """
    AtomSophy - Modo IT - MenÃº de operaciones
    -----------------------------------------
    1. Diagnóstico bÃ¡sico del sistema
    2. Comprobar conectividad de red
    3. Analizar uso de disco
    4. Listar procesos activos
    5. Escaneo bÃ¡sico de puertos (solo Linux/WSL)
    6. Escaneo rÃ¡pido de vulnerabilidades (dependiendo de herramientas instaladas)
    0. Salir
    """

    while True:
        print(menu_general)
        opcion = input("SeleccionÃ¡ una opción: ").strip()

        if opcion == "1":
            mostrar_diagnostico_basico()
        elif opcion == "2":
            diagnosticar_red()
        elif opcion == "3":
            analizar_disco()
        elif opcion == "4":
            listar_procesos()
        elif opcion == "5":
            if so == "linux":
                escanear_puertos()
            else:
                print("Opción disponible solo en Linux/WSL.")
        elif opcion == "6":
            ejecutar_pentest_basico()
        elif opcion == "0":
            print("Saliendo del modo IT.")
            break
        else:
            print("Opción invÃ¡lida. IntentÃ¡ de nuevo.")

def mostrar_diagnostico_basico():
    import platform
    import psutil

    so = platform.system()
    version = platform.version()
    procesador = platform.processor()
    memoria = psutil.virtual_memory().total / (1024**3)

    print(f"\nSistema: {so} {version}")
    print(f"Procesador: {procesador}")
    print(f"RAM Total: {memoria:.2f} GB\n")

def diagnosticar_red():
    import socket
    try:
        host = socket.gethostbyname("www.google.com")
        socket.create_connection((host, 80), 2)
        print("Conexión a Internet activa\n")
    except Exception:
        print("Sin acceso a Internet\n")

def analizar_disco():
    import psutil
    discos = psutil.disk_partitions()
    print("\nUso de discos:")
    for d in discos:
        try:
            uso = psutil.disk_usage(d.mountpoint)
            print(f"{d.device} ({d.mountpoint}): {uso.percent:.1f}% usado")
        except PermissionError:
            print(f"{d.device} ({d.mountpoint}): Permiso denegado")
    print()

def listar_procesos():
    import psutil
    print("\nProcesos activos:")
    for proc in psutil.process_iter(['pid', 'name']):
        print(f"PID: {proc.info['pid']} - Nombre: {proc.info['name']}")
    print()

def escanear_puertos():
    import socket
    print("\nEscaneo bÃ¡sico de puertos en localhost (puertos 20-1024):")
    for port in range(20, 1025):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.2)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            print(f"Puerto {port} abierto")
        sock.close()
    print()

def ejecutar_pentest_basico():
    print("\nEjecutando pentesting bÃ¡sico... (simulación)")
    # AquÃ­ podrÃ­as integrar herramientas como nmap, nikto, metasploit si estÃ¡n disponibles.
    print("Chequeo de puertos, servicios, vulnerabilidades conocidas (no implementado)")
    print()


def filetocb(parametros):
    try:
        with open(parametros,"r") as file:
            content = file.read()
            pyperclip.copy(content)
            print("El contenido lo copiÃ© al clipboard")
            speak_text("El contenido lo copiÃ© al clipboard")
    except FileNotFoundError:
        print(f"Error: El archivo '{parametros}' no se encontró.")
    except PermissionError:
        print(f"Error: No tienes permisos para leer el archivo '{parametros}'.")
    except IOError as e:
        print(f"Error de E/S: {e}")


def handle_filetocb(parametros):
    p = parametros.split()
    if len(p) > 0:
        printcol("El comando no necesita parametros.", "red")
    else:
        filetocb()
        
        
def handle_printcol(params):
    printcol(" ".join(params))


def handle_echo(params):
    print(" ".join(params))


def handle_set(params):
    if len(params) >= 2:
        entorno[params[0]] = " ".join(params[1:])
        print(f"{params[0]} = {entorno[params[0]]}")
    else:
        print("Uso: set var valor")

def handle_env(params):
    for k, v in entorno.items():
        print(f"{k} = {v}")

#def handle_help(params):
#    print("Comandos disponibles:")
#    for cmd in sorted(commands.keys()):
#        print(f" - {cmd}")

def handle_runatm(params):
    if not params:
        print("Uso: runatm archivo.atm")
        return
    path = params[0]
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for linea in f:
                linea = limpiar_comentarios(linea.strip())
                if not linea:
                    continue
                print(f"=> {linea}")
                parsear_y_ejecutar(linea)
    except FileNotFoundError:
        print(f"[x] Archivo no encontrado: {path}")


#def handle_screensaver(params):
#            screensaver()
            

def handle_set_file_to_var(command_string):
    # Sintaxis esperada: set varname << archivo.ext
    if "<<" not in command_string:
        print("[x] Sintaxis invalida. Usa: set var << archivo")
        return

    parts = command_string.replace("set", "", 1).strip().split("<<")
    if len(parts) != 2:
        print("[x] Error de parseo.")
        return

    varname = parts[0].strip()
    filepath = parts[1].strip()

    try:
        with open(filepath, "rb") as f:
            data = f.read()
            variables_entorno[varname] = data
            print(f"[set] Variable '{varname}' cargada desde '{filepath}' ({len(data)} bytes)")
    except Exception as e:
        print(f"[x] Error leyendo archivo '{filepath}': {e}")


def encrypt_and_save(data: bytes, password: str, output_path: str):
    encrypted = encrypt_bytes(data, password)
    with open(output_path, "wb") as f:
        f.write(encrypted)

def load_and_decrypt(input_path: str, password: str) -> bytes:
    with open(input_path, "rb") as f:
        enc_data = f.read()
    return decrypt_bytes(enc_data, password)


def handle_encrypt_ram(params):
    if len(params) < 2:
        print("Uso: encrypt_ram 'texto o datos' clave")
        return
    texto = params[0]
    clave = params[1]

    data = texto.encode()
    encrypted = encrypt_bytes(data, clave)
    print(f"[encrypt_ram] Datos cifrados en RAM: {encrypted.hex()}")

def handle_decrypt_ram(params):
    if len(params) < 2:
        print("Uso: decrypt_ram datos_hex clave")
        return
    datos_hex = params[0]
    clave = params[1]

    try:
        encrypted = bytes.fromhex(datos_hex)
        decrypted = decrypt_bytes(encrypted, clave)
        print(f"[decrypt_ram] Datos descifrados: {decrypted.decode()}")
    except Exception as e:
        print(f"[x] Error descifrando datos RAM: {e}")

def handle_encrypt(params):
    if len(params) < 2:
        print("Uso: encrypt archivo clave [--type-encrypt AES]")
        return

    archivo = params[0]
    clave = params[1]

    print(f"[encrypt] Cifrando {archivo} con AES...")
    try:
        encrypt_file(archivo, clave)
        print(f"[encrypt] Archivo cifrado: {archivo}.enc")
    except Exception as e:
        print(f"[x] Error en cifrado: {e}")

def handle_decrypt(params):
    if len(params) < 2:
        print("Uso: decrypt archivo.clave [--type-encrypt AES]")
        return

    archivo = params[0]
    clave = params[1]

    print(f"[decrypt] Descifrando {archivo} con AES...")
    try:
        decrypt_file(archivo, clave)
        print(f"[decrypt] Archivo descifrado guardado.")
    except Exception as e:
        print(f"[x] Error en descifrado: {e}")


def handle_show_random_image(params):
    show_random_image()
    

# 👻👻👻👻👻👻👻☠️☠️☠️☠️☠️☠️☠️☠️☠️👮👮👮👮👮👮👮👮

def parsear_redireccionamiento(linea):
    if ">>>" in linea:
        partes = linea.split(">>>")
        return ("append_out", partes[0].strip(), partes[1].strip())
    elif ">>" in linea:
        partes = linea.split(">>")
        return ("write_out", partes[0].strip(), partes[1].strip())
    elif "<<<" in linea:
        partes = linea.split("<<<")
        return ("inline_in", partes[0].strip(), partes[1].strip())
    elif "<<" in linea:
        partes = linea.split("<<")
        return ("file_in", partes[0].strip(), partes[1].strip())
    else:
        return ("normal", linea.strip(), None)

# 👻👻👻👻👻👻👻☠️☠️☠️☠️☠️☠️☠️☠️☠️👮👮👮👮👮👮👮👮

def ejecutar_redir(tipo, comando, archivo_o_valor):
    if tipo == "write_out":
        original_stdout = sys.stdout
        with open(archivo_o_valor, "w") as f:
            sys.stdout = f
            parsear_y_ejecutar(comando)
        sys.stdout = original_stdout

    elif tipo == "append_out":
        original_stdout = sys.stdout
        with open(archivo_o_valor, "a") as f:
            sys.stdout = f
            parsear_y_ejecutar(comando)
        sys.stdout = original_stdout

    elif tipo == "file_in":
        try:
            with open(archivo_o_valor, 'r') as f:
                contenido = f.read().strip()
                nuevo_cmd = f"{comando} {contenido}"
                parsear_y_ejecutar(nuevo_cmd)
        except FileNotFoundError:
            print(f"[x] Archivo no encontrado: {archivo_o_valor}")

    elif tipo == "inline_in":
        nuevo_cmd = f'{comando} "{archivo_o_valor}"'
        parsear_y_ejecutar(nuevo_cmd)

    else:  # normal
        parsear_y_ejecutar(comando)


# 👻👻👻👻👻👻👻☠️☠️☠️☠️☠️☠️☠️☠️☠️👮👮👮👮👮👮👮👮

# ====== PARSER Y EJECUCIÃ“N ======
def limpiar_comentarios(linea):
    return re.sub(r'#.*(?=(?:[^"\']*["\'][^"\']*["\'])*[^"\']*$)', '', linea).strip()

# # 👻👻👻👻👻👻👻☠️☠️☠️☠️☠️☠️☠️☠️☠️👮👮👮👮👮👮👮👮


def expandir_variables(param):
    if param.startswith("$"):
        print(f"expandir {param}")
        return entorno.get(param[1:], "")
    print(f"expandir return  {param}")
    return param

# # 👻👻👻👻👻👻👻☠️☠️☠️☠️☠️☠️☠️☠️☠️👮👮👮👮👮👮👮👮


def parsear_funcion_simple(cadena):
    print(f"parsear_Funcion simple : {cadena}")
    try:
        idx = cadena.index("(")
        funcion = cadena[:idx].strip()
        params_str = cadena[idx+1: cadena.rindex(")")].strip()

        if not params_str:
            print("not params_str")
            return funcion, []

        params = []
        buffer = ""
        dentro_comillas = False
        comilla_actual = ""

        for c in params_str:
            if c in ('"', "'"):
                if dentro_comillas and c == comilla_actual:
                    dentro_comillas = False
                else:
                    dentro_comillas = True
                    comilla_actual = c
                buffer += c
            elif c == "," and not dentro_comillas:
                params.append(buffer.strip().strip("'\""))
                buffer = ""
            else:
                buffer += c
        if buffer:
            params.append(buffer.strip().strip("'\""))
        return funcion, params
    except Exception as e:
        print(f"[x] Error parseando: {e}")
        return None, []


# # 👻👻👻👻👻👻👻☠️☠️☠️☠️☠️☠️☠️☠️☠️👮👮👮👮👮👮👮👮


def parsear_y_ejecutar(entrada):
    print(f"Debug 991 parsear y ejecutar {entrada}")
    if "(" in entrada and ")" in entrada:
        print(f"Debug 993 parsear_funcion_simple {entrada}")
        funcion, args = parsear_funcion_simple(entrada)
    else:
        partes = entrada.split()
        print(f"Debug 995 partes split: {partes}")
        if not partes:
            print("partes vacia")
            return
        funcion = partes[0]
        args = partes[1:]
    print(f"Debug 1001 - args: {args}")
    args = [expandir_variables(arg) for arg in args]

    if funcion in commands:
        try:
            print(f"Debug 1006 try - funcion: {commands[funcion]} - Argumentos: {args}")
            commands[funcion](args)
        except Exception as e:
            print("Debug 1011 - Exception")
            commands[funcion](args)
            print("Exception")
            print(f"[x] Error ejecutando '{funcion}': {e} - Argumentos: {args} -")
    else:
        print("else")
        print(f"[x] Comando desconocido: {funcion}")


# 👻👻👻👻👻👻👻☠️☠️☠️☠️☠️☠️☠️☠️☠️👮👮👮👮👮👮👮👮


def main():
    """
    Este es el procedimiento central
    :return:
    """
    print("Debug 1041 main")

    while True:
        # colored("Hello, World!", "red", "on_black", ["bold", "blink"])
        #printcol("Hello World!","red")
        directorio_actual = os.getcwd()
        prompt_text = colored(f"{directorio_actual}>", "red")
        entorno = {
            "prompt": prompt_text,
        }
        printcol(directorio_actual, "red")
        #print(prompt_text, end="")
        # t1 = threading.Thread(target=entrada_voz)
        # t2 = threading.Thread(target=get_user_input)

        # Iniciamos ambos threads
        # t1.start()
        # t2.start()
        # Esperamos a que terminen ambos
        # t1.join()
        # t2.join()
        # audio_capture()
        # print("EstÃ¡s en main...voice input:", voice_input)
        #user_input = get_user_input()
        # print('LEN :',len(user_input)) # Debug: muesta len
        #parts = user_input.split()
        #command = user_input.lower()
        try:
            # print("Try:")
            entrada = input(entorno.get("prompt", ">>> ")).strip()
            if entrada.lower() in ("exit", "quit"):
                speak_text("Cerrando la aplicación, vuelve cuando quieras")
                printcol("Cerrando la aplicación, vuelve cuando quieras","yellow")
                speak_text("Forro")
                break
            print(f"Debug 1059 - parsear_y_ejecutar {entrada}")
            parsear_y_ejecutar(entrada)
            pass
#            break
        except KeyboardInterrupt:
            printcol("\n[!] Interrupción del operador.\nCerrando la aplicación, vuelve cuando quieras","yellow")
            speak_text("Forro")
            print("\n[!] Interrupción del operador.")
            break
        except Exception as e:
            print(f"EXCEPTION [x] Error fatal: {e}")

# 👻👻👻👻👻👻👻☠️☠️☠️☠️☠️☠️☠️☠️☠️👮👮👮👮👮👮👮👮

def che_command_list(parts):
    printcol("👻 ® DISK","red") # ðŸ‘®
    printcol("checkdiskspace","blue")
    printcol("cheif","blue")
    printcol("cd        Show or set the current dir...","blue")
    printcol("chdir     Show or set the current dir...","blue")
    printcol("md        Create a new dir...","blue")
    printcol("mkdir     Create a new dir...","blue")
    printcol("rm","blue")
    printcol("rmdir","blue")
    printcol("dir","blue")
    printcol("typepdf","blue")
    printcol("type","blue")
    printcol("freespace","blue")
    printcol("volumeinfo","blue")
    printcol("exists","blue")
    printcol("👻 ® CHELANG", "green") # ðŸ‘®
    printcol("runatm - run a AtomSophy Script File", "green")
    printcol("echo", "green")
    printcol("speak", "green")
    printcol("readtospeaker", "green")
    printcol("traducir", "green")
    printcol("help", "green")
    printcol("date", "green")
    printcol("pdf_a_txt_limited -pdf_path: str, txt_path: str, line_width: int = 80-", "green")
    printcol("👻 ® CHETEXT","red") # ®
    printcol("👻 ® CHE_GENERAL_MODULE") # ðŸ‘®
    printcol("👻 ® CHESCREEN","blue") # ðŸ‘®
    printcol("screensaver - Run internal screensaver","blue")
    printcol("show_random_image","blue")
    printcol("printcol")
    printcol("👻 internal_data_datetime")
    printcol("set   Set a value to variable...","yellow")
    printcol("listprocess","yellow")
    
# 👮-------------------------------
# 👮------ MAIN -----------------
# 👮-------------------------------
if __name__ == "__main__":
    commands = {
        "runmodeit": handle_lanzar_modo_it,
        "modeit": handle_modo_it,
        "commands": handle_che_commands,
#        "echo": handle_che_echo,
        "echo": handle_echo,
        "speak": handle_speak,
        "readtospeaker": handle_read_file_to_speaker,
        "checkdiskspace": handle_check_disk_space,
        "cheif": handle_che_if,
        "cd": handle_cd,
        "chdir": handle_cd,
        "md": handle_md,
        "mkdir": handle_md,
        "rm": handle_rm,
        "rmdir": handle_rm,
        "traducir": handle_translate,
#        "help": handle_help,
        "date": handle_date,
        "dir": handle_dir,
        "typepdf": handle_typepdf,
        "type": handle_type,
        "freespace": handle_get_free_space,
        "volumeinfo": handle_get_volume_info,
        "exists": handle_exists,
        "filetocb": handle_filetocb,
        "start_bot3d": iniciar_bot3d,
        "gesture_3d": gesto_3d,
        "set": handle_set,
        "env": handle_env,
        "help": handle_help,
        "runatm": handle_runatm,
        "encrypt": handle_encrypt,
        "decrypt": handle_decrypt,
        "screensaver": handle_screensaver,
        "show_random_image": handle_show_random_image,
        "select_file": select_file,
        "printcol": handle_printcol,
        "internal_data_datetime": handle_internal_data_datetime
        }

    voice_input = ""
    printcol("Hola! Soy AtomSophy! ¿Cómo estas?", "blue")
    speak_text("Hola soy AtomSophy, ¿Cómo estas che?")
    from sys import argv

    if len(argv) > 1:
        print("Argumentos detectados, despachando tareas.",len(argv))
        # Lógica para manejar parametros
    else:
        print("Modo interactivo activado.")
        # Lógica para flujo manual
    #app = QApplication(sys.argv)
    #ventana = JsonApp()
    #ventana.show()
    # sys.exit(app.exec_())

    # Ejemplo
    # if __name__ == "__main__":
    #entrada = 'typeBinarios("C:/Users/Fran/Documents/file.txt")'
    #func, parametros = parsear_funcion_simple(entrada)
    #print("Los errores...")
    #print(f"Función: {func}")
    #print("ParÃ¡metros:")
    #for p in parametros:
    #    print(f"  {p}")
    pdf_file = "clipperManual.pdf"
    txt_intermedio = "documento_extraido.txt"
    txt_traducido = "documento_traducido.txt"
    #print("[*] Extrayendo texto de PDF...")
    #texto_ingles = pdf_a_txt_limited(pdf_file)
    #print(f"[*] Guardando texto extraÃ­do en {txt_intermedio}...")
    #with open(txt_intermedio, "w", encoding="utf-8") as f:
#        f.write(texto_ingles)
    #print("[*] Traduciendo texto extraÃ­do...")
#    traducir_y_guardar(texto_ingles, txt_traducido)
    #print(f"[*] Traducción guardada en {txt_traducido}")
    main()
# 👻👻👻👻👻👻👻☠️☠️☠️☠️☠️☠️☠️☠️☠️👮👮👮👮👮👮👮👮
