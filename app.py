# --- Imports ---
from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from redis import Redis
from config import Config
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_babel import Babel, _

is_circ_import = False

from os.path import exists

# --- Key Definitions ---
app = Flask(__name__)
bootstrap = Bootstrap(app)
babel = Babel(app)


@babel.localeselector
def get_locale():
    if request.args.get("lang", None):
        return request.args["lang"]
    return request.accept_languages.best_match(["en", "ja"])


app.config.from_object(Config)

if app.config["USE_REDIS"]:
    redis = Redis(host=app.config["REDIS_HOST"], port=app.config["REDIS_PORT"], db=0)
else:
    from redismock import DummyRedis

    redis = DummyRedis()
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# --- Routes ---
import routes

try:
    app.register_blueprint(routes.main_routes)
except AttributeError:
    pass

# --- Main Block ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
