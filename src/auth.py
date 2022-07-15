from flask import Blueprint

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post("/register")
def register():
    return "User registered"


@auth.get("/me")
def me():
    return "User authenticated"
