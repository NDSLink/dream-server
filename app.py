"""
MIT License

Copyright (c) 2022 DSLink Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
# --- Imports ---
from http import HTTPStatus
from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from redis import Redis
from config import Config
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_babel import Babel, _

# --- Key Definitions ---
app = Flask(__name__)
bootstrap = Bootstrap(app)
babel = Babel(app)

def get_locale():
    if request.args.get("lang", None):
        return request.args["lang"]
    return request.accept_languages.best_match(["en", "ja"])

babel.init_app(app, locale_selector=get_locale)

app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login = LoginManager(app)


if app.config["USE_REDIS"]:
    redis = Redis(host=app.config["REDIS_HOST"], port=app.config["REDIS_PORT"], db=0)
else:
    from redismock import DummyRedis

    redis = DummyRedis()


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html.jinja2", title=_("Page Not Found")), 404


@app.before_request
def before_request():
    request.data  # funky bug in flask


# --- Routes ---
from routes import main_routes
from cosmetics import cosmetics
from dsio import backend

app.register_blueprint(cosmetics)
app.register_blueprint(main_routes)
app.register_blueprint(backend)

from models import User


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# --- Main Block ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
