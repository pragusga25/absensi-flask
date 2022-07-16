from sqlalchemy.dialects.postgresql import UUID
from src.shared.database import db
from datetime import datetime
import enum


class AttendanceType(enum.Enum):
    CHECK_IN = "CHECK_IN"
    CHECK_OUT = "CHECK_OUT"


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    type = db.Column(
        db.Enum(AttendanceType),
        nullable=False,
        default=AttendanceType.CHECK_IN,
    )
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("user.id"), nullable=False
    )

    def __repr__(self):
        return f"Attendance('{self.id}', '{self.user_id}', '{self.attendance_type}')"
