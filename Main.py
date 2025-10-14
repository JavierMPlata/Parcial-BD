from Extract.StockExtract import StockExtract
from Transform.StockTransform import StockTransform
from Load.StockLoad import Loader
from Config.Config import Config

def main():
    """
    Función principal del proceso ETL.
    """
    try:
        # 1. EXTRACCIÓN DE DATOS
        print("PASO 1: EXTRAYENDO DATOS...")
        print("=" * 50)
        extractor = StockExtract(Config.INPUT_PATH)
        extractor.queries()

        print("Primeras 5 filas de los datos extraídos:")
        print(extractor.response())
        print(f"Shape de los datos originales: {extractor.data.shape}")
        print("\n")

        # 2. TRANSFORMACIÓN DE DATOS
        print("PASO 2: TRANSFORMANDO Y LIMPIANDO DATOS...")
        print("=" * 60)
        transformer = StockTransform(extractor.data)
        cleaned_data = transformer.clean_data()

        # Mostrar resumen detallado
        transformer.print_detailed_summary()
        
        print("\n" + "="*60)
        print("📋 MUESTRA DE DATOS LIMPIOS")
        print("="*60)
        print("Primeras 3 filas:")
        print(cleaned_data[['Date', 'Label', 'Year', 'DayName', 'HeadlineCount', 
                          'AvgHeadlineLength', 'IsWeekend']].head(3))
        print("\n")

        # 3. CARGA DE DATOS
        print("PASO 3: GUARDANDO DATOS PROCESADOS...")
        print("=" * 60)
        loader = Loader(cleaned_data)
        
        # Guardar en CSV
        output_csv = Config.INPUT_PATH.replace('.csv', '_limpio.csv')
        loader.to_csv(output_csv)
        
        # Guardar en SQLite
        loader.to_sqlite()
        
        # Mostrar estadísticas finales
        print("\n" + "🎉" * 20)
        print("✅ PROCESO ETL COMPLETADO EXITOSAMENTE!")
        print("🎉" * 20)
        print(f"\n📊 ESTADÍSTICAS FINALES:")
        print(f"   • Datos originales: {extractor.data.shape[0]:,} filas × {extractor.data.shape[1]} columnas")
        print(f"   • Datos procesados: {cleaned_data.shape[0]:,} filas × {cleaned_data.shape[1]} columnas")
        print(f"   • Eficiencia de limpieza: {(cleaned_data.shape[0]/extractor.data.shape[0]*100):.1f}%")
        print(f"   • Nuevas características: {cleaned_data.shape[1] - extractor.data.shape[1]} columnas")
        
        print(f"\n💾 ARCHIVOS GENERADOS:")
        print(f"   • CSV limpio: {output_csv}")
        print(f"   • Base de datos SQLite: {Config.SQLITE_DB_PATH}")
        print(f"   • Tabla en BD: {Config.SQLITE_TABLE}")
        
        print(f"\n🔍 ANÁLISIS DE SENTIMIENTO:")
        sentiment_dist = cleaned_data['Label'].value_counts()
        print(f"   • Sentimiento Negativo (0): {sentiment_dist.get(0, 0):,} registros")
        print(f"   • Sentimiento Positivo (1): {sentiment_dist.get(1, 0):,} registros")
        
        print("\n" + "="*60)
        
        
        
    except Exception as e:
        print(f"Error en el proceso ETL: {e}")
        raise

if __name__ == "__main__":
    main()