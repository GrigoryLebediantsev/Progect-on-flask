import phonenumbers

class User():
    def __init__(self, id, first_name, last_name, phone, email, score=0):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.score = score

    def validate_emile(self):
        ...

    def validate_phone(self):
        number = phonenumbers.parse(self.phone)
        return phonenumbers.is_valid_number(number)