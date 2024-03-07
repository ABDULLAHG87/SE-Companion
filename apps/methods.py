from flask_mail import Mail, Message
from flask import Flask
import requests
import random



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
    '''Function that reset password via email'''
    # Compose email message
    msg = Message('Password Reset Request', sender='hakeemabdullah87@gmail.com', recipients=[email])
    msg.body = f'Click the link to reset your password: http://localhost:5000/reset_password/{token}'

    # Send email
    mail.send(msg)
#function to filter resources in the resources page based on filter or search query
def filter_resources(search_query, type_filter, category_filter, level_filter,resources):
    '''Function to filter resources based on search query and filters'''
    filtered_resources = resources
    
    if search_query:
        filtered_resources = [resource for resource in filtered_resources if search_query.lower() in resource['title'].lower()]
        
    if type_filter and type_filter != 'Filter by Type':
        filtered_resources = [resource for resource in filtered_resources if resource['type'] == type_filter]
        
    if category_filter and category_filter != 'Filter by Category':
        filtered_resources = [resource for resource in filtered_resources if resource['category'] == category_filter]
        
    if level_filter and level_filter != 'Filter by Level':
        filtered_resources = [resource for resource in filtered_resources if resource['level'] == level_filter]
        
    return filtered_resources

def get_daily_quote(category):
    '''Function to get a random quote from the ZenQuotes API'''
    try:
        url = f'https://zenquotes.io/api/quotes/{category}'
        response = requests.get(url)
        data = response.json()
        info = []
        if data:
            quote = random.choice(data)
            return quote
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None
    except KeyError as e:
        return None
        