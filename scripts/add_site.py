import os
import sys
import pandas as pd
from dotenv import load_dotenv
import secrets
import string
import subprocess
import smtplib
from email.mime.text import MIMEText
from odf.opendocument import load as load_ods
from odf.table import Table, TableRow, TableCell
from odf.text import P
import time

def load_students(file_path):
    students = []
    file_extension = os.path.splitext(file_path)[1]
    
    if file_extension == '.txt':
        with open(file_path, 'r') as file:
            for line in file:
                words = line.strip().split()
                students.append({"firstname": words[0].lower(), "lastname": words[1].lower()})
    elif file_extension in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
        for index, row in df.iterrows():
            students.append({"firstname": row['Prénom'].strip().lower(), "lastname": row['Nom'].strip().lower()})
    elif file_extension == '.ods':
        doc = load_ods(file_path)
        sheet = doc.spreadsheet.getElementsByType(Table)[0]
        for row in sheet.getElementsByType(TableRow):
            cells = row.getElementsByType(TableCell)
            firstname = ""
            lastname = ""
            if len(cells) > 0:
                firstname_elements = cells[0].getElementsByType(P)
                if len(firstname_elements) > 0:
                    firstname = "".join([str(text) for text in firstname_elements[0].childNodes]).strip().lower()
            if len(cells) > 1:
                lastname_elements = cells[1].getElementsByType(P)
                if len(lastname_elements) > 0:
                    lastname = "".join([str(text) for text in lastname_elements[0].childNodes]).strip().lower()
            if firstname and lastname:
                students.append({"firstname": firstname, "lastname": lastname})
    else:
        raise ValueError("Unsupported file format")
    
    return students

# Vérifiez que le fichier de données est passé en argument
if len(sys.argv) != 2:
    print("Usage: python3 add_site.py <path_to_student_file>")
    sys.exit(1)

file_path = sys.argv[1]

# Load environment variables
load_dotenv()
site_url = os.getenv("SITE_COMPLETE_URL")
admin_user = os.getenv("ADMIN_USER")
admin_email = os.getenv("ADMIN_EMAIL")
user_email = os.getenv("USER_EMAIL")
smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
smtp_port = int(os.getenv("SMTP_PORT", 465))
smtp_user = os.getenv("SMTP_USER")
smtp_password = os.getenv("SMTP_PASSWORD")
test = os.getenv("TEST")

students = load_students(file_path)

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
    username = student["firstname"] + student["lastname"]
    new_site_slug = student["firstname"] + student["lastname"]
    new_site_title = student["firstname"] + " " + student["lastname"]
    password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))

    # Create user
    command_user_create = [
        'wp', 'user', 'create', username, student["firstname"] + '.' + student["lastname"] + user_email,
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
            '--email={}'.format(student["firstname"] + '.' + student["lastname"] + user_email),
            '--allow-root'
        ]

        result_site_create = subprocess.run(command_site_create, capture_output=True, text=True)

        if result_site_create.returncode == 0:
            print(f"Sous-site pour {student['firstname']} {student['lastname']} créé avec succès!")

            # Send email with initial password
            login_url = f"{site_url}/wp-login.php"
            
            if test:
                
                subject = "Compte eCV Wordpress [À l'attention des testeurs]"
                body = f"""
                Bonjour {student['firstname']} {student['lastname']}, tu as été invité à participer au test du service d'eCV de JrCanDev !
                
                Ton rôle en tant que testeur est le suivant :
                
                - Tester et simuler la réalisation de ton eCV avec wordpress
                - Remonter les potientiels bugs rencontrés (à Nathan Fourny)
                - Proposer des améliorations pour le service (plugins, fonctionnalités, automatisations, etc...)
                
                Merci d'avance pour ta contribution au sein de ce projet, toute l'équipe de JrCanDev te remercie !

                Voici tes logins :

                Username: {username}
                Password: {password}

                Tu peux te connecter à ton site en utilisant l'adresse suivante:
                {login_url}

                Nous t'invitons à changer ton mot de passe dans tes paramètres utilisateur.

                Cordialement,
                {admin_user}
                """

                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['From'] = admin_email
                msg['To'] = student["firstname"] + '.' + student["lastname"] + user_email
                
            else:
            
                subject = "Compte Wordpress"
                body = f"""
                Bonjour {student['firstname']} {student['lastname']},

                Ton compte a été crée avec succès ! Voici tes logins :

                Username: {username}
                Password: {password}

                Tu peux te connecter à ton site en utilisant l'addresse suivante:
                {login_url}

                Nous t'invitons à changer ton mot de passe dans tes paramètres utilisateur.

                Cordialement,
                {admin_user}
                """

                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['From'] = admin_email
                msg['To'] = student["firstname"] + '.' + student["lastname"] + user_email

            try:
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    server.login(smtp_user, smtp_password)
                    server.sendmail(admin_email, [student["firstname"] + '.' + student["lastname"] + user_email], msg.as_string())
                print(f"Email contenant le mot de passe initial envoyé à {student['firstname'] + '.' + student['lastname'] + user_email}!")
                    
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
        
    # Wait 5 seconds between each user creation    
    time.sleep(5)
