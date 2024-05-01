"""Request model."""

import datetime

from app.extensions import db
from app.utils import generate_time


# pylint: disable=too-many-instance-attributes
class Request(db.Model):
    """Request model."""

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id: str = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    title: str = db.Column(db.String(40), nullable=False)
    content: str = db.Column(db.String(1000), default="")
    community_id: int = db.Column(db.Integer, db.ForeignKey("community.id"))
    category_id: int = db.Column(db.Integer, db.ForeignKey("category.id"))
    view_num: int = db.Column(db.Integer)
    like_num: int = db.Column(db.Integer)
    reply_num: int = db.Column(db.Integer)
    save_num: int = db.Column(db.Integer)
    create_at: datetime = db.Column(db.DateTime, default=generate_time())
    update_at: datetime = db.Column(
        db.DateTime, default=generate_time(), onupdate=generate_time()
    )

    author = db.relationship("User", backref=db.backref("requests", lazy=True))
    community = db.relationship("Community", backref=db.backref("requests", lazy=True))
    category = db.relationship("Category", backref=db.backref("requests", lazy=True))

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        author_id: str,
        title: str,
        content: str,
        community_id: int,
        category_id: int,
        view_num: int,
        like_num: int,
        reply_num: int,
        save_num: int,
    ) -> None:
        self.author_id = author_id
        self.title = title
        self.content = content
        self.community_id = community_id
        self.category_id = category_id
        self.view_num = view_num
        self.like_num = like_num
        self.reply_num = reply_num
        self.save_num = save_num

    def __repr__(self) -> str:
        """Return a string representation of the request."""

        return f"<Request {self.id}>"

    # genrated by copilot
    def to_dict(self):
        """Return a JSON format of the request."""

        return {
            "id": self.id,
            "author_id": self.author_id,
            "title": self.title,
            "content": self.content,
            "community_id": self.community_id,
            "category_id": self.category_id,
            "view_num": self.view_num,
            "like_num": self.like_num,
            "reply_num": self.reply_num,
            "save_num": self.save_num,
            "create_at": self.create_at,
            "update_at": self.update_at,
        }
