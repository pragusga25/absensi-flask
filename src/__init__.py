from flask import Flask
import os
from src.auth import auth
from src.activities import activities
from src.attendances import attendances
from src.database import TokenBlocklist, db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

    Migrate(app, db)

    app.register_blueprint(auth)
    app.register_blueprint(activities)
    app.register_blueprint(attendances)

    return app
