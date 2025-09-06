from pygltflib import GLTF2
import trimesh

def cargar_y_mostrar_gltf(ruta_archivo):
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

if __name__ == "__main__":
    ruta = "ellen_joe_zzz/scene.gltf"
    cargar_y_mostrar_gltf(ruta)
