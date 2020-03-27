from datetime import datetime
from flask import render_template, url_for, flash, redirect, request
from project import app, db, bcrypt
from project.users_form import SignupForm, LoginForm, ReferForm
from project.database import User, Group, Referal
from project.generate import generate_key
from flask_login import login_user, current_user, logout_user, login_required
import secrets


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title = 'Home Page')


@app.route("/about")
def about():
    return render_template("about.html", title = 'About Page')
    

@app.route("/index")
def index():
    if current_user.is_authenticated:
        chat_data = []
        grp = Group.query.filter_by(user_id=current_user.id).first()
        for value in Group.query.filter_by(title=grp.title).all():
            chat_data.append(value)
        return render_template("index.html", title = grp.title, post=chat_data)
    else:
        return redirect(url_for('about'))


@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created, try loggin in now !', 'success')
        return redirect(url_for('login'))
    return render_template("signup.html", title = 'Sign-Up Page', form = form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        grp = Group.query.filter_by(user_id=user.id).first()
        refer = Referal.query.filter_by(title=grp.title).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if refer.referal_code==form.referal_code.data and refer.title==grp.title:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('index'))
            else:
                flash('Incorrect Referal code, please check and try again', 'danger')
        else:
            flash('Login failed, please check the entries', 'danger')
    return render_template("login.html", title = 'Login Page', form = form)

@app.route("/refer", methods = ['GET', 'POST'])
@login_required
def refer():
    form = ReferForm()
    grp = Group.query.filter_by(user_id=current_user.id).first()
    referal_data = Referal.query.filter_by(title=grp.title).first()
    date = referal_data.created_date
    if form.generate.data:
        if request.method == 'POST':
            key = secrets.token_hex(3)
            create_date = datetime.utcnow()
            ref = Referal.query.filter_by(title=referal_data.title).update(dict(referal_code=key, created_date = create_date, created_by = current_user.username))
            db.session.commit()
            return redirect(url_for('refer'))
        referal_data = Referal.query.filter_by(title=grp.title).first()
    return render_template("refer.html", title = 'Referal Code', data = referal_data, date = referal_data.created_date.strftime("%c"), form = form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/account")
@login_required
def account():
    return render_template("account.html", title = 'Account Page')

