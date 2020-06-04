from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms import StringField, TextAreaField, SubmitField, TextField
from wtforms.validators import DataRequired, Length
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    about_me = TextAreaField('О себе', validators=[Length(min=0, max=140)])
    submit = SubmitField('Сохранить')

class EditPostForm(FlaskForm):
    body = TextAreaField('Содержание', validators=[Length(min=0, max=140)])
    author = StringField('Имя', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Сбросить пароль')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class ThingForm(FlaskForm):
    submit = SubmitField('Добавить в корзину')

class InformationAboutOrder(FlaskForm):
    fio = StringField('ФИО', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    phone = StringField('Номер телефона', validators=[DataRequired()])
    mail = StringField('Почта', validators=[DataRequired()])
    index = StringField('Почтовый индекс', validators=[DataRequired()])
