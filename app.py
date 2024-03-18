import os
import random
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_required
#from flask_session import Session
from flask_login import LoginManager, login_user, UserMixin
from secompanion.apps.forms import LoginForm, RegistrationForm, ProfileForm, ForgotPasswordForm
from secompanion.apps.models import User, db, Interest, Skill, Connection,Tool,Resource
from flask_migrate import Migrate
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import secrets
import string
from secompanion.apps.methods import send_password_reset_email, filter_resources, get_daily_quote

app = Flask(__name__, template_folder='apps/templates')
app.static_folder = 'apps/static'
# implementing app  for email configuration 
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'hakeemabdullah87@gmail.com'
app.config['MAIL_PASSWORD'] = 'abdul4prof87'
mail = Mail(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# implementing configuration for Database 
app.config['SECRET_KEY'] = b'8\xc6\xef\xd8\x82\xf86\xe5R\x10\xb3\x9f\xb8k\xf0{\x88-\xc4\xde\x8eQ\x05;'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:abdul4prof@localhost/secompanion'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'

#Session(app)
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

#Creating various API endpoints for web application
#Login endpoint
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html', form=form)

@app.route('/forgot_password', methods=['GET', 'POST'], endpoint='forgot_password')
def handle_forgot_password():
    form = ForgotPasswordForm()
    if request.method == 'POST':
        if 'email' in request.form:
            email = request.form['email']
            token = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(16))
            send_password_reset_email(email, token)
            flash('Password reset instructions sent to your email.', 'success')
            return redirect(url_for('forgot_password'))
        else:
            flash('Email not provided.', 'error')
            return redirect(url_for('forgot_password'))
    return render_template('forgot_password.html', form=form)

@app.route('/reset_password/<token>', methods=['GET'])
def reset_password(token):
    return render_template('reset_password.html', token=token)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Account already exists. Please log in.', 'error')
        else:
            hashed_password = generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            #new_user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been created successfully!', 'success')
            return redirect(url_for('login')) 
    return render_template('register.html', form=form)
@app.route('/dashboard/dashboard', methods=['GET','POST'])
@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    #user_id = session.get('user_id')  # Or however you get the user_id
    #print("User ID:", user_id)  # Add this line for debugging
    categories = ['sucess','productivity','leadership', 'inspiration', 'work', 'time', 'today', 'pain']
    selected_category = random.choice(categories)
    quote = get_daily_quote(selected_category)
    if quote:
        daily_quotes=quote
    else:
        daily_quotes = "No quote found today."
    return render_template('/dashboard/dashboard.html', username=current_user.username, quote=daily_quotes)

@app.route('/dashboard/profile', methods=['GET', 'POST'])
def profile():
    user = User.query.get(current_user.id) 
    form = ProfileForm(obj=user)
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(user)
        if form.photo.data:  # Check if photo was uploaded
            filename = secure_filename(form.photo.data.filename)
            form.photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            user.avatar_image = filename  # Store the filename in the database
            flash('Photo uploaded successfully!', 'success')
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('dashboard'))  # Redirect to the dashboard page after profile update
    return render_template('dashboard/profile.html', form=form, user=user)


resources = [
    {"title": "Resource 1", "type": "Video", "category": "Web Development", "level": "Beginner"},
    {"title": "Resource 2", "type": "Book", "category": "Data Science", "level": "Intermediate"},
    {"title": "Resource 3", "type": "Article", "category": "Python Development", "level": "Expert"},
]

categories = ["Web Development", "Data Science", "Python Development"]

@app.route('/dashboard/learn_resources', methods=['GET', 'POST'])
def learn_resources():
    if request.method == 'POST':
        search_query = request.form['search']
        type_filter = request.form.get('type_filter')
        category_filter = request.form.get('category_filter')
        level_filter = request.form.get('level_filter')
        filtered_resources = filter_resources(search_query, type_filter, category_filter, level_filter, resources)
        return render_template('dashboard/learn_resources.html', resources=filtered_resources, categories=categories)
    return render_template('dashboard/learn_resources.html', resources=resources, categories=categories)

@app.route('/dashboard/tools')
def tools():
    return render_template('dashboard/tools.html')

@app.route('/dashboard/overview')
def overview():
    return render_template('dashboard/sengineer.html')

@app.route('/dashboard/overview/python_dev')
def python_dev():
    return render_template('dashboard/python_dev.html')

@app.route('/dashboard/logout')
def logout():
    session.clear()
    return render_template('dashboard/logout.html')

if __name__ == '__main__':
    app.run(debug=True)
