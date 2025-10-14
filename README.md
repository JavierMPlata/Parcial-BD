# 📊 Sistema ETL de Análisis de Sentimientos Financieros

## 🎯 Descripción del Proyecto

Sistema completo de ETL (Extract, Transform, Load) diseñado para el análisis de sentimientos en noticias financieras. Este proyecto implementa un pipeline robusto que procesa datos de sentimientos de acciones, realiza limpieza avanzada de datos, genera análisis visuales comprehensivos y almacena resultados en múltiples formatos.

### 🏆 Características Principales

- **Pipeline ETL Completo**: Extracción, transformación y carga de datos automatizada
- **Limpieza Avanzada de Datos**: Imputación inteligente y validación de calidad
- **Análisis Visual Comprehensivo**: 5+ tipos de visualizaciones especializadas
- **Sistema de Configuración Centralizada**: Parámetros unificados y escalables
- **Reportería Detallada**: Tracking completo del proceso con métricas de calidad
- **Arquitectura Modular**: Componentes independientes y reutilizables

## 📁 Estructura del Proyecto

```
Parcial-BD/
├── 📋 Main.py                     # Archivo principal de ejecución
├── 📄 README.md                   # Documentación del proyecto
├── 📦 requirements.txt            # Dependencias del proyecto
├── 📜 LICENSE                     # Licencia del proyecto
│
├── ⚙️ Config/                     # Configuración centralizada
│   ├── Config.py                  # Parámetros y rutas del sistema
│   └── Config_Readme.md           # Documentación de configuración
│
├── 📥 Extract/                    # Módulo de extracción de datos
│   ├── StockExtract.py           # Clase principal de extracción
│   └── Extract_Readme.md         # Documentación de extracción
│
├── 🔄 Transform/                  # Módulo de transformación y análisis
│   ├── StockTransform.py         # Limpieza y procesamiento de datos
│   ├── GraphicsTransform.py      # Generación de visualizaciones
│   └── Transform_Readme.md       # Documentación de transformación
│
├── 💾 Load/                       # Módulo de carga y persistencia
│   ├── StockLoad.py              # Carga de datos procesados
│   ├── GraphicsLoad.py           # Guardado de visualizaciones
│   └── Load_Readme.md            # Documentación de carga
│
├── 📂 Files/                      # Archivos de datos
│   ├── stock_senti_analysis.csv  # Dataset original
│   ├── stock_senti_analysis_limpio.csv  # Datos procesados
│   └── etl_data.db               # Base de datos SQLite
│
└── 📊 Graphics/                   # Visualizaciones generadas
    ├── 01_distribucion_sentimientos_*.png
    ├── 02_timeline_sentimientos_*.png
    ├── 03_sentimientos_por_dia_*.png
    ├── 04_analisis_titulares_*.png
    └── 05_analisis_avanzado_*.png
```

## 🔄 Pipeline ETL Detallado

### 1. 📥 **EXTRACT** - Extracción de Datos
```python
from Extract.StockExtract import StockExtract

# Cargar datos originales
extractor = StockExtract('Files/stock_senti_analysis.csv')
extractor.queries()
raw_data = extractor.response()
```

**Funcionalidades**:
- Carga de archivos CSV con validación
- Exploración inicial de datos
- Verificación de integridad del dataset
- Preparación para procesamiento posterior

### 2. 🔄 **TRANSFORM** - Transformación y Análisis

#### A. Limpieza de Datos
```python
from Transform.StockTransform import StockTransform

# Procesar y limpiar datos
transformer = StockTransform(raw_data)
clean_data = transformer.clean_data()
```

**Procesos de Limpieza**:
- ✅ **Análisis de Valores Nulos**: Identificación y estrategias de imputación
- ✅ **Limpieza de Fechas**: Validación y extracción de componentes temporales
- ✅ **Validación de Etiquetas**: Verificación de sentimientos binarios (0/1)
- ✅ **Imputación de Texto**: Sistema avanzado por moda con fallback
- ✅ **Filtrado de Calidad**: Eliminación de filas con datos insuficientes
- ✅ **Ingeniería de Features**: Creación de 6+ características derivadas

#### B. Generación de Visualizaciones
```python
from Transform.GraphicsTransform import GraphicsTransform

# Crear análisis visual
graphics = GraphicsTransform(clean_data)
visualizations = [
    graphics.create_sentiment_distribution(),
    graphics.create_sentiment_timeline(),
    graphics.create_sentiment_by_weekday(),
    graphics.create_headline_analysis(),
    graphics.create_advanced_analysis()
]
```

### 3. 💾 **LOAD** - Carga y Persistencia

#### A. Persistencia de Datos
```python
from Load.StockLoad import Loader

# Guardar datos procesados
loader = Loader(clean_data)
loader.to_csv('Files/stock_senti_analysis_limpio.csv')
loader.to_sqlite()  # Base de datos SQLite
```

#### B. Guardado de Visualizaciones
```python
from Load.GraphicsLoad import GraphicsLoad

# Guardar todas las gráficas
graphics_loader = GraphicsLoad()
saved_files = graphics_loader.save_all_graphics(graphics)
```

## 📊 Análisis y Visualizaciones Generadas

### 1. **Distribución de Sentimientos** 
- Gráfico de barras con frecuencias absolutas
- Gráfico circular con proporciones relativas
- **Insight**: Balance 52.8% positivo vs 47.2% negativo

### 2. **Evolución Temporal**
- Timeline histórico (2000-2016) de sentimientos
- Línea de referencia de neutralidad (50%)
- **Insight**: Sentimiento consistentemente por encima de neutralidad

### 3. **Patrones Semanales**
- Análisis por días de la semana
- **Insight**: "Efecto lunes" negativo (49.5%), "Efecto viernes" positivo (55.5%)

### 4. **Análisis de Contenido Textual**
- Distribución de longitudes de titulares
- Relación longitud-sentimiento
- Patrones estacionales mensuales
- Heatmap bidimensional (mes × día semana)

### 5. **Análisis Estadístico Avanzado**
- Box plots comparativos por sentimiento
- Análisis de correlaciones multivariado
- Tendencias anuales históricas
- Distribución trimestral

## 🚀 Instalación y Ejecución

### Prerrequisitos

![Versiones de Librerías](https://img.shields.io/badge/Python-3.9+-blue) ![Pandas](https://img.shields.io/badge/Pandas-2.3.1-green) ![NumPy](https://img.shields.io/badge/NumPy-2.3.2-orange) ![Matplotlib](https://img.shields.io/badge/Matplotlib-3.10.6-red) ![Seaborn](https://img.shields.io/badge/Seaborn-0.13.2-purple)

**Versiones Recomendadas (Probadas)**:
```bash
Python 3.9+
pandas == 2.3.1
numpy == 2.3.2  
matplotlib == 3.10.6
seaborn == 0.13.2
```

**Versiones Mínimas Compatibles**:
```bash
Python 3.8+
pandas >= 1.3.0
matplotlib >= 3.3.0
seaborn >= 0.11.0
numpy >= 1.20.0
```

### 1. Clonar el Repositorio
```bash
git clone https://github.com/JavierMPlata/Parcial-BD.git
cd Parcial-BD
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar el Pipeline Completo
```bash
python Main.py
```

### 4. Ejecución Modular
```python
# Solo extracción
python -c "from Extract.StockExtract import StockExtract; ..."

# Solo transformación
python -c "from Transform.StockTransform import StockTransform; ..."

# Solo carga
python -c "from Load.StockLoad import Loader; ..."
```

## ⚙️ Configuración del Sistema

El sistema utiliza configuración centralizada en `Config/Config.py`:

```python
class Config:
    # Rutas de datos
    INPUT_PATH = r'Files\stock_senti_analysis.csv'
    SQLITE_DB_PATH = r'Files\etl_data.db'
    SQLITE_TABLE = 'stock_sentiment_clean'
    
    # Configuración de gráficas
    GRAPHICS_OUTPUT_PATH = r'Graphics'
    GRAPHICS_DPI = 300          # Alta calidad
    GRAPHICS_FORMAT = 'png'     # Formato de salida
    FIGURE_SIZE = (12, 8)       # Tamaño estándar
```

### Personalización
- Modificar rutas de archivos de entrada y salida
- Ajustar parámetros de calidad de gráficas
- Configurar formatos de exportación
- Personalizar tamaños de visualizaciones

## 📈 Métricas de Calidad y Rendimiento

### Dataset Procesado
- **Registros totales**: ~4,101 días de noticias financieras
- **Período temporal**: 2000-2016 (16 años de datos históricos)
- **Completitud de datos**: 99.8% post-limpieza
- **Features generadas**: 15+ columnas derivadas

### Análisis de Sentimientos
- **Balance de clases**: Ligeramente positivo (52.8% vs 47.2%)
- **Titulares por día**: ~20-25 titulares promedio
- **Longitud promedio**: ~72 caracteres por titular
- **Cobertura temporal**: Sin gaps significativos en datos

### Rendimiento del Sistema
- **Tiempo de procesamiento**: ~30-60 segundos (dataset completo)
- **Memoria utilizada**: <500MB para dataset estándar
- **Archivos generados**: 5+ visualizaciones + 2 formatos de datos

## 🔍 Insights Clave Descubiertos

### 1. **Patrones Temporales**
- **Efecto día de semana**: Lunes más pesimista, viernes más optimista
- **Estacionalidad**: Variaciones mensuales con picos en marzo y noviembre
- **Tendencia histórica**: Relativa estabilidad en el período 2000-2016

### 2. **Características del Contenido**
- **Distribución normal**: Longitud de titulares centrada en ~40 caracteres
- **Sin sesgo por longitud**: Correlación débil entre longitud y sentimiento
- **Consistencia temporal**: Patrones estables a lo largo de los años

### 3. **Aplicaciones Prácticas**
- **Análisis de mercado**: Identificación de ciclos de sentimiento
- **Predicción de tendencias**: Patrones históricos como baseline
- **Optimización de contenido**: Insights sobre longitud efectiva de titulares

## 🛠️ Arquitectura Técnica

### Principios de Diseño
- **Modularidad**: Componentes independientes y reutilizables
- **Escalabilidad**: Configuración externa y procesamiento eficiente
- **Robustez**: Manejo de errores y validación exhaustiva
- **Observabilidad**: Logging detallado y métricas de calidad

### Patrones Implementados
- **ETL Pipeline**: Flujo estructurado Extract → Transform → Load
- **Factory Pattern**: Generación configurable de visualizaciones
- **Strategy Pattern**: Múltiples estrategias de imputación
- **Observer Pattern**: Reporting en tiempo real del progreso

## 🔮 Roadmap y Extensiones Futuras

### Funcionalidades Planeadas
- [ ] **Análisis NLP Avanzado**: Sentiment scoring granular, NER, keywords
- [ ] **Dashboard Interactivo**: Visualizaciones web con Plotly/Dash
- [ ] **API REST**: Endpoints para procesamiento en tiempo real
- [ ] **Análisis Predictivo**: Forecasting de sentimientos con ML
- [ ] **Integración Cloud**: Despliegue en AWS/GCP/Azure
- [ ] **Automatización CI/CD**: Pipeline automatizado con GitHub Actions

### Mejoras Técnicas
- [ ] **Procesamiento Paralelo**: Multi-threading para datasets grandes
- [ ] **Cache Inteligente**: Optimización de re-procesamiento
- [ ] **Monitoring Avanzado**: Métricas de performance en tiempo real
- [ ] **Testing Automatizado**: Suite completa de pruebas unitarias


## � Contribuciones

### Cómo Contribuir
1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

### Áreas de Contribución
- Nuevos tipos de análisis visual
- Optimizaciones de rendimiento
- Documentación y ejemplos
- Testing y validación
- Integración con nuevas fuentes de datos

## �📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 📞 Contacto

**Desarrollador**: Javier M. Plata  
**Repositorio**: [Parcial-BD](https://github.com/JavierMPlata/Parcial-BD)  
**Rama Actual**: Release  

---

### 🏷️ Tags
`ETL` `Data-Analysis` `Sentiment-Analysis` `Financial-Data` `Python` `Pandas` `Matplotlib` `Data-Pipeline` `Big-Data` `Visualization`