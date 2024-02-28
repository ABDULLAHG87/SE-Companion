from flask_mail import Mail, Message
from flask import Flask

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'hakeemabdullah87@gmail.com'
app.config['MAIL_PASSWORD'] = 'abdul4prof87'

mail = Mail(app)

# Function to send password reset email
def send_password_reset_email(email, token):
    # Compose email message
    msg = Message('Password Reset Request', sender='hakeemabdullah87@gmail.com', recipients=[email])
    msg.body = f'Click the link to reset your password: http://localhost:5000/reset_password/{token}'

    # Send email
    mail.send(msg)