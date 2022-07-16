from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import validators
from src.constants.http_status_codes import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from src.database import User, db

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post("/register")
def register():
    try:
        email = request.json.get("email")
        password = request.json.get("password")

        if email is None or password is None:
            return (
                jsonify({"message": "Missing email or password."}),
                HTTP_400_BAD_REQUEST,
            )

        if len(password) < 8:
            return (
                jsonify(
                    {"message": "Password must be at least 8 characters long."}
                ),
                HTTP_400_BAD_REQUEST,
            )

        if not validators.email(email):
            return (
                jsonify({"message": "Invalid email."}),
                HTTP_400_BAD_REQUEST,
            )

        if User.query.filter_by(email=email).first() is not None:
            return (
                jsonify({"message": "Email is taken."}),
                HTTP_409_CONFLICT,
            )

        hashed_password = generate_password_hash(password)
        user = User(email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return (
            jsonify({"message": "User created.", "user": {"email": email}}),
            HTTP_201_CREATED,
        )
    except:
        return (
            jsonify({"message": "Something went wrong."}),
            HTTP_500_INTERNAL_SERVER_ERROR,
        )


@auth.get("/me")
def me():
    return "User authenticated"
