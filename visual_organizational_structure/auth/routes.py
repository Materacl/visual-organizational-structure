from visual_organizational_structure.auth import bp

from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message

from visual_organizational_structure.database import db
from visual_organizational_structure.utils import mail
from visual_organizational_structure.models import User, Dashboard
from visual_organizational_structure.forms import ResetPasswordForm, RequestResetForm, RegisterForm, LoginForm


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.home"))
    return render_template("login.jinja2", title='Login', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hash_password = generate_password_hash(form.password.data)
        new_user = User(password=hash_password, email=form.email.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        except:
            return redirect(url_for('auth.register'))

    return render_template('register.jinja2', title='Register', form=form)


@login_required
@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@bp.route('/reset_password', methods=['GET', 'POST'])
def request_reset_password():
   # if current_user.is_authenticated:
#    return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('На вашу почту было отправлено письмо с инструкциями', 'info')
        return redirect(url_for('auth.login'))
    return render_template('request_reset_password.jinja2', title='Reset Password', form=form)


@login_required
@bp.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.request_reset_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Ваш пароль был успешно изменен!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reset_token.jinja2', title='Reset Password', form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@bp.after_request
def redirect_to_signin(response):
    if response.status == 401:
        return redirect(url_for('auth.login') + '?next=' + request.url)
    return response
