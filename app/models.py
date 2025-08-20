import phonenumbers
import re


class User:
    def __init__(self, id, first_name, last_name, phone, email, score=0):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.score = score

    @staticmethod
    def validate_emile(email):
        valid = re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)
        return True if valid else False

    @staticmethod
    def validate_phone(phone):
        valid = re.match(r"^\+7\d{10}$", phone)
        return True if valid else False


class Expression:
    def __init__(self, id, operation, *values):
        self.id = id
        self.operation = operation
        self.values = values
        self.answer = self.__evaluate()

    def __evaluate(self):
        return eval(self.to_str())

    def to_str(self):
        str_values = list(map(str, self.values))
        expr_str = f' {self.operation} '.join(str_values)
        # todo generate expression for len(values)>2
        return expr_str


