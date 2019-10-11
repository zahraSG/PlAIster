from flask import Blueprint, render_template, url_for, flash, redirect
from dashboard import db, bcrypt
from dashboard.users.forms import RegistrationForm, LoginForm
from dashboard.models import User,Postdevice  # we move this below db to remove errors for db
from flask_login import login_user, current_user, logout_user


users = Blueprint('users',__name__)

@users.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect (url_for('main.home'))
    form= RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf_8')
        user =  User(username = form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! you can be able to login','success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)



@users.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect (url_for('main.home'))
    form= LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # if the user exists and the password that is entered is valid with what is saved in the databse log the user in
            login_user(user, remember = form.remember.data)
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful, Please check email and password','danger')
    return render_template('login.html', title='login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))
