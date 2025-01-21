* Comment ajouter des utilisateurs

1. Ecrire un fichier `students.txt` au format (Prenom Nom) et suivre l'exemple suivant :

```
John Doe
Bernard Durand
Marie Dupont
```
2. Copier le fichier `students.txt` dans le container d'ecv wordpress et dans le dossier `scripts` (présent dans `/projet/tests/jrcandev-ecv-wordpress/`)

```bash
docker cp students.txt jrcandev-ecv-wordpress_wordpress_1:/var/www/html/scripts/
```


3. Se rendre sur le container d'ecv wordpress (présent dans `/projet/tests/jrcandev-ecv-wordpress/`) et exécuter la commande suivante :

```bash
docker exec -it jrcandev-ecv-wordpress_wordpress_1 /bin/bash
```

**Remarque: pour retrouver le nom du docker ou s'assurer qu'il est bien déployé, vous pouvez exécuter la commande `docker-compose ps`**

4. Se rendre dans le dossier `scripts`

```bash
cd scripts
```

5. Exécuter le script python `add_site.py`

```bash
python add_site.py <fichier_des_étudiants<students.txt>>
```

**Remarque: Le script python accepte les formats de fichiers .txt, .xls, .xlsx, .ods**
