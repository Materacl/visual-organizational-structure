# Routes for parent Flask app
from flask import current_app as app, current_app
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message

from visual_organizational_structure import db, mail
from visual_organizational_structure.models import User, Dashboard
from visual_organizational_structure.forms import ResetPasswordForm, RequestResetForm

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
            next_page = request.args.get("next")
            return redirect(next_page or url_for("home"))
        else:
            flash("Логин или пароль некорректны")
    else:
        flash("Введите логин и пароль")

    return render_template("login.jinja2")


def check_new_password(password: str, password_retry: str) -> bool:
    """
    new password verification
    :param password: password
    :param password_retry: password_retry
    :return: bool permission or prohibition to use this password
    """
    if len(password) < 1 and len(password_retry) < 1:
        flash('Заполните все поля')
        return False
    elif len(password) < 7:
        flash('Пароль должен быть длинее 8 символов')
        return False
    elif password != password_retry:
        flash('Пароли не совпадают')
        return False
    else:
        return True


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if check_new_password(password, password2):
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd, email=email)
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))
            except:
                flash('Ошибка при добавлении пользователя в БД')
                return redirect(url_for('register'))

    return render_template('register.jinja2')


@login_required
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/reset_password', methods=['GET', 'POST'])
def request_reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('request_reset_password.jinja2', title='Reset Password', form=form)


@login_required
@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.jinja2', title='Reset Password', form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


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

        # Redirect to the new dashboard's URL
        return redirect(url_for('view_dashboard', dashboard_id=new_dashboard.id))
    else:
        pass

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
        flash("Unauthorized access")
        return redirect(url_for("home"))

    db.session.delete(dashboard)
    db.session.commit()
    flash("Dashboard deleted successfully!")

    return redirect(url_for("home"))


@app.route("/settings", methods=["GET", "POST"])
def settings():
    return render_template("settings.jinja2")
