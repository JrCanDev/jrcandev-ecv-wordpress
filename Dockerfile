FROM wordpress:latest

# Installer les outils MySQL et WP-CLI
RUN apt-get update && \
    apt-get install --reinstall -y bash && \
    apt-get install -y nano python3 python3-pip python3-venv default-mysql-client && \
    curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && \
    chmod +x wp-cli.phar && \
    mv wp-cli.phar /usr/local/bin/wp

# Copier le script d'initialisation
COPY ./init-wp.sh /usr/local/bin/init-wp.sh
COPY ./wp-config.php /var/www/html/wp-config.php
COPY ./.htaccess /var/www/html/.htaccess
RUN chmod +x /usr/local/bin/init-wp.sh
RUN chmod 644 /var/www/html/

# Copier les scripts python
COPY ./scripts /var/www/html/scripts

# Copier le fichier .env
COPY .env /var/www/html/scripts/.env

# Installer les modules python
COPY ./scripts/requirements.txt /var/www/html/scripts/requirements.txt
RUN python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /var/www/html/scripts/requirements.txt

# Ajouter l'environnement virtuel au PATH
ENV PATH="/venv/bin:$PATH"

ENTRYPOINT ["/usr/local/bin/init-wp.sh"]
CMD ["apache2-foreground"]