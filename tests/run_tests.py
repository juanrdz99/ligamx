import unittest
import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

# Agregar el directorio principal al path para poder importar app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  

# Importar configuración de pruebas
from test_config import TEST_CONFIG, EMAIL_CONFIG, SLACK_CONFIG

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__), "test_results.log")),
        logging.StreamHandler()
    ]
)

def run_tests():
    """Ejecuta todas las pruebas unitarias y devuelve los resultados"""
    # Cargar pruebas desde el directorio de pruebas
    test_loader = unittest.TestLoader()
    # Buscar en el directorio actual (tests)
    test_suite = test_loader.discover(os.path.dirname(__file__), pattern='test_*.py')
    
    # Ejecutar las pruebas y capturar los resultados
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    return result

def send_email_notification(subject, message, to_email=None):
    """Envía una notificación por correo electrónico
    
    Nota: Para usar esta función, debes configurar las credenciales de correo
    en el archivo .env o en variables de entorno del sistema.
    """
    from test_config import EMAIL_CONFIG
    
    if not EMAIL_CONFIG['enabled']:
        logging.info("Notificaciones por correo deshabilitadas en la configuración")
        return False
    
    try:
        # Obtener configuración del correo desde test_config
        from_email = EMAIL_CONFIG['from_email']
        smtp_server = EMAIL_CONFIG['smtp_server']
        smtp_port = EMAIL_CONFIG['smtp_port']
        username = EMAIL_CONFIG['username']
        password = EMAIL_CONFIG['password']
        
        # Si no se especifica destinatario, usar los configurados
        if not to_email:
            to_email = ', '.join(EMAIL_CONFIG['to_emails'])
        
        # Crear mensaje
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = EMAIL_CONFIG['subject_prefix'] + subject
        
        # Agregar cuerpo del mensaje
        msg.attach(MIMEText(message, 'plain'))
        
        # Conectar y enviar
        if not username or not password:
            logging.warning("No se han configurado credenciales de correo. Omitiendo envío.")
            return False
            
        server = smtplib.SMTP(smtp_server, smtp_port)
        if EMAIL_CONFIG['use_tls']:
            server.starttls()
        server.login(username, password)
        server.send_message(msg)
        server.quit()
        
        logging.info(f"Notificación enviada a {to_email}")
        return True
    except Exception as e:
        logging.error(f"Error al enviar notificación por correo: {str(e)}")
        return False

def send_slack_notification(message):
    """Envía una notificación a Slack usando webhooks
    
    Nota: Para usar esta función, debes configurar un webhook de Slack
    en el archivo .env o en variables de entorno del sistema.
    """
    from test_config import SLACK_CONFIG
    import json
    import requests
    
    if not SLACK_CONFIG['enabled']:
        logging.info("Notificaciones por Slack deshabilitadas en la configuración")
        return False
    
    try:
        webhook_url = SLACK_CONFIG['webhook_url']
        if not webhook_url:
            logging.warning("No se ha configurado el webhook de Slack. Omitiendo envío.")
            return False
            
        # Preparar datos para el webhook
        slack_data = {
            'channel': SLACK_CONFIG['channel'],
            'username': SLACK_CONFIG['username'],
            'text': message,
            'icon_emoji': ':warning:'
        }
        
        # Enviar notificación
        response = requests.post(
            webhook_url,
            data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code != 200:
            logging.warning(f"Error al enviar notificación a Slack: {response.status_code} - {response.text}")
            return False
            
        logging.info("Notificación enviada a Slack correctamente")
        return True
    except Exception as e:
        logging.error(f"Error al enviar notificación a Slack: {str(e)}")
        return False

def generate_report(test_result):
    """Genera un informe detallado de los resultados de las pruebas"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"Informe de Pruebas - {timestamp}\n"
    report += "=" * 50 + "\n\n"
    
    # Resumen
    total = test_result.testsRun
    failures = len(test_result.failures)
    errors = len(test_result.errors)
    skipped = len(test_result.skipped) if hasattr(test_result, 'skipped') else 0
    success = total - failures - errors - skipped
    
    report += f"Resumen:\n"
    report += f"  Pruebas ejecutadas: {total}\n"
    report += f"  Exitosas: {success}\n"
    report += f"  Fallidas: {failures}\n"
    report += f"  Errores: {errors}\n"
    report += f"  Omitidas: {skipped}\n\n"
    
    # Detalles de fallos
    if failures > 0:
        report += "Fallos:\n" + "=" * 10 + "\n"
        for i, (test, traceback) in enumerate(test_result.failures, 1):
            report += f"  {i}. {test}\n"
            report += f"     {traceback.split('\\n')[0]}\n\n"
    
    # Detalles de errores
    if errors > 0:
        report += "Errores:\n" + "=" * 10 + "\n"
        for i, (test, traceback) in enumerate(test_result.errors, 1):
            report += f"  {i}. {test}\n"
            report += f"     {traceback.split('\\n')[0]}\n\n"
    
    return report

def save_report(report, filename="test_report.txt"):
    """Guarda el informe en un archivo"""
    try:
        with open(filename, 'w') as f:
            f.write(report)
        logging.info(f"Informe guardado en {filename}")
        return True
    except Exception as e:
        logging.error(f"Error al guardar el informe: {str(e)}")
        return False

def main():
    """Función principal que ejecuta las pruebas y envía notificaciones si hay errores"""
    logging.info("Iniciando ejecución de pruebas automatizadas")
    
    # Ejecutar pruebas
    result = run_tests()
    
    # Generar informe
    report = generate_report(result)
    save_report(report)
    
    # Verificar si hay errores o fallos
    has_issues = len(result.failures) > 0 or len(result.errors) > 0
    
    if has_issues:
        # Hay problemas, enviar notificación
        subject = "⚠️ ALERTA: Fallos en las pruebas de LIGAMX Stats"
        message = f"Se han detectado problemas en las pruebas automatizadas de LIGAMX Stats.\n\n{report}"
        
        # Enviar notificaciones por diferentes canales
        # Descomentar las líneas que quieras utilizar
        # send_email_notification(subject, message)
        # send_slack_notification(message)
        
        logging.warning("Se detectaron problemas en las pruebas")
        print("\n⚠️ ALERTA: Se detectaron problemas en las pruebas. Revisa el informe para más detalles.")
    else:
        logging.info("Todas las pruebas pasaron correctamente")
        print("\n✅ Todas las pruebas pasaron correctamente")
    
    return 0 if not has_issues else 1

if __name__ == "__main__":
    sys.exit(main())
