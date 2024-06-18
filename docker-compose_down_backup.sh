#!/bin/bash

if [ ! -f docker-compose.yml ]; then
  echo "Aucun fichier docker-compose.yml trouvé dans le répertoire courant."
  exit 1
fi

BACKUP_DIR="docker_volumes_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

volumes=$(docker-compose ps -q | xargs docker inspect --format '{{ range .Mounts }}{{ if eq .Type "volume" }}{{ .Name }} {{ end }}{{ end }}' | tr ' ' '\n' | sort -u)

for volume in $volumes; do
  echo "Sauvegarde du volume : $volume"
  docker run --rm -v "$volume":/volume -v "$(pwd)/$BACKUP_DIR":/backup ubuntu tar czf "/backup/${volume}.tar.gz" -C /volume . || {
    echo "Erreur lors de la sauvegarde du volume $volume"
    exit 1
  }
done

docker-compose down -v

echo "Les volumes ont été sauvegardés dans le répertoire : $BACKUP_DIR"
