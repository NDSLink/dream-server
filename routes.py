import json
from os import scandir
from os.path import basename
from random import choice

from flask_login import current_user, login_required, login_user, logout_user
from app import db, redis
import models
from forms import *
import helper
from flask import (
    request,
    send_from_directory,
    render_template,
    redirect,
    url_for,
    Response,
    Blueprint,
)

from wtforms import ValidationError
from dls1_client import Client
from base64 import b64encode, b64decode

from pickle import dumps
from gsid import gsid_dec, gsid_enc
from os.path import exists
from werkzeug.security import generate_password_hash, check_password_hash

# import redis
from constants import *
from flask_babel import _
from requests import post

main_routes = Blueprint("main_routes", __name__)


@main_routes.route("/")
def home():
    # return 'Hello there! This page is under construction! Why not check out <a href="https://web.archive.org/web/20110715101524id_/http://www.pokemon-gl.com/languages/">what remains of PGL</a> while you wait?'
    return render_template("home.html.jinja2", title=_("Home"))


@main_routes.route("/savedata", methods=["GET", "POST"])
def savedata():
    form = LinkForm()
    if form.validate_on_submit():
        return redirect(url_for("main_routes.get_savedata", trainerid=gsid_dec(form.gsid.data)))
    return render_template(
        "savedata.html.jinja2", form=form, title=_("Manage Save Data")
    )


@main_routes.route("/savedata/<trainerid>")
def get_savedata(trainerid):
    u = models.GSUser.query.filter_by(id=trainerid).first()
    if u == None:
        if exists(f"savdata-{trainerid}.sav"):
            return send_from_directory(".", f"savdata-{trainerid}.sav")
    return send_from_directory(".", f"savdata-{u.id}.sav")

@main_routes.route("/radar")
@login_required
def use_radar():
    # Basic functionality for catching Pokemon
    return render_template("radar.html.jinja2")

# @app.route("/users")
# def users():
#    return f"Hello! To view user information, go to {url_for('users')}/<your GSID>. For instance, if your GSID is AAAAAAA2EE, go to {url_for('users')}/AAAAAAA2EE. Note: this will have a better look soon!"


@main_routes.route("/users/<gsid>")
def user_gsid(gsid):
    gu = models.GSUser.query.filter_by(id=gsid).first()
    u = models.User.query.filter_by(id=gu.uid).first()
    return render_template("user.html.jinja2", title=_("User ") + u.username, user=u, gsuser=gu)

@main_routes.route("/users/me")
def user_me():
    u = models.User.query.filter_by(id=current_user.id).first()
    gu = models.GSUser.query.filter_by(uid=current_user.id).first()#
    return render_template("user.html.jinja2", title=_("User ") + u.username, user=u, gsuser=gu)

@main_routes.route("/link", methods=["GET", "POST"])
def link_gsid():
    form = LinkPwForm()
    if form.validate_on_submit():
        gu = models.GSUser.query.filter_by(id=gsid_dec(form.gsid.data)).first()
        u = models.User(username=form.username.data, password_hash=generate_password_hash(form.password.data))
        gu.user = u
        db.session.add(u)
        db.session.commit()
        return redirect(url_for("main_routes.home"))
    return render_template("link.html.jinja2", title=_("Link GSID"), form=form)

@main_routes.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = models.User.query.filter_by(username=form.username.data).first()
        if u == None:
            raise ValidationError("Invalid username! Your trainer name is the one you used during account link.")
        if not check_password_hash(u.password_hash, form.password.data):
            raise ValidationError("Invalid password!")
        login_user(u)
        return redirect(url_for("main_routes.home"))
    return render_template("login.html.jinja2", title=_("Login"), form=form)

@main_routes.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main_routes.home"))


@main_routes.route("/pokemon/validate", methods=["GET", "POST"])
def validate_pokemon():
    return "\x00"