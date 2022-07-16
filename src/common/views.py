from flask import Blueprint, jsonify

from src.constants.http_status_codes import HTTP_200_OK


common = Blueprint("common", __name__, url_prefix="/")


@common.get("")
def get_common():
    return (
        jsonify(
            {
                "message": "It works!",
                "developer": "Taufik Pragusga",
                "github": "http://github.com/pragusga25",
            }
        ),
        HTTP_200_OK,
    )
