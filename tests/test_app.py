import unittest
import json
import time
import sys
import os
import requests
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Agregar el directorio principal al path para poder importar app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  
import app as app_module  # Importar el módulo completo en lugar de variables específicas

class LigaMXAppTests(unittest.TestCase):
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
    
    def tearDown(self):
        # Limpiar después de cada prueba
        pass
    
    # PRUEBAS DE RUTAS
    
    def test_index_route(self):
        """Prueba que la ruta principal devuelva la página HTML correctamente"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)
        # Verificar que elementos clave estén presentes sin ser demasiado estrictos con el formato exacto
        self.assertIn(b'Liga MX', response.data)  # Verificar que el título esté presente de alguna forma
        self.assertIn(b'</html>', response.data)  # Verificar que el HTML se cierra correctamente
    
    # PRUEBAS DE API
    
    @patch('app.requests.get')
    def test_get_standings(self, mock_get):
        """Prueba que la ruta /api/standings devuelva datos correctamente"""
        # Configurar el mock para simular una respuesta exitosa
        mock_response = MagicMock()
        mock_response.json.return_value = {'success': True, 'data': {'table': []}}
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_get.return_value = mock_response
        
        # Hacer la solicitud
        response = self.client.get('/api/standings')
        
        # Verificar la respuesta
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        
        # Verificar que se registró la llamada a la API
        self.assertEqual(app_module.api_calls_count, 1)
        self.assertEqual(app_module.api_errors_count, 0)
    
    @patch('app.requests.get')
    def test_get_livescores(self, mock_get):
        """Prueba que la ruta /api/livescores devuelva datos correctamente"""
        # Configurar el mock para simular una respuesta exitosa
        mock_response = MagicMock()
        mock_response.json.return_value = {'success': True, 'data': {'match': []}}
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_get.return_value = mock_response
        
        # Hacer la solicitud
        response = self.client.get('/api/livescores')
        
        # Verificar la respuesta
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        
        # Verificar que se registró la llamada a la API
        self.assertEqual(app_module.api_calls_count, 1)
        self.assertEqual(app_module.api_errors_count, 0)
    
    @patch('app.requests.get')
    def test_get_fixtures(self, mock_get):
        """Prueba que la ruta /api/fixtures devuelva datos correctamente"""
        # Configurar el mock para simular una respuesta exitosa
        mock_response = MagicMock()
        mock_response.json.return_value = {'success': True, 'data': {'fixtures': []}}
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_get.return_value = mock_response
        
        # Hacer la solicitud
        response = self.client.get('/api/fixtures')
        
        # Verificar la respuesta
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        
        # Verificar que se registró la llamada a la API
        self.assertEqual(app_module.api_calls_count, 1)
        self.assertEqual(app_module.api_errors_count, 0)
    
    @patch('app.requests.get')
    def test_get_history(self, mock_get):
        """Prueba que la ruta /api/history devuelva datos correctamente"""
        # Configurar el mock para simular una respuesta exitosa
        mock_response = MagicMock()
        mock_response.json.return_value = {'success': True, 'data': {'match': []}}
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_get.return_value = mock_response
        
        # Hacer la solicitud
        response = self.client.get('/api/history')
        
        # Verificar la respuesta
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        
        # Verificar que se registró la llamada a la API
        self.assertEqual(app_module.api_calls_count, 1)
        self.assertEqual(app_module.api_errors_count, 0)
    
    @patch('app.requests.get')
    def test_get_metrics(self, mock_get):
        """Prueba que la ruta /api/metrics combine correctamente datos de múltiples fuentes"""
        # Configurar el mock para simular respuestas exitosas para las diferentes llamadas
        def mock_get_side_effect(url):
            mock_response = MagicMock()
            mock_response.elapsed.total_seconds.return_value = 0.1
            
            if 'topscorers' in url:
                mock_response.json.return_value = {
                    'success': True, 
                    'data': {
                        'topscorers': [
                            {'name': 'Jugador 1', 'goals': '10'},
                            {'name': 'Jugador 2', 'goals': '8'}
                        ]
                    }
                }
            elif 'table' in url:
                mock_response.json.return_value = {
                    'success': True, 
                    'data': {
                        'table': [
                            {'name': 'Equipo 1', 'goals_scored': '20', 'goals_conceded': '10'},
                            {'name': 'Equipo 2', 'goals_scored': '15', 'goals_conceded': '12'}
                        ]
                    }
                }
            
            return mock_response
        
        mock_get.side_effect = mock_get_side_effect
        
        # Hacer la solicitud
        response = self.client.get('/api/metrics')
        
        # Verificar la respuesta
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        # Verificar la estructura de datos según la implementación actual
        self.assertIn('data', data)
        self.assertIn('top_scorers', data['data'])
        self.assertIn('goals_by_team', data['data'])
        
        # Verificar que se registraron las llamadas a la API
        self.assertEqual(app_module.api_calls_count, 2)  # Una para topscorers y otra para standings
        self.assertEqual(app_module.api_errors_count, 0)
    
    @patch('app.requests.get')
    def test_get_dashboard(self, mock_get):
        """Prueba que la ruta /api/dashboard calcule correctamente las estadísticas"""
        # Configurar el mock para simular respuestas para el cálculo de partidos totales
        def mock_get_side_effect(url):
            mock_response = MagicMock()
            mock_response.elapsed.total_seconds.return_value = 0.1
            
            if 'history' in url:
                if 'page=1' in url or 'page=' not in url:
                    mock_response.json.return_value = {
                        'success': True,
                        'data': {
                            'match': [{'id': '1'}, {'id': '2'}, {'id': '3'}],
                            'total_pages': 3
                        }
                    }
                else:
                    mock_response.json.return_value = {
                        'success': True,
                        'data': {
                            'match': [{'id': '4'}, {'id': '5'}]
                        }
                    }
            
            return mock_response
        
        mock_get.side_effect = mock_get_side_effect
        
        # Registrar algunas llamadas a la API para tener datos de rendimiento
        app_module.track_api_call(True, 0.1)
        app_module.track_api_call(True, 0.2)
        app_module.track_api_call(False, 0)
        
        # Hacer la solicitud
        response = self.client.get('/api/dashboard')
        
        # Verificar la respuesta
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        # Verificar las estadísticas calculadas
        api_stats = data['data']['api_stats']
        self.assertEqual(api_stats['calls'], 3)  # Las 3 llamadas que registramos manualmente
        self.assertEqual(api_stats['errors'], 1)
        self.assertAlmostEqual(api_stats['success_rate'], 66.67, delta=0.01)  # 2 de 3 exitosas
        
        # Verificar el cálculo de partidos totales: (3-1)*3 + 2 = 8
        self.assertEqual(data['data']['total_matches'], 8)
    
    # PRUEBAS DE FUNCIONES INTERNAS
    
    def test_track_api_call_success(self):
        """Prueba que track_api_call registre correctamente una llamada exitosa"""
        # Registrar una llamada exitosa
        app_module.track_api_call(True, 0.5)
        
        # Verificar que se actualizaron los contadores
        self.assertEqual(app_module.api_calls_count, 1)
        self.assertEqual(app_module.api_errors_count, 0)
        self.assertEqual(app_module.api_response_times, [0.5])
        
        # Verificar que se actualizó el historial
        self.assertEqual(sum(app_module.api_history['calls']), 1)
        self.assertEqual(sum(app_module.api_history['errors']), 0)
    
    def test_track_api_call_error(self):
        """Prueba que track_api_call registre correctamente una llamada con error"""
        # Registrar una llamada con error
        app_module.track_api_call(False, 0)
        
        # Verificar que se actualizaron los contadores
        self.assertEqual(app_module.api_calls_count, 1)
        self.assertEqual(app_module.api_errors_count, 1)
        self.assertEqual(app_module.api_response_times, [0])
        
        # Verificar que se actualizó el historial
        self.assertEqual(sum(app_module.api_history['calls']), 1)
        self.assertEqual(sum(app_module.api_history['errors']), 1)

if __name__ == '__main__':
    unittest.main()
