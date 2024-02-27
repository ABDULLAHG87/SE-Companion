import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_session import Session
from flask_login import LoginManager, login_user, UserMixin
from secompanion.apps.forms import LoginForm, RegistrationForm
from secompanion.apps.models import User, db
from flask_migrate import Migrate

app = Flask(__name__, template_folder='apps/templates')
app.config['SECRET_KEY'] = b'8\xc6\xef\xd8\x82\xf86\xe5R\x10\xb3\x9f\xb8k\xf0{\x88-\xc4\xde\x8eQ\x05;'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
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
            return redirect(url_for('profile'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html', form=form)

@app.route('/forgot_password')
def forgot_password():
    # Logic to handle forgot password functionality
    return render_template('forgot_password.html')

@app.route('/reset_password', methods=['POST'])
def reset_password():
    # Logic to handle password reset
    # Retrieve the email address from the form data
    email = request.form.get('email')
    
    # Now you can generate a password reset link and send it to the user's email address
    # You can also add additional validation and error handling here
    
    return render_template('password_reset_confirmation.html', email=email)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # You'll need to create a registration form class
    if form.validate_on_submit():
        # Logic to create a new user account
        # For example:
        new_user = User(email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created successfully!', 'success')
        
        return redirect(url_for('login'))  # Redirect to the login page after successful registration
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
