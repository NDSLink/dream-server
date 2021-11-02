# --- Imports ---
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from redis import Redis
from config import Config
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_babel import Babel, _

from os.path import exists

# --- Key Definitions ---
app = Flask(__name__)
bootstrap = Bootstrap(app)
babel = Babel(app)
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['ja'])
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

# --- Main Block ---
if __name__ == "__main__":
    app.run(host="0.0.0.0")
