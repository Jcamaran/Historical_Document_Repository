from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_principal import Identity  # Import identity here
from .forms import LoginForm, RegistrationForm
from .models import User
from .extensions import db
from flask_login import login_user, logout_user

auth = Blueprint('auth', __name__)

# Existing login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(request.args.get('next') or url_for('app_views.index'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

# New registration route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Identity check example
@auth.route('/protected')
def protected_route():
    if Identity:
        # Access identity attributes or perform actions based on the user's identity
        user_id = Identity.id
        username = Identity.name
        return f"Welcome, {username}! Your user ID is {user_id}."
    else:
        flash('You need to log in to access this page.', 'warning')
        return redirect(url_for('auth.login'))
