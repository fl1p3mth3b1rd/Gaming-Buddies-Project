from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, IntegerField, TextField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Никнейм пользователя', validators=[DataRequired()], render_kw={'class':'form-control'})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'class':'form-control'})
    remember_me = BooleanField('Запомнить меня', render_kw={'class':'form-check-input'})
    submit = SubmitField('Отправить', render_kw={'class':'btn btn-primary'})

class RegistrationForm(FlaskForm):
    username = StringField('Никнейм пользователя', validators=[DataRequired()], render_kw={'class':'form-control'})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'class':'form-control'})
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')], render_kw={'class':'form-control'})
    email = StringField('email', validators=[DataRequired(), Email()], render_kw={'class':'form-control'})
    first_name = StringField('Имя пользователя', render_kw={'class':'form-control'})
    second_name = StringField('Фамилия пользователя', render_kw={'class':'form-control'})
    birth_date = DateField('Дата рождения', render_kw={'class':'form-control'})
    gender = StringField('Пол', render_kw={'class':'form-control'})
    submit = SubmitField('Отправить', render_kw={'class':'btn btn-primary'})

class LookingForGamersForm(FlaskForm):
    country = StringField('Страна', validators=[DataRequired()], render_kw={'class':'form-control'})
    time_zone = StringField('Часовой пояс', validators=[DataRequired()], render_kw={'class':'form-control'})
    description_as_author = TextField('Описание', validators=[DataRequired()], render_kw={'class':'form-control'})
    purpose_as_author = StringField('Цель', validators=[DataRequired()], render_kw={'class':'form-control'})
    discord = StringField('Discord', validators=[DataRequired()], render_kw={'class':'form-control'})
    prime_time = StringField('Прайм-тайм', validators=[DataRequired()], render_kw={'class':'form-control'})
    submit = SubmitField('Отправить', render_kw={'class':'btn btn-primary'})
