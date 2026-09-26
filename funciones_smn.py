from datetime import datetime

def parsear_fecha_hora(fecha: str, hora: str) -> datetime:
    meses = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, 
             "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12}
    
    p_fecha = fecha.split("-")
    dia = int(p_fecha[0])
    mes = meses.get(p_fecha[1].lower(), 1)
    anio = int(p_fecha[2])
    
    p_hora = hora.split(":")
    return datetime(anio, mes, dia, int(p_hora[0]), int(p_hora[1]))

def separar_viento(campo_viento: str) -> tuple:
    v = campo_viento.strip()
    if v.lower() == "calma":
        return ("Calma", 0.0) 
    
    partes = v.rsplit(maxsplit=1)
    if len(partes) == 2:
        try:
            return (partes[0].strip(), float(partes[1]))
        except:
            return (partes[0].strip(), 0.0)
    return (v, 0.0)

def leer_observaciones(ruta: str) -> dict:
    obs = {}
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            for linea in f:
                campos = linea.strip().split(';')
                if len(campos) != 10:
                    continue 
                
                ciudad = campos[0].strip()
                fecha_hora = parsear_fecha_hora(campos[1].strip(), campos[2].strip())
                
                try: temp = float(campos[5])
                except: temp = None
                
                if campos[6].strip().lower() == "no se calcula":
                    sensacion = None
                else:
                    try: sensacion = float(campos[6])
                    except: sensacion = None
                
                v_dir, v_vel = separar_viento(campos[8])
                
                obs[ciudad] = {
                    "fecha_hora": fecha_hora, "condicion": campos[3].strip(),
                    "visibilidad": campos[4].strip(), "temperatura": temp,
                    "sensacion_termica": sensacion, "humedad": campos[7].strip(),
                    "direccion_viento": v_dir, "velocidad_viento": v_vel,
                    "presion": campos[9].strip()
                }
    except FileNotFoundError:
        print("Error: No se encontró el archivo de datos.")
    return obs
def cantidad_ciudades(obs: dict) -> int:
    return len(obs)

def cantidad_ciudades_completas(obs: dict) -> int:
    completas = 0
    for datos in obs.values():
        if None not in datos.values():
            completas += 1
    return completas

def top_n_ciudades(obs: dict, campo: str, n: int, descendente: bool = True) -> list:
    validas = []
    for ciudad, datos in obs.items():
        if datos[campo] is not None:
            validas.append((ciudad, datos[campo]))
    
    validas.sort(key=lambda x: x[1], reverse=descendente)
    return validas[:n]

def horarios_reportados(obs: dict) -> list:
    horarios = set()
    for datos in obs.values():
        h = datos["fecha_hora"].strftime("%H:%M")
        horarios.add(h)
    lista = list(horarios)
    lista.sort()
    return lista