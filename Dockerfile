FROM wordpress:latest

# Installer les outils MySQL et WP-CLI
RUN apt-get update && \
    apt-get install --reinstall -y bash && \
    apt-get install nano && \
    apt-get install -y default-mysql-client && \
    curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && \
    chmod +x wp-cli.phar && \
    mv wp-cli.phar /usr/local/bin/wp

# Copier le script d'initialisation
COPY ./init-wp.sh /usr/local/bin/init-wp.sh
COPY ./wp-config.php /var/www/html/wp-config.php
COPY ./.htaccess /var/www/html/.htaccess
RUN chmod +x /usr/local/bin/init-wp.sh

ENTRYPOINT ["/usr/local/bin/init-wp.sh"]
CMD ["apache2-foreground"]