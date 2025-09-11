from app.models import User
from app.adapter import InMemoryDatabase


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

        InMemoryDatabase.add_user(user=user)

        return user
