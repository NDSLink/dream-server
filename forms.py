from flask_wtf import FlaskForm
from wtforms import ValidationError
import models
from gsid import gsid_dec
from wtforms import StringField, PasswordField, SubmitField
from flask_babel import lazy_gettext as _l
from werkzeug.security import check_password_hash, generate_password_hash

class LoginForm(FlaskForm):
    username = StringField(_l("Trainer Name"))
    password = PasswordField(_l("Password"))
    submit = SubmitField(_l("Login"))
    def validate_username(self, field):
        u = models.User.query.filter_by(username=field.data).first()
        if u == None:
            raise ValidationError("Invalid username! Your trainer name is the one you used during account link.")
        if not check_password_hash(u.password_hash, self.password.data):
            raise ValidationError("Invalid password!")



class LinkForm(FlaskForm):
    gsid = StringField(_l("Game Sync ID"))
    submit = SubmitField(_l("Download Save!"))
    def validate_gsid(self, field):
        gu = models.GSUser.query.filter_by(id=gsid_dec(field.data)).first()
        if gu == None:
            raise ValidationError("Invalid GSID! Please use Game Sync Settings to set up Game Sync.")
        if gu.uid != None:
            raise ValidationError("This GSID is already linked to a user!")

class WhatPokeForm(FlaskForm):
    poke = StringField(_l("Who's that Pokemon?"))
    submit = SubmitField(_l("Submit"))

class LinkPwForm(FlaskForm):
    gsid = StringField(_l("Game Sync ID"))
    username = StringField(_l("Trainer Name"))
    password = PasswordField("Password")
    submit = SubmitField(_l("Link!"))
