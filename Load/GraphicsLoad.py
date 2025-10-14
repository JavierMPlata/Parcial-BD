import os
import matplotlib.pyplot as plt
from datetime import datetime
from Config.Config import Config

class GraphicsLoad:
    """
    Clase para guardar gráficas generadas del análisis de sentimientos.
    """
    
    def __init__(self):
        """Inicializa la clase y crea el directorio de salida si no existe."""
        self.output_path = Config.GRAPHICS_OUTPUT_PATH
        self.dpi = Config.GRAPHICS_DPI
        self.format = Config.GRAPHICS_FORMAT
        self.ensure_output_directory()
    
    def ensure_output_directory(self):
        """Crea el directorio de salida si no existe."""
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
            print(f"✓ Directorio creado: {self.output_path}")
    
    def save_figure(self, figure, filename, subfolder=None):
        """
        Guarda una figura en el sistema de archivos.
        
        Args:
            figure (matplotlib.figure.Figure): Figura a guardar
            filename (str): Nombre del archivo (sin extensión)
            subfolder (str, optional): Subcarpeta dentro del directorio principal
            
        Returns:
            str: Ruta completa del archivo guardado
        """
        # Determinar la ruta completa
        if subfolder:
            full_path = os.path.join(self.output_path, subfolder)
            if not os.path.exists(full_path):
                os.makedirs(full_path)
        else:
            full_path = self.output_path
        
        # Agregar timestamp al nombre del archivo para evitar sobrescribir
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        full_filename = f"{filename}_{timestamp}.{self.format}"
        file_path = os.path.join(full_path, full_filename)
        
        try:
            # Guardar la figura
            figure.savefig(file_path, dpi=self.dpi, bbox_inches='tight', 
                          format=self.format, facecolor='white', edgecolor='none')
            print(f"✓ Gráfica guardada: {file_path}")
            return file_path
        except Exception as e:
            print(f"✗ Error guardando gráfica {filename}: {str(e)}")
            return None
        finally:
            # Cerrar la figura para liberar memoria
            plt.close(figure)
    
    def save_all_graphics(self, graphics_transformer):
        """
        Genera y guarda todas las gráficas del análisis.
        
        Args:
            graphics_transformer (GraphicsTransform): Instancia de GraphicsTransform
            
        Returns:
            dict: Diccionario con los nombres de archivos y rutas guardadas
        """
        saved_files = {}
        
        print("📊 Iniciando generación y guardado de gráficas...")
        
        # 1. Distribución de sentimientos
        try:
            fig1 = graphics_transformer.create_sentiment_distribution()
            path1 = self.save_figure(fig1, "01_distribucion_sentimientos")
            saved_files["distribucion_sentimientos"] = path1
        except Exception as e:
            print(f"✗ Error generando distribución de sentimientos: {str(e)}")
        
        # 2. Línea temporal de sentimientos
        try:
            fig2 = graphics_transformer.create_sentiment_timeline()
            path2 = self.save_figure(fig2, "02_timeline_sentimientos")
            saved_files["timeline_sentimientos"] = path2
        except Exception as e:
            print(f"✗ Error generando timeline de sentimientos: {str(e)}")
        
        # 3. Sentimientos por día de la semana
        try:
            fig3 = graphics_transformer.create_sentiment_by_weekday()
            path3 = self.save_figure(fig3, "03_sentimientos_por_dia")
            saved_files["sentimientos_por_dia"] = path3
        except Exception as e:
            print(f"✗ Error generando sentimientos por día: {str(e)}")
        
        # 4. Análisis de titulares
        try:
            fig4 = graphics_transformer.create_headline_analysis()
            path4 = self.save_figure(fig4, "04_analisis_titulares")
            saved_files["analisis_titulares"] = path4
        except Exception as e:
            print(f"✗ Error generando análisis de titulares: {str(e)}")
        
        # 5. Análisis avanzado
        try:
            fig5 = graphics_transformer.create_advanced_analysis()
            path5 = self.save_figure(fig5, "05_analisis_avanzado")
            saved_files["analisis_avanzado"] = path5
        except Exception as e:
            print(f"✗ Error generando análisis avanzado: {str(e)}")
        
        except Exception as e:
            print(f"✗ Error generando resumen estadístico: {str(e)}")
        
        print(f"✅ Proceso completado. {len(saved_files)} gráficas generadas exitosamente.")
        return saved_files
    
    
    def get_graphics_summary(self):
        """
        Obtiene un resumen de las gráficas existentes en el directorio.
        
        Returns:
            dict: Información sobre archivos existentes
        """
        if not os.path.exists(self.output_path):
            return {"total_files": 0, "files": []}
        
        files = [f for f in os.listdir(self.output_path) 
                if f.endswith(f'.{self.format}')]
        
        return {
            "total_files": len(files),
            "files": sorted(files),
            "directory": self.output_path
        }