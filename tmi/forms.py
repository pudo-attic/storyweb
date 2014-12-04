from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms import validators


class LoginForm(Form):
    email = StringField('E-Mail', validators=[validators.Email()])
    password = PasswordField('Password', validators=[validators.required()])
