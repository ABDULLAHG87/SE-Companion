import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_session import Session
from flask_login import LoginManager, login_user, UserMixin
from secompanion.apps.forms import LoginForm, RegistrationForm
from secompanion.apps.models import User, db
from flask_migrate import Migrate


#libraries for email sending
import secrets
import string
import smtplib
from email.mime.text import MIMEText

import apps.methods as methods

app = Flask(__name__, template_folder='apps/templates')
app.config['SECRET_KEY'] = b'8\xc6\xef\xd8\x82\xf86\xe5R\x10\xb3\x9f\xb8k\xf0{\x88-\xc4\xde\x8eQ\x05;'
basedir = os.path.abspath(os.path.dirname(__file__))
#Using the SQLite
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
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
    return 'Hello, World!'

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
@app.route('/forgot_password', methods=['POST'])
def handle_forgot_password():
    email = request.form['email']
    # Generate a unique token for password reset
    token = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(16))
    # Send password reset email
    methods.send_password_reset_email(email, token)
    flash('Password reset instructions sent to your email.', 'success')
    return redirect(url_for('forgot_password'))

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
            return redirect(url_for('login'))  # Redirect to the login page after successful registration
    return render_template('register.html', form=form)


@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
