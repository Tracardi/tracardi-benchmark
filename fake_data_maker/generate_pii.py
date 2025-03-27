from random import randint

from faker import Faker
from faker.providers import internet, geo, phone_number, credit_card, user_agent

fake = Faker()
fake.add_provider(internet)
fake.add_provider(phone_number)
fake.add_provider(credit_card)

number_of_fake_emails = 15000

fake_emails = [fake.email() for _ in range(0, number_of_fake_emails)]


def make_fake_pii():
    name = fake.name().split()
    return {
        "firstname": name[0],
        "lastname": name[1],
        "phone":{"main": fake.phone_number()},
        "email":{"main": fake_emails[randint(0, number_of_fake_emails-1)]}
    }


def make_identification_data():
    name = fake.name().split()
    tn = fake.phone_number()
    return {
        "firstname": name[0],
        "lastname": name[1],
        "slack": f"@{name[1]}",
        "telegram": f"@{name[0]}",
        "phone": tn,
        "whatsapp": tn,
        "email": {"main": fake_emails[randint(0, number_of_fake_emails-1)]}
    }


fake_persons = [make_fake_pii() for _ in range(0, 500)]
fake_identity = [make_identification_data() for _ in range(0, 500)]

def make_fake_login():
    return {
        "email":{"main": fake_emails[randint(0, number_of_fake_emails-1)]}
    }


def make_fake_loc():
    lng, lat, town, country, tz = fake.local_latlng()
    return {
        "login": fake_emails[randint(0, number_of_fake_emails-1)],
        "lng": lng,
        "lat": lat,
        "town": town,
        "country": country,
        "tz": tz
    }
