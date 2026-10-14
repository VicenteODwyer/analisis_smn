import sys
import os 
import json
from funciones_smn import *

def procesar_txt(ruta_txt):
    print("archivo del SMN, convirtiendo a json...")
    #Leemos el archivo usando la función que ya armamos 
    datos, lineas_rotas = leer_observaciones(ruta_txt)
    
    if not datos:
        return

    #Verificamos si existe la carpeta de destino y la creamos si hace falta
    directorio_destino = "obs_json"
    if not os.path.exists(directorio_destino):
        print(f"el directorio {directorio_destino} no existe, creándolo...")
        os.makedirs(directorio_destino)
        
    #Armamos la ruta del nuevo archivo .json
    #os.path.basename saca solo el nombre ("estado_tiempo.txt") de la ruta entera
    nombre_base = os.path.basename(ruta_txt)
    #os.path.splitext separa el nombre de la extensión (".txt")
    nombre_sin_ext = os.path.splitext(nombre_base)[0]
    ruta_destino = os.path.join(directorio_destino, nombre_sin_ext + ".json")
    
    #Guardamos el diccionario como archivo JSON asegurando UTF-8
    with open(ruta_destino, 'w', encoding='utf-8') as f:
        #ensure_ascii=False es para que no rompa las tildes al exportar
        json.dump(datos, f, ensure_ascii=False, indent=4)
        
    print("archivo guardado exitosamente.")
    
    print(f"Cantidad de ciudades que contiene el archivo: {cantidad_ciudades(datos)}")
    print(f"Cantidad de ciudades informadas: {cantidad_ciudades_completas(datos)}")
    

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