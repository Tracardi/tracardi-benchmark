from random import randint

from faker import Faker

import faker_commerce

fake = Faker()
fake.add_provider(faker_commerce.Provider)


def ecommerce_price(as_int: bool = True):
    n = randint(10, 100000)
    return round(n, 2) if as_int else n / 100


def make_fake_company():
    return {
        "company": fake.company(),
        "address": fake.address()
    }


def make_fake_product():
    return {
        "product": fake.ecommerce_name(),
        "category": fake.ecommerce_category(),
        "price": ecommerce_price(False),
        "number": fake.bothify(text='????-########', letters='ABCDE')
    }


fake_products = [make_fake_product() for _ in range(0, 1000)]


def make_fake_product_purchase():
    product = fake_products[randint(0, 999)]
    product["card"] = fake.credit_card_number()
    return product
