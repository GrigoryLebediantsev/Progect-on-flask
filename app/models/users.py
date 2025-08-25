import re


class User:
    def __init__(
        self, id: int, first_name: str, last_name: str, phone: str, email: str, score=0
    ):

        self._validate_required_fields(first_name, last_name, phone, email)
        self._validate_types(id, first_name, last_name, phone, email, score)
        self._validate_email(email)
        self._validate_phone(phone)

        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.score = score
        self.history = []

    @staticmethod
    def _validate_required_fields(first_name, last_name, phone, email):
        if not all([first_name, last_name, phone, email]):
            raise ValueError("Недостаёт обязательных полей")

    @staticmethod
    def _validate_types(
        id: int, first_name: str, last_name: str, phone: str, email: str, score: int
    ) -> None:
        if not (
            isinstance(id, int)
            and isinstance(first_name, str)
            and isinstance(last_name, str)
            and isinstance(phone, str)
            and isinstance(email, str)
            and isinstance(score, int)
        ):
            raise ValueError("Неверные типы данных")

    @staticmethod
    def _validate_email(email: str) -> None:
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            raise ValueError("Некорректный email")

    @staticmethod
    def _validate_phone(phone) -> None:
        if not re.match(r"^\+7\d{10}$", phone):
            raise ValueError("Некорректный телефон")

    def increase_score(self, amount: int):
        self.score += amount

    def __repr__(self) -> str:
        return f"{self.id}) {self.first_name} {self.last_name}"

    def __lt__(self, other):
        return self.score < other.score

    def to_dict(self):
        return dict(
            {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "score": self.score,
            }
        )

    def add_to_history(self, task: dict, user_answer):
        task['user_answer'] = user_answer
        if not task["user_answer"] == task["answer"]:
            task["reward"] = 0
        self.history.append(task)
