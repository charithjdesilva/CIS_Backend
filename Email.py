import os
from dotenv import load_dotenv
import smtplib

from email.mime.text import MIMEText

load_dotenv()

myEmail = os.environ.get('MYEMAIL')
smtp_server = os.environ.get('SMTP_SERVER')
smtp_port = os.environ.get('SMTP_PORT')
password = os.environ.get('PASSWORD')

# os.getenv('MY_ENV_VAR')
# print(os.environ.get('SMTP_PORT'))






def send_email(msg : str , subject : str):
    msg = MIMEText(msg)
    msg['Subject'] = subject
    msg['From'] = myEmail
    msg['To'] = myEmail

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(myEmail,password)

    server.send_message(msg)
    server.quit()

# send_email("4444", "Reset Password")
