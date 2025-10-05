from app.models import User
from app.adapter import InMemoryDatabase
from app.adapter.database.in_database import Database

from app.deps import get_storage

Storage = get_storage()


class UserCreateService:

    @staticmethod
    def create_user(
        first_name: str, last_name: str, phone: str, email: str, score: int
    ) -> User:

        user = User(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            score=score,
        )

        Storage.add_user(user=user)
        Storage.create_user_history(user.id)

        return user
