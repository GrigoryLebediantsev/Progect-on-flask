import re


class User:
    def __init__(self, id, first_name, last_name, phone, email, score=0):

        if not (
            isinstance(id, int)
            and isinstance(first_name, str)
            and isinstance(last_name, str)
            and isinstance(phone, str)
            and isinstance(email, str)
            and isinstance(score, int)
        ):
            raise ValueError

        if not self.validate_email(email) or not self.validate_phone(phone):
            raise ValueError

        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.score = score

    @staticmethod
    def validate_email(email):
        valid = re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)
        return True if valid else False

    @staticmethod
    def validate_phone(phone):
        valid = re.match(r"^\+7\d{10}$", phone)
        return True if valid else False

    def increase_score(self, amount):
        self.score += amount

    def __repr__(self):
        return f"{self.id}) {self.first_name} {self.last_name}"
