from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Login")


class LinkForm(FlaskForm):
    gsid = StringField("Game Sync ID")
    submit = SubmitField("Link!")
