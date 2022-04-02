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
    submit = SubmitField(_l("Link!"))

class LinkPwForm(FlaskForm):
    gsid = StringField(_l("Game Sync ID"))
    password = PasswordField("Password")
    submit = SubmitField(_l("Link!"))
