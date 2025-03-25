import unittest
import json
import sys
import os
from unittest.mock import patch, MagicMock

# Agregar el directorio principal al path para poder importar app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  
import app as app_module  # Importar el módulo completo en lugar de variables específicas

class SimpleTests(unittest.TestCase):
    def setUp(self):
        # Configurar la aplicación para pruebas
        app_module.app.config['TESTING'] = True
        self.client = app_module.app.test_client()
        
        # Reiniciar contadores globales antes de cada prueba
        app_module.api_calls_count = 0
        app_module.api_errors_count = 0
        app_module.api_response_times = []
        
        # Reiniciar historial y horas
        app_module.initialize_hours()
        
        # Reiniciar todos los valores del historial
        for key in app_module.api_history:
            app_module.api_history[key] = [0] * app_module.HISTORY_INTERVALS
    
    def test_track_api_call(self):
        """Prueba simple de la función track_api_call"""
        # Estado inicial
        self.assertEqual(app_module.api_calls_count, 0)
        
        # Registrar una llamada exitosa
        app_module.track_api_call(True, 0.5)
        
        # Verificar que se actualizaron los contadores
        self.assertEqual(app_module.api_calls_count, 1)
        self.assertEqual(app_module.api_errors_count, 0)
        self.assertEqual(app_module.api_response_times, [0.5])
    
    @patch('app.requests.get')
    def test_get_standings_simple(self, mock_get):
        """Prueba simple de la ruta /api/standings"""
        # Configurar el mock para simular una respuesta exitosa
        mock_response = MagicMock()
        mock_response.json.return_value = {'success': True, 'data': {'table': []}}
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_get.return_value = mock_response
        
        # Hacer la solicitud
        response = self.client.get('/api/standings')
        
        # Verificar la respuesta
        self.assertEqual(response.status_code, 200)
        
        # Verificar que se registró la llamada a la API
        self.assertEqual(app_module.api_calls_count, 1)

if __name__ == '__main__':
    unittest.main()
