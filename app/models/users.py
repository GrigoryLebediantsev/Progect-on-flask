from pydantic import EmailStr


class User:
    def __init__(
        self, first_name: str, last_name: str, phone: str, email: EmailStr, score: int
    ):

        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.score = score

    def increase_score(self, amount: int):
        self.score += amount

    # def __repr__(self) -> str:
    #     return f"{self.id}) {self.first_name} {self.last_name}"
    #
    # def __lt__(self, other):
    #     return self.score < other.score
    #
    # def to_dict(self) -> dict:
    #     return dict(
    #         {
    #             "first_name": self.first_name,
    #             "last_name": self.last_name,
    #             "score": self.score,
    #         }
    #     )
