# Módulo de Transformación (Transform)

## Descripción General

El módulo `Transform` implementa la fase de transformación del pipeline ETL (Extract, Transform, Load), siendo responsable tanto de la limpieza y procesamiento de datos como de la generación de visualizaciones avanzadas. Este módulo garantiza la calidad de los datos y proporciona insights visuales comprehensivos del análisis de sentimientos financieros.

## Estructura del Módulo

El módulo Transform está compuesto por dos clases principales:

### 1. **StockTransform** - Procesamiento y Limpieza de Datos
### 2. **GraphicsTransform** - Generación de Visualizaciones

---

## Clase StockTransform

### Propósito
La clase `StockTransform` es el núcleo del procesamiento de datos, implementando técnicas avanzadas de limpieza, imputación y feature engineering para garantizar la calidad y completitud del dataset de análisis de sentimientos.

### Dependencias
```python
import pandas as pd
import numpy as np
from datetime import datetime
import re
```

### Constructor

#### `__init__(self, df)`
**Descripción**: Inicializa el transformador con el DataFrame original.

**Parámetros**:
- `df` (pandas.DataFrame): DataFrame extraído con datos en bruto

**Funcionalidad**:
- Crea una copia del DataFrame para preservar los datos originales
- Inicializa atributos de control (`df_clean`, `original_nulls`, `cleaning_results`)

### Método Principal de Limpieza

#### `clean_data(self)`
**Descripción**: Pipeline completo de limpieza de datos con reportes detallados.

**Proceso de Limpieza (6 fases)**:

1. **Análisis Inicial** - `_analyze_null_values()`
2. **Limpieza de Fechas** - `_clean_dates()`
3. **Validación de Etiquetas** - `_clean_labels()`
4. **Imputación de Texto** - `_clean_text_columns()`
5. **Filtrado de Calidad** - `_remove_rows_with_too_many_nulls()`
6. **Ingeniería de Features** - `_create_features()`

**Retorna**: DataFrame limpio y procesado

**Características**:
- Reportes detallados en tiempo real con emojis
- Análisis estadístico de cada fase
- Preservación de datos originales
- Estrategias de imputación inteligente

### Métodos de Análisis y Limpieza

#### `_analyze_null_values(self)`
**Descripción**: Análisis exhaustivo de valores faltantes con estrategias de imputación.

**Funcionalidades**:
- Conteo detallado de nulos por columna
- Análisis específico de columnas de titulares (Top1-Top25)
- Cálculo de porcentajes de completitud
- Definición de estrategias de imputación

**Output**: Reporte detallado con estadísticas de calidad de datos

#### `_clean_dates(self)`
**Descripción**: Procesamiento y validación de fechas con extracción de componentes temporales.

**Transformaciones**:
- Conversión a `datetime` con manejo de errores
- Extracción de componentes: `Year`, `Month`, `DayOfWeek`
- Eliminación de fechas inválidas
- Validación de rangos temporales

**Features creadas**:
- `Year`: Año (int)
- `Month`: Mes (1-12)
- `DayOfWeek`: Día de la semana (0=Lunes, 6=Domingo)

#### `_clean_labels(self)`
**Descripción**: Validación y normalización de etiquetas de sentimiento.

**Validaciones**:
- Verificación de valores binarios (0, 1)
- Conversión a tipo entero
- Eliminación de etiquetas inválidas
- Análisis de distribución de sentimientos

#### `_clean_text_columns(self)` 🌟
**Descripción**: Sistema avanzado de imputación de texto para columnas de titulares.

**Estrategia de Imputación Inteligente**:
1. **Análisis por Columna**: Identificación de nulos por columna Top1-Top25
2. **Cálculo de Moda**: Valor más frecuente por columna
3. **Imputación Selectiva**: 
   - Moda si está disponible
   - Valor genérico "Sin titular disponible" como fallback
4. **Normalización**: Limpieza de espacios y caracteres especiales

**Características Avanzadas**:
- Reporte detallado de imputación por columna
- Manejo de múltiples tipos de valores nulos
- Preservación de la distribución original de datos
- Validación de completitud post-imputación

#### `_remove_rows_with_too_many_nulls(self)`
**Descripción**: Filtrado de calidad basado en la disponibilidad de titulares por día.

**Criterios de Filtrado**:
- Umbral mínimo: 15 titulares válidos por día
- Análisis estadístico de distribución
- Reporte de filas removidas con justificación

#### `_create_features(self)` 🔧
**Descripción**: Ingeniería de features avanzada para análisis temporal y textual.

**Features Creadas**:

1. **HeadlineCount**: Número de titulares válidos por día
2. **AvgHeadlineLength**: Longitud promedio de caracteres por titular
3. **AllHeadlines**: Concatenación de todos los titulares del día
4. **DayName**: Nombre del día en español
5. **Quarter**: Trimestre del año (1-4)
6. **IsWeekend**: Indicador binario de fin de semana

**Funciones Auxiliares**:
- `count_valid_headlines()`: Conteo inteligente excluyendo valores vacíos
- `avg_headline_length()`: Cálculo robusto de longitud promedio
- `combine_headlines()`: Concatenación con separador personalizado

### Métodos de Validación y Reporte

#### `_final_quality_check(self)`
**Descripción**: Verificación exhaustiva de calidad post-procesamiento.

**Validaciones**:
- Ausencia de nulos en columnas críticas
- Consistencia de fechas (no duplicados)
- Validez de etiquetas de sentimiento
- Análisis de titulares vacíos

#### `_show_cleaning_summary(self)`
**Descripción**: Reporte completo de impacto de limpieza con métricas de calidad.

**Métricas Reportadas**:
- Completitud original vs final
- Columnas procesadas y métodos utilizados
- Valores imputados por columna
- Mejora en calidad de datos (%)

### Métodos de Consulta

#### `get_data_summary(self)`
**Descripción**: Resumen estructurado de datos procesados en formato JSON-like.

**Secciones del Resumen**:
- **Resumen General**: Registros totales, período temporal, años incluidos
- **Análisis de Sentimiento**: Distribución negativo/positivo con porcentajes
- **Análisis de Titulares**: Promedios y totales de contenido textual
- **Distribución Temporal**: Patrones por años y días de semana
- **Columnas Creadas**: Lista de features de ingeniería

#### `print_detailed_summary(self)`
**Descripción**: Impresión formateada del resumen detallado con estructura visual.

---

## Clase GraphicsTransform

### Propósito
La clase `GraphicsTransform` genera visualizaciones avanzadas y análisis gráfico multi-dimensional de los datos procesados, proporcionando insights visuales para análisis exploratorio y presentaciones.

### Dependencias
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import warnings
```

### Constructor

#### `__init__(self, df)`
**Descripción**: Inicializa el generador de gráficas con datos procesados.

**Funcionalidad**:
- Copia del DataFrame para preservar datos originales
- Preparación automática de datos con `prepare_data()`

#### `prepare_data(self)`
**Descripción**: Preparación específica para visualizaciones.

**Transformaciones**:
- Conversión de fechas a datetime
- Creación de etiquetas de sentimiento legibles
- Configuración de advertencias

### Catálogo de Visualizaciones

#### 1. `create_sentiment_distribution(self)` 📊
**Descripción**: Visualización dual de la distribución de sentimientos.

**Componentes**:
- **Gráfico de Barras**: Frecuencias absolutas con etiquetas numéricas
- **Gráfico Circular**: Proporciones relativas con porcentajes

**Características**:
- Paleta de colores consistente (rojo/azul)
- Etiquetas automáticas en barras
- Diseño lado a lado (1x2 subplot)

#### 2. `create_sentiment_timeline(self)` 📈
**Descripción**: Evolución temporal del sentimiento con análisis de tendencias.

**Características**:
- Línea temporal con marcadores
- Línea de referencia de neutralidad (50%)
- Formato de fechas optimizado
- Análisis de tendencias históricas

#### 3. `create_sentiment_by_weekday(self)` 📅
**Descripción**: Análisis de patrones semanales de sentimiento.

**Funcionalidades**:
- Ordenación cronológica de días
- Paleta de colores degradada (Viridis)
- Identificación de "efectos" (lunes negativo, viernes positivo)
- Línea de neutralidad como referencia

#### 4. `create_headline_analysis(self)` 📰
**Descripción**: Panel de análisis multivariado en formato 2x2.

**Subgráficas**:
1. **Histograma de Longitudes**: Distribución de caracteres por titular
2. **Longitud por Sentimiento**: Comparación de longitudes promedio
3. **Sentimiento por Mes**: Tendencias estacionales con línea continua
4. **Heatmap Bidimensional**: Sentimiento por mes y día de semana

**Características Avanzadas**:
- Análisis de correlación texto-sentimiento
- Identificación de patrones estacionales
- Visualización de interacciones temporales complejas

#### 5. `create_advanced_analysis(self)` 🔬
**Descripción**: Análisis estadístico avanzado con múltiples perspectivas.

**Componentes Analíticos**:

1. **Box Plot Comparativo**: 
   - Distribuciones de longitud por sentimiento
   - Identificación de outliers y cuartiles
   - Comparación estadística visual

2. **Análisis de Correlaciones**:
   - Variables numéricas vs sentimiento
   - Gráfico horizontal de barras con código de colores
   - Identificación de predictores potenciales

3. **Tendencias Anuales**:
   - Análisis histórico cuando hay múltiples años
   - Detección automática de disponibilidad de datos
   - Fallback informativo para datos limitados

4. **Distribución Trimestral**:
   - Análisis estacional con barras agrupadas
   - Comparación sentimiento positivo vs negativo
   - Identificación de ciclos anuales

## Configuraciones Técnicas de Visualización

### Estándares de Calidad
- **Resolución**: Configurada desde Config (300 DPI)
- **Tamaños**: Figuras optimizadas por tipo de análisis
- **Paletas**: Consistentes y accesibles
- **Layouts**: `tight_layout()` automático

### Características Avanzadas
- Supresión de warnings automática
- Manejo robusto de datos faltantes
- Adaptación automática a diferentes tamaños de dataset
- Etiquetado inteligente y rotación de texto

## Flujo de Trabajo Integrado

### 1. Transformación de Datos
```python
from Transform.StockTransform import StockTransform

# Procesar datos en bruto
transformer = StockTransform(raw_dataframe)
clean_data = transformer.clean_data()

# Obtener resumen detallado
transformer.print_detailed_summary()
```

### 2. Generación de Visualizaciones
```python
from Transform.GraphicsTransform import GraphicsTransform

# Crear visualizaciones
graphics = GraphicsTransform(clean_data)

# Generar gráficas específicas
fig1 = graphics.create_sentiment_distribution()
fig2 = graphics.create_sentiment_timeline()
fig3 = graphics.create_headline_analysis()
fig4 = graphics.create_advanced_analysis()
```

### 3. Pipeline Completo
```python
# Pipeline ETL completo
extractor = StockExtract(Config.INPUT_PATH)
extractor.queries()

transformer = StockTransform(extractor.data)
clean_data = transformer.clean_data()

graphics = GraphicsTransform(clean_data)
loader = GraphicsLoad()
loader.save_all_graphics(graphics)
```

## Ventajas del Sistema de Transformación

### 1. **Robustez en Limpieza**
- Manejo inteligente de múltiples tipos de valores faltantes
- Estrategias de imputación adaptativas
- Validación exhaustiva de calidad

### 2. **Ingeniería de Features Avanzada**
- Creación automática de características temporales
- Análisis textual básico integrado
- Features específicas para análisis de sentimientos

### 3. **Visualizaciones Comprehensivas**
- 5 tipos de análisis visual diferentes
- Desde análisis básico hasta estadística avanzada
- Optimizado para presentaciones y reportes

### 4. **Reportería Detallada**
- Tracking completo del proceso de limpieza
- Métricas de calidad cuantificables
- Feedback visual en tiempo real

### 5. **Escalabilidad y Mantenibilidad**
- Código modular y bien estructurado
- Configuraciones externalizadas
- Fácil extensión para nuevos análisis

## Extensibilidad del Módulo

### Nuevas Transformaciones de Datos
```python
def _advanced_text_processing(self):
    """Análisis de texto avanzado con NLP"""
    # Sentiment scoring granular
    # Named entity recognition
    # Keyword extraction
    
def _anomaly_detection(self):
    """Detección de anomalías en patrones temporales"""
    # Outlier detection
    # Seasonal decomposition
    # Trend analysis

def _feature_selection(self):
    """Selección automática de features relevantes"""
    # Correlation analysis
    # Feature importance scoring
    # Dimensionality reduction
```

### Nuevas Visualizaciones
```python
def create_interactive_dashboard(self):
    """Dashboard interactivo con Plotly"""
    # Gráficas interactivas
    # Filtros dinámicos
    # Exportación web

def create_predictive_analysis(self):
    """Análisis predictivo visual"""
    # Forecasting de sentimientos
    # Intervalos de confianza
    # Model evaluation plots

def create_comparative_analysis(self):
    """Análisis comparativo entre períodos"""
    # Year-over-year comparisons
    # Seasonal adjustments
    # Statistical significance tests
```

## Consideraciones de Rendimiento

### Optimizaciones Implementadas
- Procesamiento vectorizado con pandas/numpy
- Gestión eficiente de memoria con copias selectivas
- Reutilización de cálculos intermedios

### Recomendaciones para Datasets Grandes
- Procesamiento por chunks para datasets masivos
- Paralelización de limpieza de columnas de texto
- Caching de resultados intermedios para visualizaciones

## Integración con el Pipeline ETL

El módulo Transform actúa como el núcleo del pipeline:

- **Input**: Datos en bruto del módulo Extract
- **Processing**: Limpieza, validación y feature engineering
- **Output**: Datos limpios para Load + Visualizaciones para presentación
- **Configuration**: Utiliza parámetros del módulo Config
- **Monitoring**: Reportes detallados para auditoría de calidad

El módulo garantiza que los datos fluyan con calidad consistente hacia las fases posteriores del pipeline, mientras proporciona insights visuales inmediatos para la toma de decisiones.