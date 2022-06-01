from random import randint

from faker import Faker
from faker.providers import internet, geo, phone_number, credit_card, user_agent

fake = Faker()
fake.add_provider(internet)
fake.add_provider(phone_number)
fake.add_provider(credit_card)

fake_emails = [fake.email() for _ in range(0, 1500)]


def make_fake_pii():
    name = fake.name().split()
    return {
        "name": name[0],
        "surname": name[1],
        "address": fake.address(),
        "phone": fake.phone_number(),
        "email": fake_emails[randint(0, 1499)]
    }


fake_persons = [make_fake_pii() for _ in range(0, 500)]


def make_fake_login():
    return {
        "email": fake_emails[randint(0, 1499)]
    }


def make_fake_loc():
    lng, lat, town, country, tz = fake.local_latlng()
    return {
        "login": fake_emails[randint(0, 1499)],
        "lng": lng,
        "lat": lat,
        "town": town,
        "country": country,
        "tz": tz
    }
