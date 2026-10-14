import sys
from funciones_smn import *

def mostrar_resumen(obs: dict, rotas: int) -> None:
    if rotas > 0:
        print(f" AVISO: Se descartaron {rotas} líneas mal formadas o con columnas ausentes.")
    print("\n=== RESUMEN METEOROLOGICO ===")
    print(f"Total de ciudades leidas: {cantidad_ciudades(obs)}")
    print(f"Ciudades con datos completos: {cantidad_ciudades_completas(obs)}")
    print(f"Horarios encontrados: {', '.join(horarios_reportados(obs))}")

    print("\n--- EXTREMOS CON EMPATES ---")
    c_max_t, max_t = extremos_con_empates(obs, "temperatura", True)
    print(f"Temperatura Máxima: {max_t} °C en {', '.join(c_max_t)}")
    
    c_min_t, min_t = extremos_con_empates(obs, "temperatura", False)
    print(f"Temperatura Mínima: {min_t} °C en {', '.join(c_min_t)}")
    
    c_max_v, max_v = extremos_con_empates(obs, "velocidad_viento", True)
    print(f"Viento Máximo: {max_v} km/h en {', '.join(c_max_v)}")
    
    c_min_v, min_v = extremos_con_empates(obs, "velocidad_viento", False)
    print(f"Viento Mínimo: {min_v} km/h en {', '.join(c_min_v)}")
    
    print("\n--- TOP 5 MAS CALIDAS ---")
    # Llamamos a top_n_ciudades pidiendo 5 elementos, ordenados de forma descendente (True)
    for c, v in top_n_ciudades(obs, "temperatura", 5, True):
        print(f"{c}: {v} °C")

    print("\n--- TOP 5 MAS FRIAS ---")
    # Al pasar False en descendente, ordena de menor a mayor (las más frías primero)
    for c, v in top_n_ciudades(obs, "temperatura", 5, False):
        print(f"{c}: {v} °C")
        
    print("\n--- TOP 5 CON MAS VIENTO ---")
    for c, v in top_n_ciudades(obs, "velocidad_viento", 5, True):
        print(f"{c}: {v} km/h")

    print("\n--- DATOS FALTANTES ---")
    faltantes = reporte_faltantes(obs)
    for campo, ciudades in faltantes.items():
        if len(ciudades) > 0:
            # Mostramos cuántas faltan y un recorte de las primeras 3 ciudades como ejemplo
            print(f"{campo.capitalize()}: Falta en {len(ciudades)} ciudades ({', '.join(ciudades[:3])}...)")
# Este if verifica si el script se está ejecutando directamente desde la terminal
if __name__ == "__main__":
    # sys.argv es una lista con lo que escribís en la consola. 
    # sys.argv[0] es "analisis_smn.py" y sys.argv[1] captura la ruta del txt
    if len(sys.argv) < 2:
        # Si el usuario no mandó la ruta, atajamos el error (evita IndexError)
        print("Error: Tenes que pasar el txt. Ejemplo: python analisis_smn.py datos/observaciones.txt")
    else:
        ruta = sys.argv[1]
        datos, lineas_rotas = leer_observaciones(ruta)
        # Solo mostramos el resumen si el diccionario 'datos' no está vacío
        if not datos:
            print("El archivo está vacío o no se encontraron datos válidos con el formato correcto.")
        else:
            mostrar_resumen(datos, lineas_rotas)