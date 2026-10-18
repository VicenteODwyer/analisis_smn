from datetime import datetime
import os
import json


def parsear_fecha_hora(fecha: str, hora: str) -> datetime:
    # Usamos un diccionario para evitar hacer 12 condicionales if/elif
    meses = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, 
             "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12}
    
    p_fecha = fecha.split("-")
    dia = int(p_fecha[0])
    # .get() busca el mes, y si por algún error el texto no está en el diccionario, devuelve 1 (enero) por defecto
    mes = meses.get(p_fecha[1].lower(), 1)
    anio = int(p_fecha[2])
    
    p_hora = hora.split(":")
    return datetime(anio, mes, dia, int(p_hora[0]), int(p_hora[1]))

def separar_viento(campo_viento: str) -> tuple:
    v = campo_viento.strip()
    if v.lower() == "calma":
        return ("Calma", 0.0) 
    # rsplit(maxsplit=1) corta desde la derecha una sola vez
    # Esto asegura que si la dirección tiene espacios (ej. "Sur Sudeste  13"), 
    # solo separe el último número y no rompa el texto de la dirección
    partes = v.rsplit(maxsplit=1)
    if len(partes) == 2:
        try:
            return (partes[0].strip(), float(partes[1]))
        except:
            return (partes[0].strip(), 0.0)
    return (v, 0.0)

def leer_observaciones(ruta: str) -> dict:
    obs = {}
    lineas_rotas = 0
    def obtener_lineas(ruta_archivo):
        try:
            # Intento primario con estándar UTF-8
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                return archivo.readlines()
        except UnicodeDecodeError:
            # Fallback a latin-1, que es el formato de la red del SMN
            with open(ruta_archivo, 'r', encoding='latin-1') as archivo:
                return archivo.readlines()
        except FileNotFoundError:
            return None

    lineas = obtener_lineas(ruta)
    
    # Validación temprana 
    if lineas is None:
        print(f"Error: No se encontró el archivo en '{ruta}'")
        return obs, lineas_rotas

    for linea in lineas:
        campos = linea.strip().split(';')
        if len(campos) != 10:
            lineas_rotas += 1
            continue 
        
        ciudad = campos[0].strip()
        fecha_hora = parsear_fecha_hora(campos[1].strip(), campos[2].strip())
        
        # Si falla, va None en vez de 0.0
        # ya que 0.0°C es un dato climático válido.
        try: temp = float(campos[5])
        except ValueError: temp = None
        
        if campos[6].strip().lower() == "no se calcula":
            sensacion = None
        else:
            try: sensacion = float(campos[6])
            except ValueError: sensacion = None
        
        v_dir, v_vel = separar_viento(campos[8])

        fecha_iso = fecha_hora.isoformat(timespec='minutes')
        obs[ciudad] = {
            "fecha_hora": fecha_iso, "condicion": campos[3].strip(),
            "visibilidad": campos[4].strip(), "temperatura": temp,
            "sensacion_termica": sensacion, "humedad": campos[7].strip(),
            "direccion_viento": v_dir, "velocidad_viento": v_vel,
            "presion": campos[9].strip()
        }
        
    return obs, lineas_rotas

def cantidad_ciudades(obs: dict) -> int:
    return len(obs)

def cantidad_ciudades_completas(obs: dict) -> int:
    completas = 0
    for datos in obs.values():
        # Si no hay ningún 'None' dentro de los valores numéricos de esta ciudad, la contamos como completa
        if None not in datos.values():
            completas += 1
    return completas

def top_n_ciudades(obs: dict, campo: str, n: int, descendente: bool = True) -> list:
    validas = []
    for ciudad, datos in obs.items():
        if datos[campo] is not None:
            # Guardamos tuplas en la lista de validas, por ejemplo: ("Bariloche", -2.5)
            validas.append((ciudad, datos[campo]))
    # El lambda x: x[1] le dice al método sort que ordene usando el valor numérico (la posición 1 de la tupla),
    # no el nombre alfabético de la ciudad (que sería la posición 0)
    validas.sort(key=lambda x: x[1], reverse=descendente)
    return validas[:n]

def horarios_reportados(obs: dict) -> list:
    # Usamos un 'set' (conjunto) porque matemáticamente no admite duplicados.
    # Si 50 ciudades reportan a las "08:00", el set la guarda una sola vez
    horarios = set()
    for datos in obs.values():
        h = datos["fecha_hora"].strftime("%H:%M")
        horarios.add(h)
    lista = list(horarios)
    lista.sort()
    return lista

def reporte_faltantes(obs: dict) -> dict:
    faltantes = {
        "temperatura": [], "sensacion_termica": [],
        "humedad": [], "presion": []
    }
    
    for ciudad, datos in obs.items():
        for campo in faltantes.keys():
            # Si el campo (ej: "presion") tiene asignado un None, agregamos el nombre de la ciudad a la lista
            if datos[campo] is None:
                faltantes[campo].append(ciudad)
                
    return faltantes
def extremos_con_empates(obs: dict, campo: str, buscar_maximo: bool = True) -> tuple:
    validas = {c: d[campo] for c, d in obs.items() if d[campo] is not None}
    if not validas:
        return [], None
    
    # Encontramos el valor máximo o mínimo absoluto
    mejor_valor = max(validas.values()) if buscar_maximo else min(validas.values())
    
    # Buscamos todas las ciudades que tengan exactamente ese valor (empates)
    empates = [c for c, v in validas.items() if v == mejor_valor]
    return empates, mejor_valor

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
    try:
        #Abrimos el archivo JSON forzando utf-8 como pide el profe
        with open(ruta_json, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            
        #Imprimimos exactamente el mismo resumen de 2 líneas
        print(f"Cantidad de ciudades que contiene el archivo: {cantidad_ciudades(datos)}")
        print(f"Cantidad de ciudades informadas: {cantidad_ciudades_completas(datos)}")
        
    except FileNotFoundError:
        print("Error: No se encontró el archivo JSON en la ruta indicada.")
    except json.JSONDecodeError:
        print("Error: El archivo no tiene un formato JSON válido.")
    

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