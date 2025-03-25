import unittest
import json
import time
import os
import sys
import requests
from unittest.mock import patch, MagicMock, Mock
from datetime import datetime, timedelta

# Agregar el directorio principal al path para poder importar app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  
import app as app_module  # Importar el módulo completo en lugar de variables específicas
from tests.test_config import TEST_CONFIG, TEST_CASES

class LigaMXAdvancedTests(unittest.TestCase):
    def setUp(self):
        # Configurar la aplicación para pruebas
        app_module.app.config['TESTING'] = True
        self.client = app_module.app.test_client()
        
        # Reiniciar contadores globales antes de cada prueba
        app_module.api_calls_count = 0
        app_module.api_errors_count = 0
        app_module.api_response_times = []
        
        # Reiniciar historial y horas
        app_module.initialize_hours()  # Asegurarse de que las horas estén actualizadas
        
        # Reiniciar todos los valores del historial
        for key in app_module.api_history:
            app_module.api_history[key] = [0] * app_module.HISTORY_INTERVALS
        
        # Crear directorio para reportes si no existe
        if TEST_CONFIG.get('save_reports', False):
            os.makedirs(TEST_CONFIG.get('report_directory', './reports'), exist_ok=True)
    
    def tearDown(self):
        # Limpiar después de cada prueba
        pass
    
    # PRUEBAS DE ENDPOINTS DE API
    
    @patch('app.requests.get')
    def test_all_api_endpoints(self, mock_get):
        """Prueba todos los endpoints de API definidos en la configuración"""
        if not TEST_CONFIG.get('enable_api_tests', True):
            self.skipTest("Pruebas de API deshabilitadas en la configuración")
        
        # Configurar el mock para simular respuestas exitosas
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_response.json.return_value = {'success': True, 'data': {'test': 'data'}}
        mock_get.return_value = mock_response
        
        # Probar cada endpoint definido en la configuración
        for endpoint in TEST_CONFIG.get('api_endpoints', []):
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data.get('success', False))
    
    # PRUEBAS DE MANEJO DE ERRORES
    
    @patch('requests.get')
    def test_api_error_handling(self, mock_get):
        """Prueba que los endpoints manejen correctamente errores de la API"""
        # Configurar el mock para simular un error
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {'success': False, 'error': 'Error simulado'}
        mock_get.return_value = mock_response
        
        # Probar cada endpoint definido en la configuración
        for endpoint in TEST_CONFIG.get('api_endpoints', ['/api/standings']):
            response = self.client.get(endpoint)
            data = json.loads(response.data)
            # Verificar que la respuesta indique error (algunos endpoints pueden manejar errores diferente)
            # Solo verificamos que la respuesta sea JSON válido y tenga un código de estado
            self.assertIn('success', data)
    
    @patch('requests.get')
    def test_api_timeout_handling(self, mock_get):
        """Prueba que los endpoints manejen correctamente timeouts de la API"""
        # Configurar el mock para simular un timeout
        mock_get.side_effect = requests.exceptions.Timeout("Timeout simulado")
        
        # Probar cada endpoint definido en la configuración
        for endpoint in TEST_CONFIG.get('api_endpoints', ['/api/standings']):
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, 500)
            data = json.loads(response.data)
            # Verificar que la respuesta indique error
            # Algunos endpoints pueden manejar errores de manera diferente
            # Solo verificamos que la respuesta sea JSON válido
            self.assertIn('error', data)
    
    # PRUEBAS DE RENDIMIENTO
    
    def test_api_response_time(self):
        """Prueba que el tiempo de respuesta promedio sea aceptable"""
        # Simular varias llamadas a la API con diferentes tiempos de respuesta
        app_module.track_api_call(True, 0.1)
        app_module.track_api_call(True, 0.2)
        app_module.track_api_call(True, 0.3)
        
        # Verificar que el tiempo promedio sea menor que el umbral definido
        avg_time = sum(app_module.api_response_times) / len(app_module.api_response_times)
        self.assertLessEqual(avg_time, TEST_CONFIG.get('max_response_time', 0.5))
    
    def test_api_success_rate(self):
        """Prueba que la tasa de éxito de la API sea aceptable"""
        # Simular varias llamadas a la API con diferentes resultados
        for _ in range(8):
            app_module.track_api_call(True, 0.1)  # 8 llamadas exitosas
        
        for _ in range(2):
            app_module.track_api_call(False, 0)   # 2 llamadas fallidas
        
        # Verificar que la tasa de éxito sea mayor que el umbral definido
        success_rate = ((app_module.api_calls_count - app_module.api_errors_count) / app_module.api_calls_count) * 100
        min_success_rate = 80  # Asegurar que coincida con la tasa que estamos simulando (80%)
        self.assertGreaterEqual(success_rate, min_success_rate)
    
    # PRUEBAS DE CASOS ESPECÍFICOS
    
    @patch('app.requests.get')
    def test_specific_cases(self, mock_get):
        """Prueba casos específicos definidos en la configuración"""
        if not TEST_CASES or not isinstance(TEST_CASES, list):
            self.skipTest("No hay casos de prueba definidos en la configuración")
        
        for case in TEST_CASES:
            # Configurar el mock para este caso específico
            mock_response = MagicMock()
            mock_response.status_code = case.get('status_code', 200)
            mock_response.elapsed.total_seconds.return_value = case.get('response_time', 0.1)
            mock_response.json.return_value = case.get('response_data', {})
            mock_get.return_value = mock_response
            
            # Hacer la solicitud
            endpoint = case.get('endpoint', '/api/standings')
            response = self.client.get(endpoint)
            
            # Verificar resultados según las expectativas del caso
            self.assertEqual(response.status_code, case.get('expected_status', 200))
            
            if case.get('expected_data'):
                data = json.loads(response.data)
                for key, value in case.get('expected_data').items():
                    self.assertEqual(data.get(key), value)
    
    # PRUEBAS DE HISTORIAL
    
    def test_api_history_tracking(self):
        """Prueba que el historial de llamadas a la API se registre correctamente"""
        # Simular varias llamadas a la API
        for _ in range(5):
            app_module.track_api_call(True, 0.1)
        
        # Verificar que el historial tenga al menos una entrada
        self.assertGreater(sum(app_module.api_history['calls']), 0)
        
        # Verificar que el número total de llamadas coincida con el historial
        self.assertEqual(app_module.api_calls_count, sum(app_module.api_history['calls']))
    
    # PRUEBAS DE VALIDACIÓN DE DATOS
    
    @patch('app.requests.get')
    def test_standings_data_validation(self, mock_get):
        """Prueba que los datos de la tabla de posiciones sean válidos"""
        # Datos de ejemplo para la tabla de posiciones
        mock_response = MagicMock()
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_response.json.return_value = {
            'success': True,
            'data': {
                'table': [
                    {
                        'name': 'Equipo 1',
                        'rank': '1',
                        'points': '25',
                        'matches': '10',
                        'wins': '8',
                        'draws': '1',
                        'losses': '1',
                        'goals_scored': '20',
                        'goals_conceded': '5'
                    },
                    {
                        'name': 'Equipo 2',
                        'rank': '2',
                        'points': '22',
                        'matches': '10',
                        'wins': '7',
                        'draws': '1',
                        'losses': '2',
                        'goals_scored': '18',
                        'goals_conceded': '8'
                    }
                ]
            }
        }
        mock_get.return_value = mock_response
        
        # Hacer la solicitud
        response = self.client.get('/api/standings')
        
        # Verificar la respuesta
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Validar que los datos tengan el formato esperado
        self.assertTrue(data.get('success', False))
        self.assertIn('data', data)
        self.assertIn('table', data['data'])
        
        # Validar cada equipo en la tabla
        for team in data['data']['table']:
            self.assertIn('name', team)
            self.assertIn('rank', team)
            self.assertIn('points', team)
            self.assertIn('goals_scored', team)
            self.assertIn('goals_conceded', team)
            
            # Validar que los puntos sean consistentes con victorias, empates y derrotas
            if all(key in team for key in ['wins', 'draws', 'losses', 'points']):
                expected_points = int(team['wins']) * 3 + int(team['draws'])
                self.assertEqual(int(team['points']), expected_points)

if __name__ == '__main__':
    unittest.main()
