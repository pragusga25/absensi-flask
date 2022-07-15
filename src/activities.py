from flask import Blueprint

activities = Blueprint("activities", __name__, url_prefix="/api/v1/activities")


@activities.get("/")
def get_activities():
    return {"activities": []}


@activities.post("/")
def create_activities():
    return "Activity created"
