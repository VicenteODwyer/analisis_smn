import sys
import os 
import json
from funciones_smn import *

def procesar_txt(ruta_txt):
    print(f"Detectado archivo SMN: {ruta_txt}")
    

def procesar_json(ruta_json):
    print(f"Detectado archivo JSON: {ruta_json}")
    

def contar_archivos_directorios():
    txt_count = 0
    json_count = 0
    
    if os.path.exists("datos/"):
        for archivo in os.listdir("datos/"):
            if archivo.endswith(".txt"):
                txt_count += 1
 
    if os.path.exists("obs_json/"):
        for archivo in os.listdir("obs_json/"):
            if archivo.endswith(".json"):
                json_count += 1
                
    print("Aviso: No se pasó ningún archivo como parámetro.")
    print(f"Hay {txt_count} archivos .txt en datos/ y {json_count} archivos .json en obs_json/")


if __name__ == "__main__":
    cantidad_parametros = len(sys.argv)
   
    if cantidad_parametros == 1:
        contar_archivos_directorios()
        
    elif cantidad_parametros > 2:
        print("Error: Se pasó más de un parámetro. El programa terminará.")
    else:
        ruta_archivo = sys.argv[1]
        
        # Filtramos por extensión
        if ruta_archivo.endswith(".txt"):
            procesar_txt(ruta_archivo)
        elif ruta_archivo.endswith(".json"):
            procesar_json(ruta_archivo)
        else:
            print("Error: El archivo debe tener extensión .txt o .json")