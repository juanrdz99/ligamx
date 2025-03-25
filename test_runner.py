#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ejecutor de pruebas para la aplicaciu00f3n LIGAMX Stats

Este script facilita la ejecuciu00f3n de las pruebas automatizadas desde cualquier ubicaciu00f3n,
configurado para funcionar con la estructura de directorios actual donde las pruebas
se encuentran en el directorio /tests.
"""

import os
import sys
import argparse
import subprocess
import time
from datetime import datetime

# Obtener la ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TESTS_DIR = os.path.join(BASE_DIR, 'tests')

def create_reports_dir():
    """Crea el directorio de reportes si no existe"""
    reports_dir = os.path.join(BASE_DIR, 'reports')
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    return reports_dir

def run_specific_test(test_name):
    """Ejecuta una prueba especu00edfica"""
    print(f"\nu2699ufe0f Ejecutando prueba: {test_name}\n")
    
    # Construir el comando para ejecutar la prueba especu00edfica
    if test_name.endswith('.py'):
        test_path = os.path.join(TESTS_DIR, test_name)
    else:
        test_path = os.path.join(TESTS_DIR, f"{test_name}.py")
    
    if not os.path.exists(test_path):
        print(f"\nu274c Error: No se encontru00f3 el archivo de prueba {test_path}")
        return 1
    
    # Ejecutar la prueba
    result = subprocess.run([sys.executable, test_path], cwd=TESTS_DIR)
    return result.returncode

def run_all_tests():
    """Ejecuta todas las pruebas disponibles"""
    print("\nu2699ufe0f Ejecutando todas las pruebas\n")
    
    # Usar el script run_tests.py del directorio de pruebas
    run_tests_script = os.path.join(TESTS_DIR, 'run_tests.py')
    
    if not os.path.exists(run_tests_script):
        print(f"\nu274c Error: No se encontru00f3 el script de pruebas en {run_tests_script}")
        return 1
    
    # Ejecutar todas las pruebas
    result = subprocess.run([sys.executable, run_tests_script], cwd=TESTS_DIR)
    return result.returncode

def schedule_tests(interval_hours):
    """Programa la ejecuciu00f3n periu00f3dica de las pruebas"""
    print(f"\nu23f0 Programando pruebas cada {interval_hours} hora(s)\n")
    
    # Usar el script schedule_tests.py del directorio de pruebas
    schedule_script = os.path.join(TESTS_DIR, 'schedule_tests.py')
    
    if not os.path.exists(schedule_script):
        print(f"\nu274c Error: No se encontru00f3 el script de programaciu00f3n en {schedule_script}")
        return 1
    
    # Modificar temporalmente el intervalo si es diferente al predeterminado
    if interval_hours != 1:
        # Importar la configuraciu00f3n y modificar el intervalo
        sys.path.insert(0, TESTS_DIR)
        try:
            from tests.test_config import TEST_CONFIG
            TEST_CONFIG['schedule_interval_hours'] = interval_hours
            print(f"Intervalo de programaciu00f3n establecido a {interval_hours} hora(s)")
        except ImportError:
            print("No se pudo modificar el intervalo de programaciu00f3n")
    
    # Ejecutar el programador
    print("Iniciando programador de pruebas (Ctrl+C para detener)...")
    result = subprocess.run([sys.executable, schedule_script], cwd=TESTS_DIR)
    return result.returncode

def generate_report():
    """Genera un informe resumido de las u00faltimas ejecuciones de pruebas"""
    reports_dir = create_reports_dir()
    latest_report = None
    latest_time = 0
    
    # Buscar el informe mu00e1s reciente
    for filename in os.listdir(reports_dir):
        if filename.startswith('test_report') and filename.endswith('.txt'):
            file_path = os.path.join(reports_dir, filename)
            file_time = os.path.getmtime(file_path)
            if file_time > latest_time:
                latest_time = file_time
                latest_report = file_path
    
    if latest_report:
        print(f"\nu2709ufe0f U00daltimo informe de pruebas ({datetime.fromtimestamp(latest_time).strftime('%Y-%m-%d %H:%M:%S')}):\n")
        with open(latest_report, 'r') as f:
            print(f.read())
    else:
        print("\nu274c No se encontraron informes de pruebas previos")
    
    return 0

def main():
    """Funciu00f3n principal del ejecutor de pruebas"""
    parser = argparse.ArgumentParser(description='Ejecutor de pruebas para LIGAMX Stats')
    group = parser.add_mutually_exclusive_group()
    
    group.add_argument('-a', '--all', action='store_true', 
                      help='Ejecutar todas las pruebas')
    group.add_argument('-t', '--test', type=str, 
                      help='Ejecutar una prueba especu00edfica (nombre del archivo sin la extensiu00f3n .py)')
    group.add_argument('-s', '--schedule', type=int, nargs='?', const=1, 
                      help='Programar la ejecuciu00f3n periu00f3dica de las pruebas (intervalo en horas, predeterminado: 1)')
    group.add_argument('-r', '--report', action='store_true', 
                      help='Mostrar el u00faltimo informe de pruebas')
    
    args = parser.parse_args()
    
    # Crear directorio de reportes
    create_reports_dir()
    
    # Determinar la acciu00f3n a realizar
    if args.test:
        return run_specific_test(args.test)
    elif args.schedule is not None:
        return schedule_tests(args.schedule)
    elif args.report:
        return generate_report()
    else:  # Por defecto o si se especifica --all
        return run_all_tests()

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nu23f9 Ejecuciu00f3n interrumpida por el usuario")
        sys.exit(1)
