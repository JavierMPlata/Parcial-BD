# Módulo de Carga (Load)

## Descripción General

El módulo `Load` implementa la fase final del pipeline ETL (Extract, Transform, Load), siendo responsable de persistir tanto los datos procesados como las visualizaciones generadas en sus destinos correspondientes. Este módulo garantiza que toda la información analizada esté disponible para consultas futuras y presentaciones.

## Estructura del Módulo

El módulo Load está compuesto por dos clases principales:

### 1. **StockLoad (Loader)** - Carga de Datos
### 2. **GraphicsLoad** - Carga de Visualizaciones

---

## Clase Loader (StockLoad)

### Propósito
La clase `Loader` se encarga de persistir los datos limpios y transformados en diferentes formatos de almacenamiento, proporcionando flexibilidad en las opciones de destino.

### Dependencias
```python
from Config.Config import Config
import sqlite3
```

### Constructor

#### `__init__(self, df)`
**Descripción**: Inicializa el loader con un DataFrame procesado.

**Parámetros**:
- `df` (pandas.DataFrame): DataFrame con los datos limpios y transformados

**Funcionalidad**:
- Almacena la referencia al DataFrame en `self.df`
- Prepara el objeto para operaciones de carga

### Métodos de Persistencia

#### `to_csv(self, output_path)`
**Descripción**: Exporta los datos procesados a un archivo CSV.

**Parámetros**:
- `output_path` (str): Ruta completa donde guardar el archivo CSV

**Funcionalidad**:
- Utiliza `pandas.to_csv()` con `index=False`
- Incluye manejo de errores con try-catch
- Proporciona feedback de éxito/error

**Ejemplo de uso**:
```python
loader = Loader(dataframe_limpio)
loader.to_csv('Files/datos_procesados.csv')
```

#### `to_sqlite(self, db_path=None, table_name=None)`
**Descripción**: Guarda los datos en una base de datos SQLite.

**Parámetros**:
- `db_path` (str, optional): Ruta de la base de datos (default: Config.SQLITE_DB_PATH)
- `table_name` (str, optional): Nombre de la tabla (default: Config.SQLITE_TABLE)

**Funcionalidad**:
- Utiliza configuraciones por defecto del módulo Config
- Reemplaza la tabla existente (`if_exists='replace'`)
- Manejo automático de conexiones (apertura y cierre)
- Gestión de errores con feedback detallado

**Ejemplo de uso**:
```python
loader = Loader(dataframe_limpio)
loader.to_sqlite()  # Usa configuración por defecto
loader.to_sqlite('custom_db.db', 'custom_table')  # Configuración personalizada
```

---

## Clase GraphicsLoad

### Propósito
La clase `GraphicsLoad` gestiona la persistencia de todas las visualizaciones generadas, organizando las gráficas en un sistema de archivos estructurado con estándares de calidad configurables.

### Dependencias
```python
import os
import matplotlib.pyplot as plt
from datetime import datetime
from Config.Config import Config
```

### Constructor

#### `__init__(self)`
**Descripción**: Inicializa el sistema de guardado de gráficas con configuraciones predefinidas.

**Funcionalidad**:
- Carga configuraciones desde Config (ruta, DPI, formato)
- Crea automáticamente el directorio de salida
- Inicializa atributos de configuración

**Atributos inicializados**:
- `self.output_path`: Directorio de salida (Config.GRAPHICS_OUTPUT_PATH)
- `self.dpi`: Resolución de gráficas (Config.GRAPHICS_DPI)
- `self.format`: Formato de archivo (Config.GRAPHICS_FORMAT)

### Métodos de Gestión de Directorios

#### `ensure_output_directory(self)`
**Descripción**: Crea el directorio de salida si no existe.

**Funcionalidad**:
- Verifica existencia del directorio
- Crea directorios faltantes recursivamente
- Proporciona feedback visual con checkmarks

### Métodos de Persistencia de Gráficas

#### `save_figure(self, figure, filename, subfolder=None)`
**Descripción**: Guarda una figura individual con configuraciones optimizadas.

**Parámetros**:
- `figure` (matplotlib.figure.Figure): Figura a guardar
- `filename` (str): Nombre base del archivo (sin extensión)
- `subfolder` (str, optional): Subcarpeta para organización

**Características Avanzadas**:
- **Timestamps únicos**: Evita sobrescribir archivos existentes
- **Calidad optimizada**: `bbox_inches='tight'`, `facecolor='white'`
- **Gestión de memoria**: Cierra figuras automáticamente
- **Organización**: Soporte para subcarpetas
- **Manejo de errores**: Try-catch con feedback detallado

**Retorna**: Ruta completa del archivo guardado o None en caso de error

**Ejemplo de uso**:
```python
graphics_loader = GraphicsLoad()
fig, ax = plt.subplots()
# ... crear gráfica ...
ruta_guardada = graphics_loader.save_figure(fig, "mi_grafica", "analisis_temporal")
```

#### `save_all_graphics(self, graphics_transformer)`
**Descripción**: Genera y guarda automáticamente todas las visualizaciones del análisis.

**Parámetros**:
- `graphics_transformer` (GraphicsTransform): Instancia del transformador de gráficas

**Gráficas Generadas**:
1. **Distribución de Sentimientos** (`01_distribucion_sentimientos`)
2. **Timeline de Sentimientos** (`02_timeline_sentimientos`)
3. **Sentimientos por Día** (`03_sentimientos_por_dia`)
4. **Análisis de Titulares** (`04_analisis_titulares`)
5. **Análisis Avanzado** (`05_analisis_avanzado`)

**Características**:
- **Numeración secuencial**: Nombres ordenados para organización
- **Manejo individual de errores**: Fallos aislados no detienen el proceso
- **Feedback completo**: Progreso y resultados detallados
- **Retorno estructurado**: Diccionario con todas las rutas guardadas

**Retorna**: Dict con nombres de gráficas y rutas guardadas

**Ejemplo de uso**:
```python
graphics_loader = GraphicsLoad()
transformer = GraphicsTransform(datos)
rutas_guardadas = graphics_loader.save_all_graphics(transformer)
```

### Métodos de Consulta

#### `get_graphics_summary(self)`
**Descripción**: Proporciona información sobre las gráficas existentes en el directorio.

**Funcionalidad**:
- Lista archivos con el formato configurado
- Cuenta total de archivos
- Ordena listado alfabéticamente

**Retorna**: Dict con información del directorio
```python
{
    "total_files": 5,
    "files": ["01_distribucion_sentimientos_20241014_143022.png", ...],
    "directory": "Graphics"
}
```

## Configuraciones Técnicas

### Estándares de Calidad
Basándose en la configuración del módulo Config:
- **Resolución**: 300 DPI (calidad de impresión)
- **Formato**: PNG (sin pérdida de calidad)
- **Tamaño**: 12x8 pulgadas (Config.FIGURE_SIZE)
- **Optimizaciones**: Bordes ajustados, fondo blanco

### Organización de Archivos
```
Graphics/
├── 01_distribucion_sentimientos_20241014_143022.png
├── 02_timeline_sentimientos_20241014_143025.png
├── 03_sentimientos_por_dia_20241014_143028.png
├── 04_analisis_titulares_20241014_143031.png
├── 05_analisis_avanzado_20241014_143034.png
└── subcarpetas/
    └── analisis_personalizado_20241014_143040.png
```

## Flujo de Trabajo Completo

### 1. Carga de Datos Procesados
```python
from Load.StockLoad import Loader
from Load.GraphicsLoad import GraphicsLoad

# Cargar datos procesados
loader = Loader(dataframe_procesado)
loader.to_csv('Files/stock_senti_analysis_limpio.csv')
loader.to_sqlite()  # Usa configuración por defecto
```

### 2. Carga de Visualizaciones
```python
# Generar y guardar todas las gráficas
graphics_loader = GraphicsLoad()
transformer = GraphicsTransform(dataframe_procesado)
archivos_guardados = graphics_loader.save_all_graphics(transformer)

# Resumen de gráficas generadas
resumen = graphics_loader.get_graphics_summary()
print(f"Total de gráficas: {resumen['total_files']}")
```

## Ventajas del Sistema de Carga

### 1. **Flexibilidad de Destinos**
- Múltiples formatos de salida (CSV, SQLite)
- Configuración personalizable de parámetros
- Soporte para destinos adicionales fácilmente extensible

### 2. **Gestión Avanzada de Archivos**
- Prevención de sobrescritura con timestamps
- Organización automática en directorios
- Manejo robusto de errores

### 3. **Calidad Garantizada**
- Configuraciones optimizadas para presentaciones
- Estándares consistentes en todas las gráficas
- Gestión eficiente de memoria

### 4. **Monitoreo y Feedback**
- Mensajes detallados de progreso
- Identificación clara de éxitos y errores
- Resúmenes de operaciones realizadas

## Extensibilidad del Módulo

### Nuevos Destinos de Datos
```python
def to_json(self, output_path):
    """Exportar a formato JSON"""
    self.df.to_json(output_path, orient='records', indent=2)

def to_parquet(self, output_path):
    """Exportar a formato Parquet"""
    self.df.to_parquet(output_path, index=False)

def to_database(self, connection_string, table_name):
    """Cargar a base de datos externa"""
    # Implementación para PostgreSQL, MySQL, etc.
```

### Nuevos Formatos de Gráficas
```python
def save_interactive_html(self, plotly_figure, filename):
    """Guardar gráficas interactivas Plotly"""
    # Implementación para gráficas web interactivas

def save_vector_format(self, figure, filename):
    """Guardar en formato vectorial (SVG, PDF)"""
    # Para gráficas escalables
```

## Consideraciones de Rendimiento

### Optimizaciones Implementadas
- Cierre automático de figuras para liberar memoria
- Manejo eficiente de conexiones de base de datos
- Procesamiento por lotes de múltiples gráficas

### Recomendaciones para Datasets Grandes
- Considerar chunking para exports CSV muy grandes
- Indexación apropiada en tablas SQLite
- Compresión de gráficas para almacenamiento optimizado

## Integración con el Pipeline ETL

El módulo Load completa el pipeline ETL integrándose con:
- **Extract**: Recibe datos extraídos
- **Transform**: Procesa datos transformados y genera visualizaciones
- **Config**: Utiliza configuraciones centralizadas
- **Sistema de archivos**: Organiza outputs de manera estructurada