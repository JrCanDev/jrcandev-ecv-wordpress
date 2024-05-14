# jrcandev-ecv-wordpress
Test of automatic creation of sites and users for multisite wordpress

# .env Format

```bash
SITE_URL="localhost:PORT"
SITE_COMPLETE_URL="http://localhost:PORT"
ADMIN_USER="admin_user"
ADMIN_PASSWORD="admin_password"
ADMIN_EMAIL="admin_email"
WP_TITLE="wp_title"
WP_IS_MULTISITE_SUBDOMAIN="false" # false for subdirectory and true for subdomain

MYSQL_USER="wordpress"
MYSQL_PASSWORD="root"
NAME="name"
```

# How to test ?

1. Build

```bash
docker-compose -f docker-compose-local.yml build --no-cache
```

2. Run

```bash
docker-compose -f docker-compose-local.yml up -d
```

3. Open your browser and go to `http://localhost:8000/wp-admin/`

4. Login

5. Go to the /bin/bash

```bash
docker exec -it <container_name> /bin/bash
```

6. Copy the students.txt file

```bash
docker cp students.txt <container_name>:/var/www/html/scripts/
```

7. Run the script

```bash
cd scripts
python3 add_site.py
```

8. Go to the multisites and check if new sites are created
