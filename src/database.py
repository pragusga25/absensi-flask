from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime
import enum

db = SQLAlchemy()


class AttendanceType(enum.Enum):
    CHECK_IN = "CHECK_IN"
    CHECK_OUT = "CHECK_OUT"


class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, onupdate=datetime.now()
    )
    activities = db.relationship("Activity", backref="user")
    attendances = db.relationship("Attendance", backref="user")

    def __repr__(self):
        return f"User('{self.id}', '{self.email}')"


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, onupdate=datetime.now()
    )
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("user.id"), nullable=False
    )

    def __repr__(self):
        return f"Activity('{self.id}', '{self.name}')"


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    attendance_type = db.Column(
        db.Enum(AttendanceType),
        nullable=False,
        default=AttendanceType.CHECK_IN,
    )
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("user.id"), nullable=False
    )

    def __repr__(self):
        return f"Attendance('{self.id}', '{self.user_id}', '{self.attendance_type}')"
