from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import smtplib

def secret_santa(couples, participants):

    all_participants = [name for couple in couples for name in couple] + participants
    random.shuffle(all_participants)

    while True:
        valid_start = True
        for i in range(len(all_participants)):
            giver = all_participants[i]
            receiver = all_participants[(i + 1) % len(all_participants)]

            for couple in couples:
                if giver in couple and receiver in couple:
                    valid_start = False
                    break

            if not valid_start:
                random.shuffle(all_participants)
                break

        if valid_start:
            break

    assignments = {}

    for i in range(len(all_participants)):
        giver = all_participants[i]
        recipient = all_participants[(i + 1) % len(all_participants)]
        assignments[giver] = recipient

    return assignments

def send_secret_santa_emails(assignments, email_dict, sender_email, sender_password):
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    try:
        server.login(sender_email, sender_password)
    except smtplib.SMTPAuthenticationError:
        print("Failed to log in to the email server. Please check the sender's email and password.")
        return

    for giver, recipient in assignments.items():
        recipient_email = email_dict.get(giver)
        if not recipient_email:
            print(f"No email found for {giver}. Skipping.")
            continue

        message = MIMEMultipart()
        message['From'] = "Secret Santa"
        message['To'] = recipient_email
        message['Subject'] = "Secret Santa"
        body = f"Hello {giver}, your Secret Santa Friend is {recipient}."
        message.attach(MIMEText(body, 'plain'))

        try:
            server.send_message(message)
            print(f"Email sent to {giver}.")
        except Exception as e:
            print(f"Failed to send email to {giver}: {e}")

    server.quit()

couples = [("Balcan", "Diana"), ("Trincu", "Ana Hogas"), ("Cretu", "Ana Cretu"), ("Damian", "Carolina")]
participants = ["Ionut", "Animalute"]

email_dict = {
    "Trincu"    : "trincudan@gmail.com",
    "Ana Hogas" : "ahogas04@gmail.com",
    "Balcan"    : "alin.balcan9812@yahoo.com",
    "Diana"     : "dianaalexandrescu66@gmail.com",
    "Damian"    : "damiandamyan@gmail.com",
    "Carolina"  : "sumanariucarolina@yahoo.com",
    "Cretu"     : "ionut.grd18@yahoo.com",
    "Ana Cretu" : "avapasarica@gmail.com",
    "Ionut"     : "ichiriac96@gmail.com",
    "Animalute" : "trincu_dan@yahoo.ro"
}

assignments = secret_santa(couples, participants)

send_secret_santa_emails(assignments,email_dict,"email", "password")
