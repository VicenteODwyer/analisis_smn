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