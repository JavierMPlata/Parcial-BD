# Módulo de Configuración (Config)

## Descripción General

El módulo `Config` centraliza todas las configuraciones y parámetros necesarios para el proceso ETL (Extract, Transform, Load) del proyecto de análisis de sentimientos de acciones. Esta clase proporciona un punto único de configuración que facilita el mantenimiento y modificación de rutas y parámetros del sistema.

## Estructura de la Clase Config

### Rutas de Archivos de Datos

#### `INPUT_PATH`
- **Tipo**: `str`
- **Valor**: `r'Files\stock_senti_analysis.csv'`
- **Descripción**: Ruta del archivo CSV de entrada que contiene los datos originales de análisis de sentimientos de acciones.
- **Uso**: Utilizado por el módulo Extract para leer los datos iniciales del dataset.

#### `SQLITE_DB_PATH`
- **Tipo**: `str`
- **Valor**: `r'Files\etl_data.db'`
- **Descripción**: Ruta de la base de datos SQLite donde se almacenarán los datos procesados.
- **Uso**: Utilizado por el módulo Load para crear/conectar con la base de datos de destino.

#### `SQLITE_TABLE`
- **Tipo**: `str`
- **Valor**: `'stock_sentiment_clean'`
- **Descripción**: Nombre de la tabla en la base de datos SQLite donde se insertarán los datos limpios.
- **Uso**: Define la estructura de almacenamiento en la base de datos.

### Configuración de Gráficas

#### `GRAPHICS_OUTPUT_PATH`
- **Tipo**: `str`
- **Valor**: `r'Graphics'`
- **Descripción**: Directorio donde se guardarán todas las visualizaciones generadas por el sistema.
- **Uso**: Utilizado por los módulos de generación de gráficas para definir el directorio de salida.

#### `GRAPHICS_DPI`
- **Tipo**: `int`
- **Valor**: `300`
- **Descripción**: Resolución en DPI (puntos por pulgada) para las gráficas generadas.
- **Uso**: Asegura alta calidad en las visualizaciones exportadas.

#### `GRAPHICS_FORMAT`
- **Tipo**: `str`
- **Valor**: `'png'`
- **Descripción**: Formato de archivo para guardar las gráficas.
- **Uso**: Define el tipo de archivo de imagen para las exportaciones.

#### `FIGURE_SIZE`
- **Tipo**: `tuple`
- **Valor**: `(12, 8)`
- **Descripción**: Tamaño de las figuras en pulgadas (ancho, alto).
- **Uso**: Establece las dimensiones estándar para todas las visualizaciones.

## Uso del Módulo

### Importación
```python
from Config.Config import Config
```

### Acceso a Configuraciones
```python
# Acceder a rutas de archivos
input_file = Config.INPUT_PATH
database_path = Config.SQLITE_DB_PATH
table_name = Config.SQLITE_TABLE

# Acceder a configuraciones de gráficas
output_dir = Config.GRAPHICS_OUTPUT_PATH
dpi = Config.GRAPHICS_DPI
format_type = Config.GRAPHICS_FORMAT
fig_size = Config.FIGURE_SIZE
```

## Ventajas del Sistema de Configuración

1. **Centralización**: Todas las configuraciones están en un solo lugar.
2. **Mantenibilidad**: Fácil modificación de parámetros sin tocar el código principal.
3. **Consistencia**: Garantiza que todos los módulos usen los mismos parámetros.
4. **Escalabilidad**: Fácil adición de nuevas configuraciones según las necesidades del proyecto.

## Modificaciones Futuras

Para agregar nuevas configuraciones:

1. Añadir la nueva variable de clase con su valor correspondiente.
2. Documentar el nuevo parámetro siguiendo el formato establecido.
3. Actualizar los módulos que requieran la nueva configuración.

## Consideraciones de Desarrollo

- Las rutas utilizan raw strings (`r''`) para evitar problemas con caracteres de escape en Windows.
- Los valores están optimizados para el flujo de trabajo del proyecto actual.
- La configuración de gráficas está diseñada para generar visualizaciones de alta calidad para presentaciones y reportes.