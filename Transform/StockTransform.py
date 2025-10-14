import pandas as pd
import numpy as np
from datetime import datetime
import re

class StockTransform:
    """
    Clase para transformar y limpiar los datos del análisis de sentimiento de acciones.
    """
    def __init__(self, df):
        self.df = df.copy()  # Trabajar con una copia para no modificar el original
        self.df_clean = None
        
    def clean_data(self):
        """
        Método principal para limpiar los datos.
        """
        print("🧹 INICIANDO PROCESO DE LIMPIEZA DE DATOS...")
        print("=" * 60)
        
        # Mostrar información inicial
        print(f"📊 Datos iniciales: {len(self.df)} filas, {len(self.df.columns)} columnas")
        print(f"📅 Período de datos: {self.df['Date'].min()} a {self.df['Date'].max()}")
        
        # Analizar valores nulos iniciales
        self._analyze_null_values()
        
        # 1. Limpiar fechas
        self._clean_dates()
        
        # 2. Validar y limpiar labels
        self._clean_labels()
        
        # 3. Limpiar texto de los titulares
        self.cleaning_results = self._clean_text_columns()
        
        # 4. Remover filas con demasiados valores nulos
        self._remove_rows_with_too_many_nulls()
        
        # 5. Crear nuevas características
        self._create_features()
        
        # 6. Ordenar por fecha
        self._sort_by_date()
        
        # Análisis final de calidad
        self._final_quality_check()
        
        # Mostrar reporte final de limpieza
        self._show_cleaning_summary()
        
        print("✅ LIMPIEZA COMPLETADA EXITOSAMENTE!")
        print(f"📈 Filas procesadas: {len(self.df)} → {len(self.df_clean)}")
        print(f"🗂️  Columnas finales: {len(self.df_clean.columns)}")
        
        return self.df_clean
    
    def _analyze_null_values(self):
        """
        Analiza y reporta los valores nulos en el dataset.
        """
        print("\n🔍 ANÁLISIS DETALLADO DE VALORES NULOS:")
        print("=" * 60)
        
        # Contar nulos por columna
        null_counts = self.df.isnull().sum()
        total_rows = len(self.df)
        
        # Guardar información para mostrar después de la limpieza
        self.original_nulls = null_counts.copy()
        
        # Columnas con nulos
        columns_with_nulls = null_counts[null_counts > 0].sort_values(ascending=False)
        
        if len(columns_with_nulls) == 0:
            print("   ✅ No se encontraron valores nulos en el dataset original")
        else:
            print(f"   ❌ COLUMNAS CON DATOS FALTANTES:")
            print(f"   Total de columnas afectadas: {len(columns_with_nulls)} de {len(self.df.columns)}")
            print()
            
            for col, null_count in columns_with_nulls.items():
                percentage = (null_count / total_rows) * 100
                non_null = total_rows - null_count
                print(f"   📊 {col}:")
                print(f"      • Datos válidos: {non_null:,} ({100-percentage:.1f}%)")
                print(f"      • Datos faltantes: {null_count:,} ({percentage:.1f}%)")
                print()
        
        # Análisis específico de columnas de titulares
        text_columns = [col for col in self.df.columns if col.startswith('Top')]
        headline_nulls = {col: null_counts[col] for col in text_columns if null_counts[col] > 0}
        
        if headline_nulls:
            print("   📰 RESUMEN DE TITULARES CON DATOS FALTANTES:")
            print("-" * 50)
            for col, null_count in headline_nulls.items():
                percentage = (null_count / total_rows) * 100
                print(f"      • {col}: {null_count:,} faltantes ({percentage:.1f}%)")
            
            total_headline_nulls = sum(headline_nulls.values())
            total_headline_cells = len(text_columns) * total_rows
            overall_percentage = (total_headline_nulls / total_headline_cells) * 100
            print(f"\n   📈 TOTAL: {total_headline_nulls:,} celdas vacías de {total_headline_cells:,} ({overall_percentage:.1f}%)")
        
        print()
        print(f"   🔧 ESTRATEGIA DE IMPUTACIÓN A APLICAR:")
        print("      1. Identificar valores NaN/null en cada columna")
        print("      2. Calcular moda (valor más frecuente) de valores válidos")
        print("      3. Reemplazar nulos con la moda de la columna")
        print("      4. Si no hay moda disponible, usar 'Sin titular disponible'")
        print("      5. Normalizar texto y limpiar caracteres especiales")
        print("      6. Validar que no queden valores nulos")
        
        return columns_with_nulls
    
    def _clean_dates(self):
        """
        Limpia y valida las fechas.
        """
        print("📅 Procesando fechas...")
        
        # Convertir a datetime
        self.df['Date'] = pd.to_datetime(self.df['Date'], errors='coerce')
        
        # Remover filas con fechas inválidas
        initial_count = len(self.df)
        self.df = self.df.dropna(subset=['Date'])
        removed_count = initial_count - len(self.df)
        
        if removed_count > 0:
            print(f"   ❌ Removidas {removed_count} filas con fechas inválidas")
        else:
            print("   ✅ Todas las fechas son válidas")
        
        # Agregar componentes de fecha
        self.df['Year'] = self.df['Date'].dt.year
        self.df['Month'] = self.df['Date'].dt.month
        self.df['DayOfWeek'] = self.df['Date'].dt.dayofweek  # 0=Lunes, 6=Domingo
        
        # Mostrar rango de fechas
        fecha_min = self.df['Date'].min().strftime('%d/%m/%Y')
        fecha_max = self.df['Date'].max().strftime('%d/%m/%Y')
        print(f"   📆 Rango temporal: {fecha_min} - {fecha_max}")
        print(f"   🗓️  Años incluidos: {self.df['Year'].nunique()} años únicos")
        
    def _clean_labels(self):
        """
        Limpia y valida los labels de sentimiento.
        """
        print("🏷️  Validando etiquetas de sentimiento...")
        
        # Verificar que solo contenga 0 y 1
        valid_labels = self.df['Label'].isin([0, 1])
        invalid_count = (~valid_labels).sum()
        
        if invalid_count > 0:
            print(f"   ❌ Removidas {invalid_count} filas con etiquetas inválidas")
            self.df = self.df[valid_labels]
        else:
            print("   ✅ Todas las etiquetas son válidas (0 o 1)")
        
        # Convertir a entero
        self.df['Label'] = self.df['Label'].astype(int)
        
        # Mostrar distribución de sentimientos
        sentiment_counts = self.df['Label'].value_counts()
        negativo = sentiment_counts.get(0, 0)
        positivo = sentiment_counts.get(1, 0)
        total = len(self.df)
        
        print(f"   📊 Distribución de sentimiento:")
        print(f"      • Negativo (0): {negativo} registros ({negativo/total*100:.1f}%)")
        print(f"      • Positivo (1): {positivo} registros ({positivo/total*100:.1f}%)")
        
    def _clean_text_columns(self):
        """
        Limpia las columnas de texto (Top1 a Top25) usando imputación inteligente.
        """
        print("\n📰 PROCESO DE LIMPIEZA E IMPUTACIÓN DE TITULARES:")
        print("=" * 70)
        
        # Obtener columnas de texto
        text_columns = [col for col in self.df.columns if col.startswith('Top')]
        print(f"   📄 Procesando {len(text_columns)} columnas de titulares (Top1 - Top25)")
        
        # Contar nulos antes de la limpieza
        nulls_before = {}
        total_nulls_before = 0
        
        print("\n   🔍 ESTADO ANTES DE LA IMPUTACIÓN:")
        print("   " + "-" * 50)
        
        for col in text_columns:
            null_count = self.df[col].isnull().sum()
            nulls_before[col] = null_count
            total_nulls_before += null_count
            
            if null_count > 0:
                percentage = (null_count / len(self.df)) * 100
                print(f"      • {col}: {null_count:,} nulos ({percentage:.1f}%)")
        
        if total_nulls_before == 0:
            print("      ✅ No se encontraron valores nulos en las columnas de titulares")
        else:
            print(f"\n   📊 TOTAL DE VALORES NULOS: {total_nulls_before:,}")
        
        print("\n   🔧 ESTRATEGIA DE IMPUTACIÓN:")
        print("   " + "-" * 40)
        print("      1. Calcular moda (valor más frecuente) por columna")
        print("      2. Reemplazar nulos con la moda correspondiente")
        print("      3. Si no hay moda, usar valor genérico 'Sin titular'")
        print("      4. Normalizar texto y espacios")
        
        # Proceso de imputación detallado
        cleaned_columns = []
        imputation_summary = {}
        
        for col in text_columns:
            original_nulls = nulls_before[col]
            
            if original_nulls > 0:
                print(f"\n      🔄 Procesando {col}:")
                
                # Paso 1: Limpiar datos existentes antes de calcular moda
                self.df[col] = self.df[col].astype(str)
                self.df[col] = self.df[col].replace(['nan', 'NaN', 'None'], pd.NA)
                
                # Paso 2: Calcular moda de valores válidos
                valid_values = self.df[col].dropna()
                valid_values = valid_values[valid_values.str.strip() != '']  # Excluir strings vacíos
                
                if len(valid_values) > 0:
                    mode_value = valid_values.mode()
                    if len(mode_value) > 0:
                        impute_value = mode_value.iloc[0]
                        frequency = valid_values.value_counts().iloc[0] if len(valid_values.value_counts()) > 0 else 0
                        print(f"         • Moda encontrada: '{impute_value[:50]}...' (aparece {frequency} veces)")
                    else:
                        impute_value = "Sin titular disponible"
                        print(f"         • No se pudo calcular moda, usando valor genérico")
                else:
                    impute_value = "Sin titular disponible"
                    print(f"         • Columna sin valores válidos, usando valor genérico")
                
                # Paso 3: Imputar valores nulos
                self.df[col] = self.df[col].fillna(impute_value)
                
                # Paso 4: Limpiar texto
                self.df[col] = self.df[col].apply(self._clean_text)
                
                print(f"         • {original_nulls} valores imputados con: '{impute_value[:30]}...'")
                
                cleaned_columns.append(col)
                imputation_summary[col] = {
                    'nulls_original': original_nulls,
                    'valor_imputado': impute_value,
                    'metodo': 'moda' if 'Sin titular' not in impute_value else 'genérico'
                }
            else:
                # Aunque no tenga nulos, limpiar el texto
                self.df[col] = self.df[col].astype(str)
                self.df[col] = self.df[col].apply(self._clean_text)
        
        # Verificación final
        print(f"\n   ✅ RESULTADO DE LA IMPUTACIÓN:")
        print("   " + "-" * 45)
        
        nulls_after = 0
        for col in text_columns:
            null_count = self.df[col].isnull().sum()
            nulls_after += null_count
        
        print(f"      • Valores nulos restantes: {nulls_after} (✅ Objetivo: 0)")
        print(f"      • Columnas imputadas: {len(cleaned_columns)} de {len(text_columns)}")
        print(f"      • Total valores imputados: {total_nulls_before:,}")
        
        if nulls_after == 0:
            print("      🎉 ¡Imputación exitosa! No quedan valores nulos.")
        else:
            print(f"      ⚠️  Atención: Quedan {nulls_after} valores nulos sin procesar.")
        
        # Mostrar resumen detallado de imputación
        if imputation_summary:
            print(f"\n   📋 RESUMEN DETALLADO DE IMPUTACIÓN:")
            print("   " + "-" * 50)
            for col, info in imputation_summary.items():
                metodo_emoji = "📊" if info['metodo'] == 'moda' else "🔧"
                print(f"      {metodo_emoji} {col}: {info['nulls_original']} → '{info['valor_imputado'][:40]}...'")
        
        return {
            'columnas_procesadas': cleaned_columns,
            'nulls_eliminados': total_nulls_before,
            'imputation_summary': imputation_summary,
            'metodo_usado': 'moda_con_fallback'
        }
        
    def _clean_text(self, text):
        """
        Limpia un texto individual.
        """
        if pd.isna(text) or text == '' or text == 'nan':
            return ''
        
        # Convertir a string si no lo es
        text = str(text)
        
        # Normalizar espacios
        text = re.sub(r'\s+', ' ', text)
        
        # Remover espacios al inicio y final
        text = text.strip()
        
        return text
    
    def _remove_rows_with_too_many_nulls(self):
        """
        Remueve filas que tienen demasiados valores nulos en las columnas de texto.
        """
        print("\n🔍 ANÁLISIS DE CALIDAD POR FILA:")
        print("-" * 40)
        
        text_columns = [col for col in self.df.columns if col.startswith('Top')]
        
        # Contar valores no vacíos por fila (excluyendo strings vacíos y nulos)
        def count_non_empty(row):
            return sum(1 for val in row if val and str(val).strip() != '' and str(val) != 'nan')
        
        non_empty_counts = self.df[text_columns].apply(count_non_empty, axis=1)
        
        # Estadísticas antes de filtrar
        avg_headlines = non_empty_counts.mean()
        min_headlines_found = non_empty_counts.min()
        max_headlines_found = non_empty_counts.max()
        
        print(f"   📊 Estadísticas de titulares por día:")
        print(f"      • Promedio: {avg_headlines:.1f} titulares válidos")
        print(f"      • Mínimo: {min_headlines_found} titulares válidos")
        print(f"      • Máximo: {max_headlines_found} titulares válidos")
        
        # Analizar distribución de titulares por fila
        distribution = non_empty_counts.value_counts().sort_index()
        print(f"   📈 Distribución de titulares por fila:")
        for headlines, count in distribution.items():
            print(f"      • {headlines} titulares: {count} días")
        
        # Mantener filas que tienen al menos X titulares válidos
        min_headlines = 15  # Cambiamos el umbral para ser menos restrictivo
        valid_rows = non_empty_counts >= min_headlines
        
        removed_count = (~valid_rows).sum()
        if removed_count > 0:
            print(f"   ❌ Se removerán {removed_count} filas con menos de {min_headlines} titulares válidos")
            # Mostrar qué filas se van a remover
            rows_to_remove = non_empty_counts[~valid_rows]
            print(f"      Filas removidas tienen entre {rows_to_remove.min()} y {rows_to_remove.max()} titulares")
        else:
            print(f"   ✅ Todas las filas tienen al menos {min_headlines} titulares válidos")
        
        self.df = self.df[valid_rows].reset_index(drop=True)
    
    def _create_features(self):
        """
        Crea nuevas características derivadas de los datos.
        """
        print("🔧 Creando características adicionales...")
        
        text_columns = [col for col in self.df.columns if col.startswith('Top')]
        
        # Contar titulares no vacíos por día
        def count_valid_headlines(row):
            return sum(1 for val in row if val and val != '' and val != 'nan')
        
        self.df['HeadlineCount'] = self.df[text_columns].apply(count_valid_headlines, axis=1)
        print("   ✅ HeadlineCount: Número de titulares válidos por día")
        
        # Longitud promedio de titulares
        def avg_headline_length(row):
            valid_headlines = [val for val in row if val and val != '' and val != 'nan']
            if not valid_headlines:
                return 0
            return np.mean([len(headline) for headline in valid_headlines])
        
        self.df['AvgHeadlineLength'] = self.df[text_columns].apply(avg_headline_length, axis=1)
        print("   ✅ AvgHeadlineLength: Longitud promedio de titulares")
        
        # Consolidar todos los titulares en una sola columna (opcional)
        def combine_headlines(row):
            valid_headlines = [val for val in row if val and val != '' and val != 'nan']
            return ' | '.join(valid_headlines)
        
        self.df['AllHeadlines'] = self.df[text_columns].apply(combine_headlines, axis=1)
        print("   ✅ AllHeadlines: Todos los titulares concatenados")
        
        # Crear mapeo de días de la semana en español
        day_names = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 
                    4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}
        self.df['DayName'] = self.df['DayOfWeek'].map(day_names)
        print("   ✅ DayName: Nombre del día de la semana")
        
        # Crear características temporales adicionales
        self.df['Quarter'] = self.df['Date'].dt.quarter
        self.df['IsWeekend'] = self.df['DayOfWeek'].isin([5, 6]).astype(int)
        print("   ✅ Quarter: Trimestre del año")
        print("   ✅ IsWeekend: Indicador de fin de semana")
        
        # Imputar valores numéricos si hubiera nulos (usando media/mediana)
        self._impute_numeric_features()
        
    def _impute_numeric_features(self):
        """
        Imputa valores nulos en características numéricas usando media o mediana.
        """
        print("\n🔢 IMPUTACIÓN DE CARACTERÍSTICAS NUMÉRICAS:")
        print("-" * 50)
        
        numeric_columns = ['HeadlineCount', 'AvgHeadlineLength', 'Year', 'Month', 
                          'DayOfWeek', 'Quarter', 'IsWeekend']
        
        imputed_numeric = []
        
        for col in numeric_columns:
            if col in self.df.columns:
                nulls = self.df[col].isnull().sum()
                if nulls > 0:
                    # Decidir entre media y mediana basado en la distribución
                    if col in ['HeadlineCount', 'AvgHeadlineLength']:
                        # Para estas variables, usar mediana (más robusta a outliers)
                        impute_value = self.df[col].median()
                        method = 'mediana'
                    else:
                        # Para variables categóricas numéricas, usar moda
                        impute_value = self.df[col].mode().iloc[0] if len(self.df[col].mode()) > 0 else self.df[col].median()
                        method = 'moda'
                    
                    self.df[col] = self.df[col].fillna(impute_value)
                    print(f"   ✅ {col}: {nulls} nulos → {method} ({impute_value:.2f})")
                    imputed_numeric.append((col, nulls, method, impute_value))
        
        if not imputed_numeric:
            print("   ✅ No se encontraron valores nulos en características numéricas")
        
        return imputed_numeric
        
    def _sort_by_date(self):
        """
        Ordena el DataFrame por fecha.
        """
        print("📊 Finalizando procesamiento...")
        
        self.df = self.df.sort_values('Date').reset_index(drop=True)
        self.df_clean = self.df
        print("   ✅ Datos ordenados cronológicamente")
        print("   ✅ Índices reiniciados")
    
    def _final_quality_check(self):
        """
        Realiza una verificación final de calidad de los datos.
        """
        print("\n🔎 VERIFICACIÓN FINAL DE CALIDAD:")
        print("-" * 40)
        
        # Verificar que no hay valores nulos en las columnas principales
        main_cols = ['Date', 'Label']
        has_nulls = False
        
        for col in main_cols:
            null_count = self.df[col].isnull().sum()
            if null_count > 0:
                print(f"   ❌ {col}: {null_count} valores nulos encontrados")
                has_nulls = True
            else:
                print(f"   ✅ {col}: Sin valores nulos")
        
        # Verificar columnas de texto
        text_columns = [col for col in self.df.columns if col.startswith('Top')]
        empty_headlines = 0
        total_headlines = 0
        
        for col in text_columns:
            empty_count = (self.df[col] == '').sum()
            empty_headlines += empty_count
            total_headlines += len(self.df)
        
        print(f"   📊 Titulares vacíos: {empty_headlines}/{total_headlines} ({empty_headlines/total_headlines*100:.1f}%)")
        
        # Verificar consistencia de fechas
        date_duplicates = self.df['Date'].duplicated().sum()
        if date_duplicates > 0:
            print(f"   ⚠️  Fechas duplicadas: {date_duplicates}")
        else:
            print(f"   ✅ Fechas únicas: Sin duplicados")
        
        # Verificar rango de labels
        unique_labels = self.df['Label'].unique()
        expected_labels = [0, 1]
        if set(unique_labels) == set(expected_labels):
            print(f"   ✅ Labels válidos: {sorted(unique_labels)}")
        else:
            print(f"   ❌ Labels inesperados: {sorted(unique_labels)}")
        
        if not has_nulls:
            print("\n   🎉 CALIDAD DE DATOS: EXCELENTE")
        else:
            print("\n   ⚠️  CALIDAD DE DATOS: REVISAR VALORES NULOS")
    
    def _show_cleaning_summary(self):
        """
        Muestra un resumen final de qué columnas tenían nulos y cómo fueron limpiadas.
        """
        print("\n" + "="*70)
        print("📋 REPORTE FINAL DE LIMPIEZA DE DATOS FALTANTES")
        print("="*70)
        
        if not hasattr(self, 'original_nulls'):
            print("   ℹ️  No hay información de valores nulos originales disponible")
            return
        
        # Columnas que tenían nulos originalmente
        columns_with_original_nulls = self.original_nulls[self.original_nulls > 0]
        
        if len(columns_with_original_nulls) == 0:
            print("   ✅ El dataset original no tenía valores nulos")
            return
        
        print(f"   📊 RESUMEN DE COLUMNAS PROCESADAS:")
        print("   " + "-" * 50)
        
        total_nulls_cleaned = 0
        
        for col, original_count in columns_with_original_nulls.items():
            current_nulls = self.df_clean[col].isnull().sum() if col in self.df_clean.columns else 0
            empty_strings = (self.df_clean[col] == '').sum() if col in self.df_clean.columns else 0
            
            total_nulls_cleaned += original_count
            
            print(f"\n   🔧 {col}:")
            print(f"      • Valores nulos originales: {original_count:,}")
            print(f"      • Valores nulos finales: {current_nulls:,}")
            print(f"      • Convertidos a string vacío: {empty_strings:,}")
            
            if current_nulls == 0:
                print(f"      • Estado: ✅ LIMPIADO")
            else:
                print(f"      • Estado: ⚠️  PENDIENTE ({current_nulls} nulos restantes)")
        
        print(f"   📈 ESTADÍSTICAS GENERALES:")
        print("   " + "-" * 40)
        print(f"      • Total de nulos imputados: {total_nulls_cleaned:,}")
        print(f"      • Columnas procesadas: {len(columns_with_original_nulls)}")
        print(f"      • Método utilizado: Imputación por moda + normalización")
        
        # Mostrar detalles de imputación si están disponibles
        if hasattr(self, 'cleaning_results') and 'imputation_summary' in self.cleaning_results:
            imputation_summary = self.cleaning_results['imputation_summary']
            moda_count = sum(1 for info in imputation_summary.values() if info['metodo'] == 'moda')
            generico_count = sum(1 for info in imputation_summary.values() if info['metodo'] == 'genérico')
            
            print(f"      • Imputación por moda: {moda_count} columnas")
            print(f"      • Imputación genérica: {generico_count} columnas")
        
        # Verificar si quedan nulos en todo el dataset
        remaining_nulls = self.df_clean.isnull().sum().sum()
        if remaining_nulls == 0:
            print(f"      • Resultado final: ✅ DATASET COMPLETAMENTE LIMPIO")
        else:
            print(f"      • Resultado final: ⚠️  {remaining_nulls} nulos restantes")
        
        print("\n   🎯 IMPACTO EN LA CALIDAD:")
        print("   " + "-" * 30)
        original_completeness = ((len(self.df_clean) * len(self.df_clean.columns) - total_nulls_cleaned) / 
                               (len(self.df_clean) * len(self.df_clean.columns))) * 100
        final_completeness = ((len(self.df_clean) * len(self.df_clean.columns) - remaining_nulls) / 
                            (len(self.df_clean) * len(self.df_clean.columns))) * 100
        
        print(f"      • Completitud original: {original_completeness:.2f}%")
        print(f"      • Completitud final: {final_completeness:.2f}%")
        print(f"      • Mejora obtenida: +{final_completeness - original_completeness:.2f}%")
        
        print("="*70)
    
    def get_data_summary(self):
        """
        Retorna un resumen detallado de los datos limpios en español.
        """
        if self.df_clean is None:
            return "❌ Datos no han sido limpiados aún. Ejecute clean_data() primero."
        
        # Estadísticas básicas
        total_rows = len(self.df_clean)
        fecha_inicio = self.df_clean['Date'].min().strftime('%d/%m/%Y')
        fecha_fin = self.df_clean['Date'].max().strftime('%d/%m/%Y')
        
        # Distribución de sentimiento
        sentiment_counts = self.df_clean['Label'].value_counts()
        negativo = sentiment_counts.get(0, 0)
        positivo = sentiment_counts.get(1, 0)
        
        # Estadísticas de titulares
        avg_headlines = self.df_clean['HeadlineCount'].mean()
        avg_length = self.df_clean['AvgHeadlineLength'].mean()
        
        # Distribución por años
        years = self.df_clean['Year'].value_counts().sort_index()
        
        # Distribución por días de la semana
        weekdays = self.df_clean['DayName'].value_counts()
        
        summary = {
            '📊 RESUMEN GENERAL': {
                'Total de registros': f"{total_rows:,}",
                'Período de tiempo': f"{fecha_inicio} - {fecha_fin}",
                'Años incluidos': f"{self.df_clean['Year'].nunique()} años",
                'Total de columnas': len(self.df_clean.columns)
            },
            '💭 ANÁLISIS DE SENTIMIENTO': {
                'Registros negativos (0)': f"{negativo:,} ({negativo/total_rows*100:.1f}%)",
                'Registros positivos (1)': f"{positivo:,} ({positivo/total_rows*100:.1f}%)",
                'Balance': 'Positivo' if positivo > negativo else 'Negativo'
            },
            '📰 ANÁLISIS DE TITULARES': {
                'Promedio titulares/día': f"{avg_headlines:.1f}",
                'Longitud promedio': f"{avg_length:.1f} caracteres",
                'Total caracteres': f"{self.df_clean['AllHeadlines'].str.len().sum():,}"
            },
            '📅 DISTRIBUCIÓN TEMPORAL': {
                'Años con más datos': years.head(3).to_dict(),
                'Días más frecuentes': weekdays.head(3).to_dict()
            },
            '🗂️ COLUMNAS CREADAS': [
                'Year (Año)', 'Month (Mes)', 'DayOfWeek (Día semana)',
                'HeadlineCount (Cantidad titulares)', 'AvgHeadlineLength (Longitud promedio)',
                'AllHeadlines (Todos los titulares)', 'DayName (Nombre día)',
                'Quarter (Trimestre)', 'IsWeekend (Es fin de semana)'
            ]
        }
        
        return summary
    
    def print_detailed_summary(self):
        """
        Imprime un resumen detallado formateado de los datos limpios.
        """
        summary = self.get_data_summary()
        
        if isinstance(summary, str):
            print(summary)
            return
        
        print("\n" + "="*70)
        print("📈 REPORTE DETALLADO DE LIMPIEZA DE DATOS")
        print("="*70)
        
        for section_title, section_data in summary.items():
            print(f"\n{section_title}")
            print("-" * 50)
            
            if isinstance(section_data, dict):
                for key, value in section_data.items():
                    if isinstance(value, dict):
                        print(f"   {key}:")
                        for sub_key, sub_value in value.items():
                            print(f"      • {sub_key}: {sub_value}")
                    else:
                        print(f"   • {key}: {value}")
            elif isinstance(section_data, list):
                for item in section_data:
                    print(f"   • {item}")
        
        print("\n" + "="*70)
    
    def response(self):
        """
        Retorna los datos limpios o los primeros registros.
        """
        if self.df_clean is None:
            return "Datos no han sido limpiados aún. Ejecute clean_data() primero."
        
        return self.df_clean