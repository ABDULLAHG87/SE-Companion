import secrets
import string
import smtplib
from email.mime.text import MIMEText


# Function to send password reset email
def send_password_reset_email(email, token):
    # Configure email server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('hakeemabdullah87@gmail.com', 'abdul4prof87')

    # Compose email message
    msg = MIMEText(f'Click the link to reset your password: http://localhost:5000/reset_password/{token}')
    msg['Subject'] = 'Password Reset Request'
    msg['From'] = 'hakeemabdullah87@gmail.com'
    msg['To'] = email

    # Send email
    server.sendmail('hakeemabdullah87@gmail.com', email, msg.as_string())
    server.quit()