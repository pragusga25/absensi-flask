from flask import Flask
import os
from src.auth import auth
from src.activities import activities
from src.database import db
from flask_migrate import Migrate


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)
    Migrate(app, db)
    app.register_blueprint(auth)
    app.register_blueprint(activities)

    return app
