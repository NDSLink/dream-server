from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class LoginForm(FlaskForm):
    username = StringField("Trainer Name")
    gsid = StringField("Game Sync ID")
    password = PasswordField("Password")
    submit = SubmitField("Login")


class LinkForm(FlaskForm):
    gsid = StringField("Game Sync ID")
    submit = SubmitField("Link!")

class LinkPwForm(FlaskForm):
    gsid = StringField("Game Sync ID")
    password = PasswordField("Password")
    submit = SubmitField("Link!")
