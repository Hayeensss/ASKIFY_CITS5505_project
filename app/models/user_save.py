"""User Save model."""

import datetime

from app.extensions import db
from app.utils import generate_time


class UserSave(db.Model):
    """User Save model."""

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id: str = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    request_id: int = db.Column(db.Integer, db.ForeignKey("request.id"), nullable=False)
    create_at: datetime = db.Column(db.DateTime, default=generate_time())

    user = db.relationship("User", backref=db.backref("user_saves", lazy=True))
    request = db.relationship("Request", backref=db.backref("user_saves", lazy=True))

    def __init__(self, user_id: str, request_id: int) -> None:
        self.user_id = user_id
        self.request_id = request_id

    def __repr__(self) -> str:
        """Return a string representation of the user record."""

        return f"<UserSave {self.request_id}>"

    # genrated by copilot
    def to_dict(self) -> dict:
        """Return a JSON format of the user record."""

        return {
            "id": self.id,
            "user_id": self.user_id,
            "request_id": self.request_id,
            "create_at": self.create_at,
        }
