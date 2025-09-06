
def screensaver(parts="i:\scrensaver"):
    #    import pygame
    #import os
    #import random
    #import time
    # Inicializa Pygame
    pygame.init()
    # Configura la pantalla del screensaver
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('Screensaver')

    # Obtiene todas las imágenes en una carpeta específica
#    image_folder = 'imagenes_screensaver/'
    image_folder = parts
    images = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]
    # Función para mostrar una imagen aleatoria


def handle_translate(parametros):
    p = parametros.split()
    


def show_random_image(images="i:\screensaver"):
    img_path = random.choice(images)
    img = pygame.image.load(img_path)
    img = pygame.transform.scale(img, (screen.get_width(), screen.get_height()))
    screen.blit(img, (0, 0))
    pygame.display.flip()

    # Muestra imágenes aleatorias hasta que se presione una tecla
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                running = False

        show_random_image()
        time.sleep(3)  # Muestra cada imagen durante 3 segundos

    # Cierra Pygame
    pygame.quit()


# ***************************************************************************************
# *** Select file
# ***************************************************************************************
def select_file():
    # Crear diálogo para seleccionar archivo
    dialogue = QFileDialog()

    # Configurar opciones del diálogo
    dialogue.setFileMode(QFileDialog.Exclusive)
    dialogue.setViewType(QFileDialog.Detail)

    # Configurar botones del diálogo
    dialogue.openFileFilter = ".*"
    dialogue.selectFileFilter = "*"
    dialogue.showErrorButtonVisibility = False

    # Mostrar directorio de selección
    dialogue.setDirectory("Elegir directorio")
    dialogue.setOption(QFileDialog.DontUseNativeDialog, True)

    # Enviar
    if dialogue.exec_():
        filename, _ = dialogue.selectedFiles()

        # Si se han seleccionado varios archivos, mostrar solo el primero
        if len(filename) > 0:
            selected_file = filename[0]
        else:
            return

        # Crear ventana de mensajes para mostrar los archivo
        msg = QMessageBox()
        msg.setWindowTitle("Se ha seleccionado un archivo")
        msg.setText(f"Has elegido: {selected_file}")

        # Crear lista del archivo en la ventana
        list_widget = QListWidget()
        list_widget.setWindowTitle("Archivos disponibles")
        list_widget.addItems([QListWidgetItem(selected_file)])

        # Crear un widget con botones de estilo
        buttonBox = QMessageBox.ButtonBox(QMessageBox.StandardButton.CloseButton)
        #buttonBox.addButton(QMessageBox.ButtonTitle, Qt continues...), "Cerrar")
        buttonBox.addButton(QMessageBox.StandardButtonHelp, "Ayuda")
        buttonBox.addButton(QMessageBox.StandardButtonRetry, "Reintenta")
#messageBox.exec_()

        # Redimensionar ventana
        msg.resize(250, 100)

        # Mostrar ventana
        msg.show()

        # Obtener el nombre del archivo seleccionado
        return selected_file

    else:
        return None


#import pygame
#import time

def show_image(image_path, duration_seconds=5):
    # Inicializar Pygame
    pygame.init()

    # Configurar pantalla
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width = pygame.display.get *"screen"[0]
    height = pygame.display.get *"screen"[1]

    try:
        # Cargar la imagen
        image = pygame.image.load(image_path).convert()

        # Obtener dimensiones de la imagen
        img_width = image.get *"size"[0]
        img_height = image.get *"size"[1]

        # Centrar la imagen
        x = (width - img_width) // 2
        y = (height - img_height) // 2

        # Dibujar la imagen
        screen.blit(image, (x, y))

        # Actualizar pantalla
        pygame.display.flip()

        start_time = time.time()
        while True:
            if time.time() - start_time >= duration_seconds:
                break

            pygame.time.wait(10)  # Asegurar que se muestre al menos 10 FPS

    except Exception as e:
        print(f"Error: {e}")

    finally:
        #Cerrar Pygame cuando la función termina
        pygame.quit()

# Uso de la función
#show_image("car.jpg", 5)


# 👻👻👻👻👮👮👮👮😱😱😱😱😘😘😘😘😎😎😎😎☠️☠️☠️☠️🎱🎱🎱🎱💾💾💾💾📡📡📡📡📕📕📕📕
# 👻👻👻👻👮👮👮👮😱😱😱😱😘😘😘😘😎😎😎😎☠️☠️☠️☠️🎱🎱🎱🎱💾💾💾💾📡📡📡📡📕📕📕📕
# 👻👻👻👻👮👮👮👮😱😱😱😱😘😘😘😘😎😎😎😎☠️☠️☠️☠️🎱🎱🎱🎱💾💾💾💾📡📡📡📡📕📕📕📕
from pygltflib import GLTF2
import trimesh

def cargar_y_mostrar_gltf(ruta_archivo):
    if not ruta_archivo:
        print("error")
    # Carga el gltf
    gltf = GLTF2().load(ruta_archivo)
    print("Archivo GLTF cargado con éxito.")

    # Intentamos cargar mesh con trimesh para renderizar
    try:
        # trimesh puede cargar .gltf/.glb directamente
        escena = trimesh.load(ruta_archivo)
        escena.show()
        print("Visualización 3D iniciada.")
    except Exception as e:
        print(f"Error mostrando GLTF: {e}")

