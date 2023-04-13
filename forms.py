from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=128)])
    submit = SubmitField('Login')


class RegistrationForm(LoginForm):
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=4, max=240)])
    submit = SubmitField('Add Task')
