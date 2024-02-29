import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_session import Session
from flask_login import LoginManager, login_user, UserMixin
from secompanion.apps.forms import LoginForm, RegistrationForm, ProfileForm
from secompanion.apps.models import User, db
from flask_migrate import Migrate
from flask_mail import Mail, Message  # Import necessary modules
from secompanion.apps.forms import ForgotPasswordForm
from werkzeug.utils import secure_filename
import secrets
import string


# Import the function for sending password reset email
from secompanion.apps.methods import send_password_reset_email, filter_resources

app = Flask(__name__, template_folder='apps/templates')

# Configure Flask-Mail with your email server settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = True
# Update with your Gmail address
app.config['MAIL_USERNAME'] = 'hakeemabdullah87@gmail.com' 
# Update with your Gmail app password or account password if less secure apps
app.config['MAIL_PASSWORD'] = 'abdul4prof87'  
mail = Mail(app)  # Initialize Flask-Mail

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = b'8\xc6\xef\xd8\x82\xf86\xe5R\x10\xb3\x9f\xb8k\xf0{\x88-\xc4\xde\x8eQ\x05;'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:abdul4prof@localhost/secompanion'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html', form=form)

# Route to handle form submission
@app.route('/forgot_password', methods=['GET', 'POST'], endpoint='forgot_password')
def handle_forgot_password():
    form = ForgotPasswordForm()
    if request.method == 'POST':
        # Check if 'email' exists in the form data
        if 'email' in request.form:
            email = request.form['email']
            # Generate a unique token for password reset
            token = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(16))
            # Send password reset email using Flask-Mail
            send_password_reset_email(email, token)
            flash('Password reset instructions sent to your email.', 'success')
            return redirect(url_for('forgot_password'))
        else:
            flash('Email not provided.', 'error')
            return redirect(url_for('forgot_password'))
    # Render the forgot password form for GET requests
    return render_template('forgot_password.html', form=form)

# Route for password reset page
@app.route('/reset_password/<token>', methods=['GET'])
def reset_password(token):
    #logic to handle password reset
    # Render the HTML page for password reset
    return render_template('reset_password.html', token=token)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # You'll need to create a registration form class
    if form.validate_on_submit():
        # Check if the user already exists in the database
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Account already exists. Please log in.', 'error')
        else:
            # Create a new user account
            new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been created successfully!', 'success')
            # Redirect to the login page after successful registration
            return redirect(url_for('login')) 
    return render_template('register.html', form=form)


@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        # Handle file upload
        if form.photo.data:
            filename = secure_filename(form.photo.data.filename)
            form.photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Photo uploaded successfully!', 'success')
        else:
            # Generate default avatar using first letters of first and last name
            default_avatar_filename = '{}{}.png'.format(form.first_name.data[0], form.last_name.data[0])
            default_avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], default_avatar_filename)
            # Check if default avatar already exists
            if not os.path.exists(default_avatar_path):
                # Generate and save default avatar
                # Here's a simple example using PIL:
                from PIL import Image, ImageDraw, ImageFont
                avatar_size = (100, 100)
                default_avatar = Image.new('RGB', avatar_size, color='white')
                draw = ImageDraw.Draw(default_avatar)
                font = ImageFont.load_default()
                draw.text((25, 25), '{}{}'.format(form.first_name.data[0], form.last_name.data[0]), fill='black', font=font)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Create uploads directory if it doesn't exist
                default_avatar.save(default_avatar_path)
                flash('Default avatar created!', 'info')
    if form.validate_on_submit():
        # Here you would typically process the form data, save it to a database, etc.
        # For demonstration purposes, let's just print the form data.
        print("Form data:", form.data)
        return redirect(url_for('index'))
    return render_template('profile.html', form=form)

# Hardcoded resources
resources = [
    {"title": "Resource 1", "type": "Video", "category": "Web Development", "level": "Beginner"},
    {"title": "Resource 2", "type": "Book", "category": "Data Science", "level": "Intermediate"},
    {"title": "Resource 3", "type": "Article", "category": "Python Development", "level": "Expert"},
    # Add more resources as needed
]

# Categories
categories = ["Web Development", "Data Science", "Python Development"]

@app.route('/learn_resources', methods=['GET', 'POST'])
def learn_resources():
    if request.method == 'POST':
        search_query = request.form['search']
        type_filter = request.form.get('type_filter')
        category_filter = request.form.get('category_filter')
        level_filter = request.form.get('level_filter')
        
        # Pass the resources list to the filter_resources function
        filtered_resources = filter_resources(search_query, type_filter, category_filter, level_filter, resources)
        
        return render_template('learn_resources.html', resources=filtered_resources, categories=categories)
    
    return render_template('learn_resources.html', resources=resources, categories=categories)

if __name__ == '__main__':
    app.run(debug=True)
