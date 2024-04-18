"""User model."""

import datetime
import enum
import hashlib

from flask_login import UserMixin
from sqlalchemy import event

from app.constant import GRAVATAR_URL
from app.extensions import bcrypt, db
from app.utils import generate_time, generate_uuid


class UserStatusEnum(enum.Enum):
    """Enum for user status."""

    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


# pylint: disable=too-many-instance-attributes
class User(UserMixin, db.Model):
    """User model."""

    id: str = db.Column(db.String(36), primary_key=True, default="")
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    email: str = db.Column(db.String(120), nullable=False)
    password_hash: str = db.Column(db.String(300), nullable=True)
    avatar_url: str = db.Column(db.String(300), default="")
    use_google: bool = db.Column(db.Boolean, default=False)
    use_github: bool = db.Column(db.Boolean, default=False)
    security_question: str = db.Column(db.String(300), nullable=True)
    security_answer: str = db.Column(db.String(300), nullable=True)
    status: str = db.Column(db.String(20), default=UserStatusEnum.ACTIVE.value)
    create_at: datetime = db.Column(db.DateTime, default=generate_time())
    update_at: datetime = db.Column(
        db.DateTime, default=generate_time(), onupdate=generate_time()
    )

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        username: str,
        email: str,
        avatar_url: str = "",
        use_google: bool = False,
        use_github: bool = False,
        security_question: str = "",
        security_answer: str = "",
    ) -> None:
        self.username = username
        self.email = email
        self.avatar_url = avatar_url
        self.use_google = use_google
        self.use_github = use_github
        self.security_question = security_question
        self.security_answer = security_answer

    @property
    def password(self) -> str:
        """Get the password hash."""
        return self.password_hash

    @password.setter
    def password(self, password: str) -> None:
        """Set password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def __repr__(self) -> str:
        """Return the user object."""
        return f"<User {self.username}>"

    def to_dict(self) -> dict:
        """Return a JSON format of the user."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "avatarUrl": self.avatar_url,
            "useGoogle": self.use_google,
            "useGithub": self.use_github,
            "securityQuestion": self.security_question,
            "securityAnswer": self.security_answer,
            "status": self.status,
            "createAt": self.create_at,
            "updateAt": self.update_at,
        }

    def verify_password(self, password: str) -> bool:
        """Check the password."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_id(self) -> str:
        """Get the user id."""
        return self.id

    @staticmethod
    def user_exists(email: str) -> bool:
        """Check if the user is the user."""
        return User.query.get(email=email) is not None


@event.listens_for(User, "before_insert")
def before_insert_listener(_, __, target) -> None:
    """Update the create time before inserting a new user."""
    target.id = generate_uuid()
    target.avatar_url = check_avatar_url(target.avatar_url, target.email)


def check_avatar_url(avatar_url: str, email: str) -> None:
    """Check the avatar url."""
    if not avatar_url and email:
        return f"{GRAVATAR_URL}{hashlib.sha256(email.lower().encode()).hexdigest()}"
    return avatar_url
