import sys
from funciones_smn import *

if __name__ == "__main__":
    cantidad_parametros = len(sys.argv)
    
    if cantidad_parametros == 1:
        contar_archivos_directorios()
    elif cantidad_parametros > 2:
        print("Error: Se pasó más de un parámetro. El programa terminará.")
    else:
        ruta_archivo = sys.argv[1]
        
        if ruta_archivo.endswith(".txt"):
            procesar_txt(ruta_archivo)
        elif ruta_archivo.endswith(".json"):
            procesar_json(ruta_archivo)
        else:
            print("Error: El archivo debe tener extensión .txt o .json")