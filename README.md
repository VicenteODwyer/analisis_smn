## Ejecución
Requiere Python 3. Se ejecuta pasando la ruta del archivo `.txt` de observaciones:
`python analisis_smn.py datos/observaciones_smn.txt`

## Ejemplo de Salida
```text
=== RESUMEN METEOROLOGICO ===
AVISO: Se descartaron 2 líneas mal formadas o con columnas ausentes.
Total de ciudades leidas: 115
Ciudades con datos completos: 98

--- EXTREMOS CON EMPATES ---
Temperatura Máxima: 28.5 °C en Formosa, Las Lomitas
Temperatura Mínima: -4.2 °C en San Carlos de Bariloche

## Origen de los datos
Se descargan desde la página oficial: https://www.smn.gob.ar/descarga-de-datos
Se debe descargar el archivo `.rar` de "Observaciones actuales", descomprimirlo y guardar el `.txt` resultante.
