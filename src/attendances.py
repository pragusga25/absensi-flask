from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from src.constants.http_status_codes import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from src.database import Attendance, AttendanceType, User, db

attendances = Blueprint(
    "attendances", __name__, url_prefix="/api/v1/attendances"
)


@attendances.get("/")
@jwt_required()
def get_attendances():
    identity = get_jwt_identity()
    uid = identity.get("uid")

    attendances_db = Attendance.query.filter_by(user_id=uid).all()

    attendances = []
    for attendance in attendances_db:
        data = {
            "id": attendance.id,
            "type": attendance.type.name,
            "time": attendance.created_at,
        }
        attendances.append(data)

    return {
        "attendances": attendances,
    }


@attendances.post("/check-in")
@jwt_required()
def check_in():
    identity = get_jwt_identity()

    uid = identity.get("uid")
    user = User.query.filter_by(id=uid).first()
    if user.is_checkin:
        return (
            jsonify({"message": "You have already checked in."}),
            HTTP_400_BAD_REQUEST,
        )

    attendance = Attendance(user_id=uid, type=AttendanceType.CHECK_IN)
    user.is_checkin = True
    db.session.add(attendance)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Check in successfully",
                "attendance": {
                    "type": AttendanceType.CHECK_IN.name,
                    "id": attendance.id,
                },
            }
        ),
        HTTP_201_CREATED,
    )


@attendances.post("/check-out")
@jwt_required()
def check_out():
    identity = get_jwt_identity()

    uid = identity.get("uid")
    user = User.query.filter_by(id=uid).first()
    if not user.is_checkin:
        return (
            jsonify({"message": "You have not checked in yet"}),
            HTTP_400_BAD_REQUEST,
        )

    attendance = Attendance(user_id=uid, type=AttendanceType.CHECK_OUT)
    user.is_checkin = False
    db.session.add(attendance)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Check out successfully",
                "attendance": {
                    "type": AttendanceType.CHECK_OUT.name,
                    "id": attendance.id,
                },
            }
        ),
        HTTP_201_CREATED,
    )
