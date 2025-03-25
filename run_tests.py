import os
import sys
import subprocess

def main():
    """Ejecuta las pruebas desde el directorio principal del proyecto"""
    # Obtener la ruta al directorio de pruebas
    tests_dir = os.path.join(os.path.dirname(__file__), 'tests')
    tests_script = os.path.join(tests_dir, 'run_tests.py')
    
    # Verificar que el script existe
    if not os.path.exists(tests_script):
        print(f"Error: No se encontru00f3 el script de pruebas en {tests_script}")
        return 1
    
    # Ejecutar el script de pruebas
    print(f"Ejecutando pruebas desde {tests_script}...\n")
    result = subprocess.run([sys.executable, tests_script], cwd=tests_dir)
    
    # Devolver el cu00f3digo de salida del script de pruebas
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
