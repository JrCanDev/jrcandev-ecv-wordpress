#!/bin/bash
set -euo pipefail

# Exporter la variable SITE_URL
export SITE_URL=${SITE_URL:-defaulturl.com}
export ADMIN_USER=${ADMIN_USER:-defaultuser}
export ADMIN_PASSWORD=${ADMIN_PASSWORD:-defaultpassword}
export ADMIN_EMAIL=${ADMIN_EMAIL:-defaultemail@example.com}
export WP_TITLE=${WP_TITLE:-defaulttitle}
export WP_IS_MULTISITE_SUBDOMAIN=${WP_MULTISITE_DOMAINE:-false}


# Utiliser la variable SITE_URL
echo "URL is $SITE_URL"

# Appeler le script d'entrée original de WordPress pour initialiser correctement l'environnement
docker-entrypoint.sh apache2-foreground &

# Attendre que MySQL soit prêt
while ! mysqladmin ping -h"db" --silent; do
    sleep 1
done

# S'assurer que WordPress est complètement installé
while [ ! -f /var/www/html/wp-settings.php ]; do
    echo "Waiting for WordPress to be fully installed..."
    sleep 5
done

# Installer WordPress si non installé
if ! wp core is-installed --allow-root; then
    wp core install --url=$SITE_URL --title=$WP_TITLE --admin_user=$ADMIN_USER --admin_password=$ADMIN_PASSWORD --admin_email=$ADMIN_EMAIL --allow-root
    wp core multisite-install --allow-root --url=$SITE_URL --base="/" --subdomains=false --title=$WP_TITLE --admin_user=$ADMIN_USER --admin_password=$ADMIN_PASSWORD --admin_email=$ADMIN_EMAIL
fi

# Attendre indéfiniment pour garder le conteneur en cours d'exécution en arrière-plan
wait
