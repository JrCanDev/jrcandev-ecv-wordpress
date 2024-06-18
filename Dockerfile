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
COPY ./wp-config.php ecv_data/wordpress/wp-config.php
COPY ./.htaccess ecv_data/wordpress/.htaccess
RUN chmod +x /usr/local/bin/init-wp.sh
RUN chmod 644 ecv_data/wordpress/

# Copier les scripts
COPY ./scripts ecv_data/wordpress/scripts

# Copier le fichier .env
COPY .env ecv_data/wordpress/scripts/.env

# Installer les modules python
COPY ./scripts/requirements.txt ecv_data/wordpress/scripts/requirements.txt
RUN python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r ecv_data/wordpress/scripts/requirements.txt

# Ajouter l'environnement virtuel au PATH
ENV PATH="/venv/bin:$PATH"

ENTRYPOINT ["/usr/local/bin/init-wp.sh"]
CMD ["apache2-foreground"]