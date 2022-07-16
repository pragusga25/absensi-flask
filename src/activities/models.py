from sqlalchemy.dialects.postgresql import UUID
from src.shared.database import db
from datetime import datetime


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("user.id"), nullable=False
    )

    def __repr__(self):
        return f"Activity('{self.id}', '{self.name}')"
