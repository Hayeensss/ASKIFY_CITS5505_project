"""This module seeds the database with initial user data for testing. """

import random

from faker import Faker

from app.extensions import db
from app.models.user import User

random.seed(5505)
faker = Faker()


def create_seed_user_data() -> list:
    """Create seed user data."""

    return [
        {
            "username": faker.name(),
            "email": faker.email(),
            "avatar_url": f"https://api.dicebear.com/5.x/adventurer/svg?seed={random.randint(1, 1000)}",
            "password": "Password@123",
            "security_question": "What is your favorite color?",
            "security_answer": "blue",
        }
        for _ in range(10)
    ]


seed_user_data = create_seed_user_data()


def seed_user():
    """Seed the database with initial user data."""

    if not seed_user_data:
        return

    for data in seed_user_data:
        user = User(
            username=data["username"],
            email=data["email"],
            avatar_url=data["avatar_url"],
            use_google=False,
            use_github=False,
            security_question=data["security_question"],
            security_answer=data["security_answer"],
        )
        user.password = data["password"]
        db.session.add(user)

    db.session.commit()
