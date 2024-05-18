"""This module seeds the database with initial user like data for testing. """

import random

from app.extensions import db
from app.models.request import Request
from app.models.reply import Reply
from app.models.user import User
from app.models.user_like import UserLike

random.seed(5505)


def create_seed_user_like_data() -> list:
    """Create seed user like data."""

    users = [user.id for user in User.query.all()]
    requests = [request.id for request in Request.query.all()]
    replies = [reply.id for reply in Reply.query.all()]


    return [
        {
            "user_id": random.choice(users),
            "request_id": random.choice(requests),
            "reply_id": random.choice(replies),

        }
        for _ in range(100)
    ]


def seed_user_like():
    """Seed the database with initial user like data."""

    seed_user_like_data = create_seed_user_like_data()
    if not seed_user_like_data:
        return

    for data in seed_user_like_data:
        user_like = UserLike(
            user_id=data["user_id"],
            request_id=data["request_id"],
            reply_id=data["reply_id"],
        )
        db.session.add(user_like)

    db.session.commit()
