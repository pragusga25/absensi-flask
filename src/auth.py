from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import validators
from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
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


@auth.post("/login")
def login():
    try:
        email = request.json.get("email")
        password = request.json.get("password")

        if email is None or password is None:
            return (
                jsonify({"message": "Missing email or password."}),
                HTTP_400_BAD_REQUEST,
            )

        user = User.query.filter_by(email=email).first()

        if user:
            is_password_correct = check_password_hash(user.password, password)
            if is_password_correct:
                identity = {"uid": user.id, "is_checkin": False}
                refresh_token = create_refresh_token(identity=identity)
                access_token = create_access_token(identity=identity)

                return (
                    jsonify(
                        {
                            "message": "Login successful.",
                            "user": {
                                "email": user.email,
                                "refresh_token": refresh_token,
                                "access_token": access_token,
                            },
                        }
                    ),
                    HTTP_200_OK,
                )

        return (
            jsonify({"message": "Wrong credentials."}),
            HTTP_401_UNAUTHORIZED,
        )
    except:
        return (
            jsonify({"message": "Something went wrong."}),
            HTTP_500_INTERNAL_SERVER_ERROR,
        )


@auth.get("/me")
@jwt_required()
def me():
    return "User authenticated"
