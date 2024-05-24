from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from visual_organizational_structure.models import User


class RequestResetForm(FlaskForm):
    email = StringField(
        "Почта", validators=[DataRequired(), Email("Некорректная почта")]
    )
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("Аккаунта с такой почтой не существует")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Пароль", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Сменить пароль")


class RegisterForm(FlaskForm):
    email = StringField(
        "Почта",
        validators=[DataRequired(), Email(message="Некорректная почта")],
        render_kw={"placeholder": "example@mail.ru"},
    )
    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(),
            Length(min=8, max=100, message="Пароль должен быть длиннее 8 символов"),
        ],
        render_kw={"placeholder": "Введите пароль"},
    )
    password_retry = PasswordField(
        "Повторите пароль",
        validators=[
            DataRequired(),
            Length(min=8, max=100),
            EqualTo("password", message="Пароли не совпадают"),
        ],
        render_kw={"placeholder": "Повторите пароль"},
    )

    submit = SubmitField("Регистрация")


class LoginForm(FlaskForm):
    email = StringField(
        "Почта",
        validators=[DataRequired(), Email(message="Некорректная почта")],
        render_kw={"placeholder": "example@mail.ru"},
    )
    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(),
            Length(min=8, max=100, message="Пароль должен быть длиннее 8 символов"),
        ],
        render_kw={"placeholder": "Введите пароль"},
    )

    submit = SubmitField("Войти")
