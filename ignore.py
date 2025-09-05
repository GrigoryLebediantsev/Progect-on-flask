from faker import Faker

faker = Faker("ru_RU")


def create_random_payload():
    return {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "phone": faker.phone_number(),
        "email": faker.email()
    }

print(create_random_payload())