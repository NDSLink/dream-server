from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_babel import lazy_gettext as _l


class LoginForm(FlaskForm):
    username = StringField(_l("Trainer Name"))
    gsid = StringField(_l("Game Sync ID"))
    password = PasswordField(_l("Password"))
    submit = SubmitField(_l("Login"))


class LinkForm(FlaskForm):
    gsid = StringField(_l("Game Sync ID"))
    submit = SubmitField(_l("Download Save!"))

class WhatPokeForm(FlaskForm):
    poke = StringField(_l("Who's that Pokemon?"))
    submit = SubmitField(_l("Submit"))

class LinkPwForm(FlaskForm):
    gsid = StringField(_l("Game Sync ID"))
    username = StringField(_l("Trainer Name"))
    password = PasswordField("Password")
    submit = SubmitField(_l("Link!"))
