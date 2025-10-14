from Extract.StockExtract import StockExtract
from Config.Config import Config

# Extracción de datos
print("EXTRAYENDO DATOS...")
print("=" * 50)
response1 = StockExtract(Config.INPUT_PATH)
response1.queries()

print("Primeras 15 filas de los datos extraídos:")
print(response1.response())