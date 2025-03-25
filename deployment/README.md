# Configuraciu00f3n de CI/CD para LIGAMX Stats

Este directorio contiene archivos de configuraciu00f3n para el despliegue continuo (CI/CD) de la aplicaciu00f3n LIGAMX Stats.

## Configuraciu00f3n de GitHub Actions

La aplicaciu00f3n utiliza GitHub Actions para automatizar las pruebas y el despliegue. Los archivos de configuraciu00f3n se encuentran en el directorio `.github/workflows/`.

### Secretos requeridos

Para que el flujo de CI/CD funcione correctamente, debes configurar los siguientes secretos en tu repositorio de GitHub:

#### Para CI (Integraciu00f3n Continua)

- `LIVESCORE_API_KEY`: Tu clave de API de LiveScore
- `LIVESCORE_API_SECRET`: Tu secreto de API de LiveScore

#### Para CD (Despliegue Continuo)

- `SSH_HOST`: La direcciu00f3n IP o nombre de dominio de tu servidor
- `SSH_USERNAME`: El nombre de usuario para conectarse al servidor
- `SSH_PRIVATE_KEY`: La clave privada SSH para autenticaciu00f3n
- `SMTP_SERVER`: Servidor SMTP para notificaciones
- `SMTP_PORT`: Puerto del servidor SMTP
- `SMTP_USERNAME`: Usuario para autenticaciu00f3n SMTP
- `SMTP_PASSWORD`: Contraseu00f1a para autenticaciu00f3n SMTP
- `SMTP_FROM`: Direcciu00f3n de correo remitente
- `SMTP_TO`: Direcciones de correo destinatarias (separadas por comas)

## Configuraciu00f3n del servidor

### Servicio Systemd

El archivo `ligamxweb.service` es una configuraciu00f3n para systemd que permite ejecutar la aplicaciu00f3n como un servicio en el servidor.

Para instalar el servicio:

1. Copia el archivo a `/etc/systemd/system/`:
   ```
   sudo cp ligamxweb.service /etc/systemd/system/
   ```

2. Recarga la configuraciu00f3n de systemd:
   ```
   sudo systemctl daemon-reload
   ```

3. Habilita el servicio para que se inicie automu00e1ticamente:
   ```
   sudo systemctl enable ligamxweb.service
   ```

4. Inicia el servicio:
   ```
   sudo systemctl start ligamxweb.service
   ```

### Configuraciu00f3n de Nginx

Se recomienda utilizar Nginx como proxy inverso para la aplicaciu00f3n. Aquu00ed hay una configuraciu00f3n bu00e1sica:

```nginx
server {
    listen 80;
    server_name tudominio.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Guarda esta configuraciu00f3n en `/etc/nginx/sites-available/ligamxweb` y crea un enlace simbu00f3lico a `sites-enabled`:

```
sudo ln -s /etc/nginx/sites-available/ligamxweb /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Flujo de trabajo

1. Los desarrolladores hacen push de sus cambios a GitHub
2. GitHub Actions ejecuta las pruebas automu00e1ticamente
3. Si las pruebas pasan y el push fue a la rama `main`, se inicia el proceso de despliegue
4. La aplicaciu00f3n se despliega en el servidor de producciu00f3n
5. El servicio se reinicia para aplicar los cambios

## Monitoreo

Puedes verificar el estado del servicio con:

```
sudo systemctl status ligamxweb.service
```

Y revisar los logs con:

```
sudo journalctl -u ligamxweb.service
```
