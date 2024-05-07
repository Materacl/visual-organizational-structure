# Routes for parent Flask app
from flask import current_app as app, current_app
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message

from visual_organizational_structure import db, mail
from visual_organizational_structure.models import User, Dashboard
from visual_organizational_structure.forms import ResetPasswordForm, RequestResetForm, RegisterForm, LoginForm

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

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("home"))
    else:
        flash('проблема с валидацией')
    return render_template("login.jinja2", title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()
    if form.validate_on_submit():
        hash_password = generate_password_hash(form.password.data)
        new_user = User(password=hash_password, email=form.email.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return redirect(url_for('register'))

    return render_template('register.jinja2', title='Register', form=form)


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
        flash('На вашу почту было отправлено письмо с инструкциями', 'info')
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
        return redirect(url_for('request_reset_password'))
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
