import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class GraphicsTransform:
    """
    Clase para crear gráficas de análisis del dataset de sentimientos de noticias.
    """
    
    def __init__(self, df):
        """
        Inicializa la clase con el DataFrame de datos.
        
        Args:
            df (pd.DataFrame): DataFrame con los datos procesados
        """
        self.df = df.copy()
        self.prepare_data()
    
    def prepare_data(self):
        """Prepara los datos para el análisis gráfico."""
        # Convertir Date a datetime
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        
        # Crear columnas adicionales para análisis
        self.df['SentimentLabel'] = self.df['Label'].map({0: 'Negativo', 1: 'Positivo'})
        
    def create_sentiment_distribution(self):
        """
        Crea un gráfico de distribución de sentimientos.
        
        Returns:
            matplotlib.figure.Figure: Figura de la gráfica
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Gráfico de barras
        sentiment_counts = self.df['SentimentLabel'].value_counts()
        colors = ['#ff7f7f', '#7f7fff']  # Rojo para negativo, azul para positivo
        
        bars = ax1.bar(sentiment_counts.index, sentiment_counts.values, color=colors)
        ax1.set_title('Distribución de Sentimientos en las Noticias', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Frecuencia')
        ax1.set_xlabel('Sentimiento')
        
        # Agregar etiquetas en las barras
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 10,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        # Gráfico de torta
        wedges, texts, autotexts = ax2.pie(sentiment_counts.values, labels=sentiment_counts.index, 
                                          autopct='%1.1f%%', colors=colors, startangle=90)
        ax2.set_title('Proporción de Sentimientos', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def create_sentiment_timeline(self):
        """
        Crea un gráfico de línea temporal de sentimientos.
        
        Returns:
            matplotlib.figure.Figure: Figura de la gráfica
        """
        fig, ax = plt.subplots(figsize=(15, 8))
        
        # Agrupar por fecha y calcular el promedio de sentimiento
        daily_sentiment = self.df.groupby('Date')['Label'].agg(['mean', 'count']).reset_index()
        daily_sentiment['SentimentPercentage'] = daily_sentiment['mean'] * 100
        
        # Crear gráfico de línea
        ax.plot(daily_sentiment['Date'], daily_sentiment['SentimentPercentage'], 
                linewidth=2, color='#2E86AB', marker='o', markersize=3)
        
        # Línea de referencia en 50%
        ax.axhline(y=50, color='red', linestyle='--', alpha=0.7, label='Neutralidad (50%)')
        
        ax.set_title('Evolución Temporal del Sentimiento Positivo', fontsize=16, fontweight='bold')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Porcentaje de Sentimiento Positivo (%)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Formato de fechas en el eje x
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        return fig
    
    def create_sentiment_by_weekday(self):
        """
        Crea un gráfico de sentimientos por día de la semana.
        
        Returns:
            matplotlib.figure.Figure: Figura de la gráfica
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Calcular promedio de sentimiento por día de la semana
        weekday_sentiment = self.df.groupby('DayName')['Label'].agg(['mean', 'count']).reset_index()
        weekday_sentiment['SentimentPercentage'] = weekday_sentiment['mean'] * 100
        
        # Ordenar por días de la semana
        day_order = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        weekday_sentiment['DayName'] = pd.Categorical(weekday_sentiment['DayName'], 
                                                     categories=day_order, ordered=True)
        weekday_sentiment = weekday_sentiment.sort_values('DayName')
        
        # Crear gráfico de barras
        colors = plt.cm.viridis(np.linspace(0, 1, len(weekday_sentiment)))
        bars = ax.bar(weekday_sentiment['DayName'], weekday_sentiment['SentimentPercentage'], 
                     color=colors)
        
        # Línea de referencia
        ax.axhline(y=50, color='red', linestyle='--', alpha=0.7, label='Neutralidad (50%)')
        
        ax.set_title('Sentimiento Positivo por Día de la Semana', fontsize=14, fontweight='bold')
        ax.set_ylabel('Porcentaje de Sentimiento Positivo (%)')
        ax.set_xlabel('Día de la Semana')
        ax.legend()
        
        # Agregar etiquetas en las barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        plt.tight_layout()
        return fig
    
    def create_headline_analysis(self):
        """
        Crea un gráfico de análisis de titulares.
        
        Returns:
            matplotlib.figure.Figure: Figura de la gráfica
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Distribución de longitud promedio de titulares
        ax1.hist(self.df['AvgHeadlineLength'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.set_title('Distribución de Longitud Promedio de Titulares')
        ax1.set_xlabel('Longitud Promedio (caracteres)')
        ax1.set_ylabel('Frecuencia')
        ax1.grid(True, alpha=0.3)
        
        # 2. Relación entre longitud de titulares y sentimiento
        sentiment_length = self.df.groupby('SentimentLabel')['AvgHeadlineLength'].mean()
        bars2 = ax2.bar(sentiment_length.index, sentiment_length.values, 
                       color=['#ff7f7f', '#7f7fff'])
        ax2.set_title('Longitud Promedio de Titulares por Sentimiento')
        ax2.set_ylabel('Longitud Promedio (caracteres)')
        
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                    f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # 3. Sentimiento por mes
        monthly_sentiment = self.df.groupby('Month')['Label'].mean() * 100
        ax3.plot(monthly_sentiment.index, monthly_sentiment.values, 
                marker='o', linewidth=3, markersize=8, color='green')
        ax3.set_title('Sentimiento Positivo por Mes')
        ax3.set_xlabel('Mes')
        ax3.set_ylabel('Porcentaje de Sentimiento Positivo (%)')
        ax3.grid(True, alpha=0.3)
        ax3.set_xticks(range(1, 13))
        
        # 4. Heatmap de sentimiento por día de la semana y mes
        pivot_data = self.df.pivot_table(values='Label', 
                                       index='Month', 
                                       columns='DayOfWeek', 
                                       aggfunc='mean')
        
        sns.heatmap(pivot_data, annot=True, cmap='RdYlBu', center=0.5, 
                   fmt='.2f', ax=ax4, cbar_kws={'label': 'Promedio de Sentimiento'})
        ax4.set_title('Heatmap: Sentimiento por Mes y Día de la Semana')
        ax4.set_xlabel('Día de la Semana (0=Lunes)')
        ax4.set_ylabel('Mes')
        
        plt.tight_layout()
        return fig
    
    def create_advanced_analysis(self):
        """
        Crea gráficos de análisis avanzado.
        
        Returns:
            matplotlib.figure.Figure: Figura de la gráfica
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Box plot de longitud de titulares por sentimiento
        sentiment_data = [self.df[self.df['Label']==0]['AvgHeadlineLength'], 
                         self.df[self.df['Label']==1]['AvgHeadlineLength']]
        box_plot = ax1.boxplot(sentiment_data, labels=['Negativo', 'Positivo'], 
                              patch_artist=True)
        box_plot['boxes'][0].set_facecolor('#ff7f7f')
        box_plot['boxes'][1].set_facecolor('#7f7fff')
        ax1.set_title('Distribución de Longitud de Titulares por Sentimiento')
        ax1.set_ylabel('Longitud Promedio (caracteres)')
        ax1.grid(True, alpha=0.3)
        
        # 2. Correlación entre variables numéricas
        numeric_cols = ['AvgHeadlineLength', 'Year', 'Month', 'DayOfWeek', 'Quarter', 'IsWeekend']
        correlation_data = self.df[numeric_cols + ['Label']].corr()['Label'].drop('Label')
        
        colors = ['red' if x < 0 else 'blue' for x in correlation_data.values]
        bars3 = ax2.barh(range(len(correlation_data)), correlation_data.values, color=colors)
        ax2.set_yticks(range(len(correlation_data)))
        ax2.set_yticklabels(correlation_data.index)
        ax2.set_title('Correlación con Sentimiento')
        ax2.set_xlabel('Coeficiente de Correlación')
        ax2.axvline(x=0, color='black', linestyle='-', alpha=0.3)
        
        # 3. Tendencia anual (si hay múltiples años)
        if self.df['Year'].nunique() > 1:
            yearly_sentiment = self.df.groupby('Year')['Label'].mean() * 100
            ax3.bar(yearly_sentiment.index, yearly_sentiment.values, 
                   color='orange', alpha=0.7)
            ax3.set_title('Sentimiento Positivo por Año')
            ax3.set_xlabel('Año')
            ax3.set_ylabel('Porcentaje de Sentimiento Positivo (%)')
        else:
            ax3.text(0.5, 0.5, 'Datos de un solo año\n(2000)', 
                    ha='center', va='center', transform=ax3.transAxes,
                    fontsize=14, bbox=dict(boxstyle="round", facecolor='lightgray'))
            ax3.set_title('Datos Anuales')
        
        # 4. Distribución de sentimientos por trimestre
        quarterly_sentiment = self.df.groupby(['Quarter', 'SentimentLabel']).size().unstack()
        quarterly_sentiment.plot(kind='bar', ax=ax4, color=['#ff7f7f', '#7f7fff'])
        ax4.set_title('Distribución de Sentimientos por Trimestre')
        ax4.set_xlabel('Trimestre')
        ax4.set_ylabel('Número de Registros')
        ax4.legend(title='Sentimiento')
        plt.setp(ax4.xaxis.get_majorticklabels(), rotation=0)
        
        plt.tight_layout()
        return fig
    