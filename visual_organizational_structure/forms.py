from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from visual_organizational_structure.models import User




class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email("Некорректная почта")])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Аккаунта с такой почтой не существует')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message = 'Пароли не совпадают')])
    submit = SubmitField('Сменить пароль')