import os
from dotenv import load_dotenv
import secrets
import string
import subprocess
import smtplib
from email.mime.text import MIMEText
import requests

students = []

load_dotenv()
site_url = os.getenv("SITE_COMPLETE_URL")
admin_user = os.getenv("ADMIN_USER")
admin_email = os.getenv("ADMIN_EMAIL")
user_email = os.getenv("USER_EMAIL")
smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
smtp_port = int(os.getenv("SMTP_PORT", 465))
smtp_user = os.getenv("SMTP_USER")
smtp_password = os.getenv("SMTP_PASSWORD")

with open('students.txt', 'r') as file:
    for line in file:
        words = line.strip().split()
        students.append({"firstname": words[0].lower(), "lastname": words[1].lower(), "email": words[0].lower() + '.' + words[1].lower() + user_email})

# Check that all environment variables are set
if not site_url or not admin_user or not admin_email or not smtp_user or not smtp_password:
    print("Erreur: Une ou plusieurs variables d'environnement ne sont pas définies.")
    print(f"SITE_COMPLETE_URL={site_url}")
    print(f"ADMIN_USER={admin_user}")
    print(f"ADMIN_EMAIL={admin_email}")
    print(f"SMTP_USER={smtp_user}")
    print(f"SMTP_PASSWORD={'set' if smtp_password else 'not set'}")
    exit(1)

for student in students:
    username = student["firstname"]
    new_site_slug = student["firstname"] + student["lastname"]
    new_site_title = student["firstname"] + " " + student["lastname"]
    password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))

    # Create user
    command_user_create = [
        'wp', 'user', 'create', username, student["email"],
        '--user_pass={}'.format(password),
        '--role=subscriber',
        '--allow-root'
    ]

    result_user_create = subprocess.run(command_user_create, capture_output=True, text=True)

    if result_user_create.returncode == 0:
        print(f"Utilisateur {username} créé avec succès!")

        # Subsite creation
        command_site_create = [
            'wp', 'site', 'create',
            '--slug={}'.format(new_site_slug),
            '--title={}'.format(new_site_title),
            '--email={}'.format(student["email"]),
            '--allow-root'
        ]

        result_site_create = subprocess.run(command_site_create, capture_output=True, text=True)

        if result_site_create.returncode == 0:
            print(f"Sous-site pour {student['firstname']} {student['lastname']} créé avec succès!")

            # Send email with initial password
            login_url = f"{site_url}/wp-login.php"
            subject = "Welcome to Your New Site"
            body = f"""
            Hello {student['firstname']} {student['lastname']},

            Your account has been created successfully.

            Username: {username}
            Password: {password}

            You can log in to your site using the following URL:
            {login_url}

            Please log in and change your password immediately after logging in.

            Best regards,
            {admin_user}
            """

            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = admin_email
            msg['To'] = student["email"]

            try:
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    server.login(smtp_user, smtp_password)
                    server.sendmail(admin_email, [student["email"]], msg.as_string())
                print(f"Email contenant le mot de passe initial envoyé à {student['email']}!")
            except Exception as e:
                print(f"Erreur lors de l'envoi de l'email pour {username}: {e}")
        else:
            print(f"Erreur lors de la création du sous-site pour {student['firstname']} {student['lastname']}: {result_site_create.returncode}")
            print(result_site_create.stdout)
            print(result_site_create.stderr)
    else:
        print(f"Erreur lors de la création de l'utilisateur {username}: {result_user_create.returncode}")
        print(result_user_create.stdout)
        print(result_user_create.stderr)
