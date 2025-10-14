class Config:
    """
    Clase de configuración para rutas y parámetros del ETL.
    """
    INPUT_PATH = r'Files\stock_senti_analysis.csv'
    SQLITE_DB_PATH = r'Files\etl_data.db'
    SQLITE_TABLE = 'stock_sentiment_clean'
    
    # Configuración para gráficas
    GRAPHICS_OUTPUT_PATH = r'Graphics'
    GRAPHICS_DPI = 300
    GRAPHICS_FORMAT = 'png'
    FIGURE_SIZE = (12, 8)