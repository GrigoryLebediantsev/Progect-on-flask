from pydantic import EmailStr
from typing import Optional


class User:
    def __init__(
        self, first_name: str, last_name: str, phone: str, email: EmailStr, score: int
    ):

        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.score = score
        self.id: Optional[int] = None

    def increase_score(self, amount: int):
        self.score += amount

    def add_id_from_memory(self, id: int) -> None:
        self.id = id

    def __lt__(self, other) -> bool:
        return self.score < other.score

