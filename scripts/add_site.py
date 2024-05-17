import os
from dotenv import load_dotenv
import secrets
import string
import subprocess

students= []

load_dotenv()
site_url = os.getenv("SITE_COMPLETE_URL")
admin_user = os.getenv("ADMIN_USER")
admin_email = os.getenv("ADMIN_EMAIL")
user_email = os.getenv("USER_EMAIL")

with open('students.txt', 'r') as file:
    for line in file:
        words = line.strip().split()
        students.append({"firstname": words[0].lower(), "lastname": words[1].lower(), "email": words[0].lower()+'.'+words[1].lower()+user_email})

# Check that all environment variables are set
if not site_url or not admin_user or not admin_email:
    print("Erreur: Une ou plusieurs variables d'environnement ne sont pas définies.")
    print(f"SITE_COMPLETE_URL={site_url}")
    print(f"ADMIN_USER={admin_user}")
    print(f"ADMIN_EMAIL={admin_email}")
    exit(1)

for student in students:
    username = student["firstname"]
    new_site_slug = student["firstname"] + student["lastname"]
    new_site_title = student["firstname"] + " " + student["lastname"]
    password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))

    # subsite creation
    command = [
        'wp', 'site', 'create',
        '--slug={}'.format(new_site_slug),
        '--title={}'.format(new_site_title),
        '--email={}'.format(student["email"]),
        '--allow-root'
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"Sous-site pour {student['firstname']} {student['lastname']} créé avec succès!")
    else:
        print(f"Erreur pour {student['firstname']} {student['lastname']}: {result.returncode}")
        print(result.stdout)
        print(result.stderr)