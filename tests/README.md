# Pruebas Automatizadas para LIGAMX Stats

Este directorio contiene las pruebas automatizadas para la aplicaciu00f3n LIGAMX Stats. Las pruebas validan la funcionalidad de la aplicaciu00f3n, aseguran la cobertura de varios escenarios de uso y proporcionan notificaciones en caso de fallos.

## Estructura de Archivos

- `test_app.py`: Pruebas unitarias bu00e1sicas para la aplicaciu00f3n.
- `test_advanced.py`: Pruebas avanzadas que cubren escenarios de error y casos especiales.
- `test_config.py`: Configuraciu00f3n para las pruebas, incluyendo opciones para notificaciones.
- `run_tests.py`: Script para ejecutar todas las pruebas y generar informes.
- `schedule_tests.py`: Script para programar la ejecuciu00f3n periu00f3dica de las pruebas.

## Cu00f3mo Ejecutar las Pruebas

### Usando el ejecutor principal

Desde el directorio principal del proyecto, puedes usar el script `test_runner.py` para ejecutar las pruebas:

```bash
# Ejecutar todas las pruebas
python test_runner.py

# Ejecutar una prueba especu00edfica
python test_runner.py -t test_app

# Programar la ejecuciu00f3n periu00f3dica (cada hora)
python test_runner.py -s

# Programar la ejecuciu00f3n periu00f3dica (cada 2 horas)
python test_runner.py -s 2

# Ver el u00faltimo informe de pruebas
python test_runner.py -r
```

### Ejecuciu00f3n directa

Tambiou00e9n puedes ejecutar las pruebas directamente desde el directorio de pruebas:

```bash
# Navegar al directorio de pruebas
cd tests

# Ejecutar todas las pruebas
python run_tests.py

# Ejecutar una prueba especu00edfica
python test_app.py
```

## Notificaciones

El sistema puede enviar notificaciones cuando se detectan fallos en las pruebas. Las opciones de notificaciu00f3n se configuran en `test_config.py`:

- **Correo electru00f3nico**: Configura las credenciales SMTP y las direcciones de correo en `EMAIL_CONFIG`.
- **Slack**: Configura el webhook URL y el canal en `SLACK_CONFIG`.
- **SMS**: Configura las credenciales de Twilio y los nu00fameros de telu00e9fono en `SMS_CONFIG`.

Para habilitar las notificaciones, establece `'enabled': True` en la configuraciu00f3n correspondiente.

## Informes

Los informes de pruebas se guardan en el directorio `reports` en la rau00edz del proyecto. Cada informe incluye:

- Resumen de pruebas ejecutadas, exitosas, fallidas y con errores.
- Detalles de los fallos y errores encontrados.
- Fecha y hora de la ejecuciu00f3n.

## Programaciu00f3n

Puedes programar la ejecuciu00f3n periu00f3dica de las pruebas usando el script `schedule_tests.py`. Por defecto, las pruebas se ejecutan cada hora, pero puedes modificar este intervalo en `test_config.py` o al ejecutar el script con el paru00e1metro `-s`.

## Personalizaciu00f3n

Puedes personalizar las pruebas modificando los siguientes archivos:

- `test_config.py`: Configuraciu00f3n general, umbrales de alerta y opciones de notificaciu00f3n.
- `test_app.py` o `test_advanced.py`: Au00f1adir nuevos casos de prueba para cubrir funcionalidades adicionales.

## Solucionar Problemas

Si encuentras problemas al ejecutar las pruebas:

1. Verifica que las importaciones sean correctas (rutas relativas vs. absolutas).
2. Asegu00farate de que la aplicaciu00f3n principal estu00e9 funcionando correctamente.
3. Revisa los logs en `test_results.log` y `scheduled_tests.log` para obtener mu00e1s informaciu00f3n.
