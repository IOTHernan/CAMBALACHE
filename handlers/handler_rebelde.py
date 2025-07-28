def rebelde(func):
    def wrapper(*args, **kwargs):
        print("Ejecutando con resistencia simbólica...")
        resultado = func(*args, **kwargs)
        print("Función completada con conciencia de clase.")
        return resultado
    return wrapper

@rebelde
def buscar_rumbo():
    return "Caminito al costado del mundo..."

if __name__ == "__main__":
    print(buscar_rumbo())
