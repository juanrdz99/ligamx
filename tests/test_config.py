# Configuración para las pruebas automatizadas de LIGAMX Stats
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Directorio base para reportes y logs
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuración general
TEST_CONFIG = {
    # Habilitar o deshabilitar tipos de pruebas
    'enable_api_tests': True,        # Pruebas de endpoints de API
    'enable_function_tests': True,   # Pruebas de funciones internas
    'enable_integration_tests': True, # Pruebas de integración
    
    # Configuración de ejecución
    'retry_failed_tests': 1,         # Número de reintentos para pruebas fallidas
    'timeout_seconds': 10,           # Tiempo máximo para cada prueba
    
    # Umbrales para alertas
    'alert_on_any_failure': True,    # Alertar ante cualquier fallo
    'min_success_rate': 95,          # Porcentaje mínimo de éxito aceptable
    
    # Configuración de reportes
    'save_reports': True,            # Guardar reportes en archivos
    'report_directory': os.path.join(BASE_DIR, 'reports'),  # Directorio para reportes
    'keep_reports_days': 30,         # Días que se conservan los reportes
    
    # Programación
    'schedule_interval_hours': 1,    # Intervalo en horas para pruebas programadas
    
    # Endpoints de API para pruebas
    'api_endpoints': [
        '/api/standings',
        '/api/livescores',
        '/api/fixtures',
        '/api/history',
        '/api/metrics',
        '/api/dashboard'
    ],
    
    # Credenciales de API para pruebas (usar variables de entorno)
    'api_key': os.getenv('LIVESCORE_API_KEY'),
    'api_secret': os.getenv('LIVESCORE_API_SECRET'),
}

# Configuración de notificaciones por correo
EMAIL_CONFIG = {
    'enabled': False,                # Habilitar notificaciones por correo
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', '587')),
    'use_tls': True,
    'username': os.getenv('SMTP_USERNAME', ''),
    'password': os.getenv('SMTP_PASSWORD', ''),
    'from_email': os.getenv('SMTP_FROM', 'notificaciones@ligamx.com'),
    'to_emails': os.getenv('SMTP_TO', 'admin@ligamx.com').split(','),
    'cc_emails': [],
    'subject_prefix': '[LIGAMX Tests] ',
}

# Configuración de notificaciones por Slack
SLACK_CONFIG = {
    'enabled': False,                # Habilitar notificaciones por Slack
    'webhook_url': '',               # URL del webhook de Slack
    'channel': '#alertas-sistema',   # Canal donde se enviarán las notificaciones
    'username': 'LIGAMX Test Bot',   # Nombre del bot
    'icon_emoji': ':soccer:',        # Emoji para el avatar del bot
}

# Configuración de notificaciones por SMS (usando Twilio)
SMS_CONFIG = {
    'enabled': False,                # Habilitar notificaciones por SMS
    'account_sid': '',               # Twilio Account SID
    'auth_token': '',                # Twilio Auth Token
    'from_number': '',               # Número de teléfono de origen
    'to_numbers': [],                # Lista de números de teléfono de destino
}

# Configuración de casos de prueba específicos
TEST_CASES = {
    # Pruebas de API
    'api_endpoints': [
        {'name': 'standings', 'url': '/api/standings', 'expected_status': 200},
        {'name': 'livescores', 'url': '/api/livescores', 'expected_status': 200},
        {'name': 'fixtures', 'url': '/api/fixtures', 'expected_status': 200},
        {'name': 'history', 'url': '/api/history', 'expected_status': 200},
        {'name': 'metrics', 'url': '/api/metrics', 'expected_status': 200},
        {'name': 'dashboard', 'url': '/api/dashboard', 'expected_status': 200},
    ],
    
    # Casos de error específicos a probar
    'error_scenarios': [
        # Simular error de conexión a la API
        {'name': 'api_connection_error', 'type': 'connection', 'endpoint': '/api/standings'},
        
        # Simular respuesta de API con formato incorrecto
        {'name': 'api_invalid_format', 'type': 'format', 'endpoint': '/api/metrics'},
        
        # Simular timeout en la API
        {'name': 'api_timeout', 'type': 'timeout', 'endpoint': '/api/dashboard', 'timeout_seconds': 5},
        
        # Simular respuesta vacía
        {'name': 'api_empty_response', 'type': 'empty', 'endpoint': '/api/livescores'},
        
        # Simular error de autenticación
        {'name': 'api_auth_error', 'type': 'auth', 'endpoint': '/api/fixtures'},
    ],
    
    # Valores esperados para validaciones
    'expected_values': {
        'min_teams_in_standings': 18,     # Número mínimo de equipos en la tabla
        'max_api_response_time': 2.0,      # Tiempo máximo de respuesta en segundos
        'required_fields_standings': ['rank', 'name', 'points', 'matches'],  # Campos requeridos
    }
}
