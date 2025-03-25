import os
import json
import time
from datetime import datetime, timedelta

class ApiStatsManager:
    def __init__(self, history_intervals=48):
        self.HISTORY_INTERVALS = history_intervals
        self.stats_file = os.path.join(os.path.dirname(__file__), 'data', 'api_stats.json')
        self.ensure_data_dir()
        
        # Valores predeterminados
        self.api_calls_count = 0
        self.api_errors_count = 0
        self.api_response_times = []
        self.api_start_time = time.time()
        
        # Historial de llamadas para tendencias (últimas horas)
        self.api_history = {
            'calls': [0] * self.HISTORY_INTERVALS,
            'success_rate': [100] * self.HISTORY_INTERVALS,
            'response_time': [0] * self.HISTORY_INTERVALS,
            'errors': [0] * self.HISTORY_INTERVALS
        }
        
        # Horas para el historial
        self.api_hours = self.initialize_hours()
        
        # Cargar datos existentes si están disponibles
        self.load_stats()
    
    def ensure_data_dir(self):
        """Asegura que el directorio de datos exista"""
        data_dir = os.path.dirname(self.stats_file)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def initialize_hours(self):
        """Inicializa las horas para los últimos intervalos"""
        now = datetime.now()
        return [(now - timedelta(hours=i)).strftime('%H:%M') for i in range(self.HISTORY_INTERVALS-1, -1, -1)]
    
    def update_hours(self):
        """Actualiza las horas basadas en la hora actual"""
        now = datetime.now()
        current_hour = now.strftime('%H:%M')
        
        # Si la hora actual ya está en la lista, no es necesario actualizar
        if current_hour in self.api_hours:
            return
        
        # Actualizar las horas y desplazar los datos históricos
        self.api_hours = self.initialize_hours()
        
        # No desplazamos los datos históricos aquí para mantener la continuidad
        # Solo actualizamos las etiquetas de tiempo
    
    def load_stats(self):
        """Carga las estadísticas desde el archivo JSON"""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as f:
                    data = json.load(f)
                
                # Cargar datos básicos
                self.api_calls_count = data.get('api_calls_count', 0)
                self.api_errors_count = data.get('api_errors_count', 0)
                self.api_response_times = data.get('api_response_times', [])
                
                # Si el tiempo de inicio guardado es más reciente que el actual, usarlo
                saved_start_time = data.get('api_start_time', 0)
                if saved_start_time > 0:
                    self.api_start_time = saved_start_time
                
                # Cargar historial
                if 'api_history' in data:
                    self.api_history = data['api_history']
                
                # Actualizar horas
                self.update_hours()
                
                print(f"Estadísticas de API cargadas: {self.api_calls_count} llamadas, {self.api_errors_count} errores")
        except Exception as e:
            print(f"Error al cargar estadísticas de API: {str(e)}")
    
    def save_stats(self):
        """Guarda las estadísticas en el archivo JSON"""
        try:
            data = {
                'api_calls_count': self.api_calls_count,
                'api_errors_count': self.api_errors_count,
                'api_response_times': self.api_response_times[-100:],  # Guardar solo los últimos 100 tiempos para evitar archivos enormes
                'api_start_time': self.api_start_time,
                'api_history': self.api_history,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.stats_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error al guardar estadísticas de API: {str(e)}")
    
    def track_api_call(self, success, response_time):
        """Registra una llamada a la API y actualiza las estadísticas"""
        self.api_calls_count += 1
        self.api_response_times.append(response_time)
        if not success:
            self.api_errors_count += 1
        
        # Actualizar horas si es necesario
        self.update_hours()
        
        # Obtener la hora actual para actualizar el índice correcto
        current_hour = datetime.now().strftime('%H:%M')
        
        # Buscar la hora actual en el array de horas o usar la más cercana
        if current_hour in self.api_hours:
            hour_index = self.api_hours.index(current_hour)
        else:
            # Si la hora exacta no está, encontrar la hora más cercana
            hour_index = self.HISTORY_INTERVALS - 1
            
            # Convertir current_hour a minutos desde medianoche para comparación
            current_hour_parts = current_hour.split(':')
            current_minutes = int(current_hour_parts[0]) * 60 + int(current_hour_parts[1])
            
            # Encontrar la hora más cercana
            min_diff = float('inf')
            for i, hour in enumerate(self.api_hours):
                hour_parts = hour.split(':')
                hour_minutes = int(hour_parts[0]) * 60 + int(hour_parts[1])
                diff = abs(hour_minutes - current_minutes)
                if diff < min_diff:
                    min_diff = diff
                    hour_index = i
        
        # Actualizar historial para la hora actual
        self.api_history['calls'][hour_index] += 1
        
        if not success:
            self.api_history['errors'][hour_index] += 1
        
        # Actualizar tasa de éxito
        total_calls = self.api_history['calls'][hour_index]
        total_errors = self.api_history['errors'][hour_index]
        success_rate = 100
        if total_calls > 0:
            success_rate = round(((total_calls - total_errors) / total_calls) * 100)
        self.api_history['success_rate'][hour_index] = success_rate
        
        # Actualizar tiempo de respuesta promedio
        self.api_history['response_time'][hour_index] = response_time
        
        # Guardar estadísticas después de cada actualización
        self.save_stats()
    
    def get_api_stats(self):
        """Obtiene las estadísticas básicas de la API"""
        # Calcular tiempo de respuesta promedio
        avg_response_time = 0
        if self.api_response_times:
            avg_response_time = sum(self.api_response_times) / len(self.api_response_times)
        
        # Calcular tasa de éxito global
        success_rate = 100
        if self.api_calls_count > 0:
            success_rate = 100 - (self.api_errors_count / self.api_calls_count) * 100
        
        return {
            'calls': self.api_calls_count,
            'success_rate': success_rate,
            'response_time': avg_response_time,
            'errors': self.api_errors_count,
            'uptime': int(time.time() - self.api_start_time)
        }
    
    def get_api_trend(self):
        """Obtiene los datos de tendencias de la API"""
        return self.api_history
    
    def get_hours(self):
        """Obtiene las horas para el historial"""
        return self.api_hours
    
    def get_dashboard_data(self):
        """Obtiene los datos para el dashboard"""
        return {
            'api_stats': self.get_api_stats(),
            'api_trend': self.get_api_trend(),
            'hours': self.get_hours()
        }
