import schedule
import time
import subprocess
import logging
import os
import sys
from datetime import datetime

# Agregar el directorio principal al path para poder importar app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__), "scheduled_tests.log")),
        logging.StreamHandler()
    ]
)

def run_tests():
    """Ejecuta el script de pruebas y registra el resultado"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"Ejecutando pruebas programadas a las {timestamp}")
        
        # Ejecutar el script run_tests.py desde el directorio de pruebas
        script_path = os.path.join(os.path.dirname(__file__), 'run_tests.py')
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        
        # Registrar la salida
        if result.returncode == 0:
            logging.info("Pruebas completadas con éxito")
        else:
            logging.error(f"Pruebas fallidas con código de salida {result.returncode}")
            logging.error(f"Salida de error: {result.stderr}")
        
        logging.info(f"Salida: {result.stdout}")
        
        return result.returncode == 0
    except Exception as e:
        logging.error(f"Error al ejecutar las pruebas: {str(e)}")
        return False

def schedule_tests():
    """Configura la programación de las pruebas"""
    # Ejecutar pruebas cada hora
    schedule.every(1).hours.do(run_tests)
    
    # También se pueden programar en momentos específicos
    # schedule.every().day.at("00:00").do(run_tests)  # Cada día a medianoche
    # schedule.every().monday.at("09:00").do(run_tests)  # Cada lunes a las 9 AM
    
    logging.info("Pruebas programadas configuradas")
    logging.info("Próxima ejecución: " + str(schedule.next_run()))
    
    # Ejecutar inmediatamente la primera vez
    run_tests()
    
    # Bucle principal para mantener el programa en ejecución
    while True:
        schedule.run_pending()
        time.sleep(60)  # Comprobar cada minuto

def main():
    """Función principal"""
    try:
        logging.info("Iniciando programador de pruebas automáticas")
        schedule_tests()
    except KeyboardInterrupt:
        logging.info("Programador detenido manualmente")
    except Exception as e:
        logging.error(f"Error en el programador: {str(e)}")

if __name__ == "__main__":
    main()
