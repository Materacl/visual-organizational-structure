"""Routes for parent Flask app."""
from flask import current_app as app
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from main_app import db
from main_app.models import User


@app.route("/")
def home():
    """Home page of Flask Application."""
    return render_template(
        "index.jinja2",
        title="Home page",
        description="Home page.",
        template="home-template",
        body="This is a homepage served with Flask.",
        base_url=request.base_url,
    )


@app.route('/login', methods=['GET, POST'])
def login():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page)
        else:
            flash('Логин или пароль некорректны')
    else:
        flash('Введите логин и пароль')

    return render_template('login.jinja2')


@app.route('/register', methods=['GET, POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Заполните все поля')
        elif password != password2:
            flash('Пароли не совпадают')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))

    return render_template('register.jinja2')


@app.route('/logout', methods=['GET, POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('/'))


@app.after_request
def redirect_to_signin(response):
    if response.status == 401:
        return redirect(url_for('login_page')+'?next='+request.url)
    return response