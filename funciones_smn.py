from datetime import datetime

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
        
        obs[ciudad] = {
            "fecha_hora": fecha_hora, "condicion": campos[3].strip(),
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