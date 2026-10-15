## Ejecución
Requiere Python 3. El programa funciona de tres maneras dependiendo de lo que se le pase por consola:

- **Para procesar un TXT y exportar a JSON:** `python analisis_smn.py datos/observaciones_smn.txt`
- **Para leer un archivo JSON ya convertido:** `python analisis_smn.py obs_json/observaciones_smn.json`
- **Para contar archivos disponibles:** `python analisis_smn.py`

## Ejemplo de Salida

**Salida actual (Conversión a JSON):**
archivo del SMN, convirtiendo a json...
el directorio obs_json no existe, creándolo...
archivo guardado exitosamente.
Cantidad de ciudades que contiene el archivo: 115
Cantidad de ciudades informadas: 98

## Origen de los datos
Se descargan desde la página oficial: https://www.smn.gob.ar/descarga-de-datos
Se debe descargar el archivo `.rar` de "Observaciones actuales", descomprimirlo y guardar el `.txt` resultante.
