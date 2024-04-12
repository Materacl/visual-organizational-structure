# Routes for parent Flask app
from flask import current_app as app, current_app
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from main_app import db
from main_app.models import User, Dashboard

from .dash_apps.organization_graph.dashboard import init_dashboard


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            flash('Логин или пароль некорректны')
    else:
        flash('Введите логин и пароль')

    return render_template('login.jinja2')


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not (login and password and password2):
            flash('Заполните все поля')
        elif password != password2:
            flash('Пароли не совпадают')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))

    return render_template('register.jinja2')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.after_request
def redirect_to_signin(response):
    if response.status == 401:
        return redirect(url_for('login') + '?next=' + request.url)
    return response


@app.route('/create_dashboard', methods=['POST'])
@login_required
def create_dashboard():
    name = request.form.get('name')

    if name:
        new_dashboard = Dashboard(name=name, user_id=current_user.id)
        db.session.add(new_dashboard)
        db.session.commit()
        flash('Dashboard created successfully!')

        # Redirect to the new dashboard's URL
        return redirect(url_for('view_dashboard', dashboard_id=new_dashboard.id))
    else:
        flash('Name is required for the dashboard')

    return redirect(url_for('home'))


@app.route('/dashboard/<int:dashboard_id>')
@login_required
def view_dashboard(dashboard_id):
    dashboard = Dashboard.query.get(dashboard_id)

    if dashboard.user_id != current_user.id:
        flash('Unauthorized access')
        return redirect(url_for('home'))

    # Redirect to the correct URL
    return redirect(f'org-structure/{dashboard_id}')


@app.route('/delete_dashboard/<int:dashboard_id>', methods=['POST'])
@login_required
def delete_dashboard(dashboard_id):
    dashboard = Dashboard.query.get(dashboard_id)

    if dashboard.user_id != current_user.id:
        flash('Unauthorized access')
        return redirect(url_for('home'))

    db.session.delete(dashboard)
    db.session.commit()
    flash('Dashboard deleted successfully!')

    return redirect(url_for('home'))
