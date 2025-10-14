class Config:
    """
    Clase de configuración para rutas y parámetros del ETL.
    """
    INPUT_PATH = r'Files\stock_senti_analysis.csv'
    SQLITE_DB_PATH = r'Files\etl_data.db'
    SQLITE_TABLE = 'stock_sentiment_clean'