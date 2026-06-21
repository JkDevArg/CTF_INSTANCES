# Mario_bros — Super Mario CTF (Web / Recon, flag dinamica)
# Necesita PHP (guard.php / arm.php / flag.php) para el handshake de la flag.
FROM php:8.2-apache

# Respetar el .htaccess del reto (sin listado de directorios, bloquea .git,
# oculta guard.php, sirve README.md como texto, etc.).
RUN sed -ri 's/AllowOverride None/AllowOverride All/' /etc/apache2/apache2.conf

# La raiz web es SOLO el juego. Los archivos privados/solucionario viven en la
# carpeta padre (Mario_bros/) y no se copian aqui.
COPY FullScreenMario/ /var/www/html/

EXPOSE 80
