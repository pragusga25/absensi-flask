from sqlalchemy.dialects.postgresql import UUID
from src.shared.database import db
import uuid
from datetime import datetime


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    type = db.Column(db.String(16), nullable=False)
    user_id = db.Column(
        db.ForeignKey("user.id"),
        nullable=False,
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.now(),
        nullable=False,
    )


class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    is_checkin = db.Column(db.Boolean, nullable=False, default=False)
    activities = db.relationship("Activity", backref="user")
    attendances = db.relationship("Attendance", backref="user")
    token_blocklist = db.relationship("TokenBlocklist", backref="user")

    def __repr__(self):
        return f"User('{self.id}', '{self.email}')"
