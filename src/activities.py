from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from src.database import Activity, User, db

activities = Blueprint("activities", __name__, url_prefix="/api/v1/activities")


@activities.get("/")
@jwt_required()
def get_activities():
    try:
        args = request.args
        from_date = args.get("from")
        to_date = args.get("to")

        identity = get_jwt_identity()
        uid = identity.get("uid")

        activities_db = None

        if from_date is not None and to_date is not None:
            activities_db = (
                Activity.query.filter_by(user_id=uid)
                .filter(Activity.created_at.between(from_date, to_date))
                .all()
            )
        else:
            activities_db = Activity.query.filter_by(user_id=uid).all()

        activities = []
        for activity in activities_db:
            data = {
                "id": activity.id,
                "name": activity.name,
                "time": activity.created_at,
            }
            activities.append(data)

        return jsonify({"activities": activities}), HTTP_200_OK
    except:
        return (
            jsonify({"message": "Something went wrong"}),
            HTTP_500_INTERNAL_SERVER_ERROR,
        )


@activities.post("/")
@jwt_required()
def create_activities():
    try:
        identity = get_jwt_identity()
        uid = identity.get("uid")

        user = User.query.filter_by(id=uid).first()
        if not user.is_checkin:
            return (
                jsonify({"message": "You have to check in first."}),
                HTTP_403_FORBIDDEN,
            )

        name = request.json.get("name")
        if name is None:
            return (
                jsonify({"message": "Please provide a name."}),
                HTTP_400_BAD_REQUEST,
            )

        activity = Activity(user_id=uid, name=name)
        db.session.add(activity)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Activity created successfully",
                    "activity": {
                        "id": activity.id,
                        "name": activity.name,
                        "time": activity.created_at,
                    },
                }
            ),
            HTTP_201_CREATED,
        )

    except:
        return (
            jsonify({"message": "Something went wrong"}),
            HTTP_500_INTERNAL_SERVER_ERROR,
        )


@activities.patch("/<int:id>")
@jwt_required()
def update_activities(id):
    try:
        identity = get_jwt_identity()
        uid = identity.get("uid")

        user = User.query.filter_by(id=uid).first()
        if not user.is_checkin:
            return (
                jsonify({"message": "You have to check in first."}),
                HTTP_403_FORBIDDEN,
            )

        activity = Activity.query.filter_by(id=id, user_id=uid).first()
        if activity is None:
            return (
                jsonify({"message": "Activity not found."}),
                HTTP_400_BAD_REQUEST,
            )

        name = request.json.get("name")
        if name is None:
            return (
                jsonify({"message": "Please provide a name."}),
                HTTP_400_BAD_REQUEST,
            )

        activity.name = name
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Activity updated successfully",
                    "activity": {
                        "id": activity.id,
                        "name": activity.name,
                        "time": activity.created_at,
                    },
                }
            ),
            HTTP_200_OK,
        )
    except:
        return (
            jsonify({"message": "Something went wrong"}),
            HTTP_500_INTERNAL_SERVER_ERROR,
        )


@activities.delete("/<int:id>")
@jwt_required()
def delete_activities(id):
    try:
        identity = get_jwt_identity()
        uid = identity.get("uid")

        user = User.query.filter_by(id=uid).first()
        if not user.is_checkin:
            return (
                jsonify({"message": "You have to check in first."}),
                HTTP_403_FORBIDDEN,
            )

        activity = Activity.query.filter_by(id=id, user_id=uid).first()
        if activity is None:
            return (
                jsonify({"message": "Activity not found."}),
                HTTP_400_BAD_REQUEST,
            )

        db.session.delete(activity)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Activity deleted successfully",
                }
            ),
            HTTP_200_OK,
        )
    except:
        return (
            jsonify({"message": "Something went wrong"}),
            HTTP_500_INTERNAL_SERVER_ERROR,
        )
