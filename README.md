# jrcandev-ecv-wordpress
Test of automatic creation of sites and users for multisite wordpress

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
python3 add_user.py
```

8. Go to the multisites and check if new sites are created
