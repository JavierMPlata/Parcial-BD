# Módulo de Extracción (Extract)

## Descripción General

El módulo `Extract` es responsable de la fase de extracción en el proceso ETL (Extract, Transform, Load). Este módulo se encarga de leer y cargar los datos originales desde archivos CSV, proporcionando las funcionalidades básicas para acceder a la información del dataset de análisis de sentimientos de acciones.

## Clase StockExtract

### Propósito
La clase `StockExtract` maneja la extracción de datos desde archivos CSV y proporciona métodos para explorar y acceder a la información contenida en el dataset.

### Dependencias
```python
import requests      # Para futuras implementaciones de APIs web
import pandas as pd  # Para manipulación y análisis de datos
import numpy         # Para operaciones numéricas avanzadas
```

## Métodos de la Clase

### `__init__(self, csv_path)`

**Descripción**: Constructor de la clase que inicializa el objeto con la ruta del archivo CSV.

**Parámetros**:
- `csv_path` (str): Ruta del archivo CSV que contiene los datos a extraer.

**Funcionalidad**:
- Almacena la ruta del archivo CSV en el atributo `self.csv`
- Prepara el objeto para las operaciones de extracción posteriores

**Ejemplo de uso**:
```python
extractor = StockExtract('Files/stock_senti_analysis.csv')
```

### `queries(self)`

**Descripción**: Método principal de extracción que carga los datos del archivo CSV y genera información básica sobre el dataset.

**Funcionalidad**:
- Utiliza `pandas.read_csv()` para cargar los datos del archivo especificado
- Almacena los datos en el atributo `self.data`
- Genera información del dataset usando `info()` y la almacena en `self.data_info`

**Atributos generados**:
- `self.data`: DataFrame de pandas con todos los datos del CSV
- `self.data_info`: Información detallada sobre la estructura del dataset (tipos de datos, valores nulos, memoria utilizada)

**Ejemplo de uso**:
```python
extractor = StockExtract('Files/stock_senti_analysis.csv')
extractor.queries()  # Carga los datos y genera información
```

### `response(self)`

**Descripción**: Método que retorna una muestra de los datos extraídos para visualización inicial.

**Retorna**:
- DataFrame de pandas con las primeras 15 filas del dataset

**Funcionalidad**:
- Proporciona una vista previa de los datos cargados
- Útil para verificación inicial y exploración rápida del contenido
- Facilita la validación de que la extracción se realizó correctamente

**Ejemplo de uso**:
```python
extractor = StockExtract('Files/stock_senti_analysis.csv')
extractor.queries()
preview_data = extractor.response()
print(preview_data)
```

## Flujo de Trabajo Típico

### 1. Inicialización
```python
from Extract.StockExtract import StockExtract

# Crear instancia del extractor
extractor = StockExtract('Files/stock_senti_analysis.csv')
```

### 2. Extracción de Datos
```python
# Cargar datos y generar información
extractor.queries()
```

### 3. Visualización Inicial
```python
# Obtener vista previa de los datos
sample_data = extractor.response()
```

## Características del Módulo

### Ventajas
1. **Simplicidad**: Interfaz clara y fácil de usar
2. **Integración**: Preparado para trabajar con pandas DataFrames
3. **Verificación**: Proporciona métodos para validar la extracción
4. **Extensibilidad**: Estructura preparada para futuras mejoras

### Limitaciones Actuales
1. **Formato único**: Solo maneja archivos CSV
2. **Sin validación**: No incluye verificación de formato o existencia de archivos
3. **Dependencia requests**: Importada pero no utilizada en la versión actual

## Posibles Mejoras Futuras

### 1. Validación de Archivos
```python
def validate_file(self):
    """Verificar que el archivo existe y es accesible"""
    if not os.path.exists(self.csv):
        raise FileNotFoundError(f"Archivo no encontrado: {self.csv}")
```

### 2. Manejo de Errores
```python
def queries(self):
    """Cargar datos con manejo de errores"""
    try:
        self.data = pd.read_csv(self.csv)
        self.data_info = self.data.info()
    except Exception as e:
        print(f"Error al cargar datos: {e}")
        raise
```

### 3. Múltiples Formatos
- Soporte para archivos Excel, JSON, Parquet
- Integración con APIs web (usando requests)
- Conexión a bases de datos

### 4. Configuración Avanzada
- Parámetros de encoding para archivos CSV
- Opciones de separadores personalizados
- Configuración de tipos de datos automática

## Integración con el Sistema ETL

El módulo Extract forma parte del pipeline ETL y se integra con:

- **Config**: Utiliza las rutas definidas en `Config.INPUT_PATH`
- **Transform**: Los datos extraídos (`self.data`) son procesados por el módulo Transform
- **Load**: Los datos transformados son cargados por el módulo Load

## Consideraciones de Rendimiento

- Utiliza pandas para manejo eficiente de datos grandes
- Carga completa en memoria (considerar chunking para datasets muy grandes)
- Información del dataset disponible para optimizaciones futuras