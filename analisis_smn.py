import sys
from funciones_smn import *

def mostrar_resumen(obs: dict) -> None:
    print("\n=== RESUMEN METEOROLOGICO ===")
    print(f"Total de ciudades leidas: {cantidad_ciudades(obs)}")
    print(f"Ciudades con datos completos: {cantidad_ciudades_completas(obs)}")
    print(f"Horarios encontrados: {', '.join(horarios_reportados(obs))}")
    
    print("\n--- TOP 5 MAS CALIDAS ---")
    for c, v in top_n_ciudades(obs, "temperatura", 5, True):
        print(f"{c}: {v} °C")

    print("\n--- TOP 5 MAS FRIAS ---")
    for c, v in top_n_ciudades(obs, "temperatura", 5, False):
        print(f"{c}: {v} °C")
        
    print("\n--- TOP 5 CON MAS VIENTO ---")
    for c, v in top_n_ciudades(obs, "velocidad_viento", 5, True):
        print(f"{c}: {v} km/h")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Tenes que pasar el txt. Ejemplo: python analisis_smn.py datos/observaciones.txt")
    else:
        ruta = sys.argv[1]
        datos = leer_observaciones(ruta)
        if datos:
            mostrar_resumen(datos)