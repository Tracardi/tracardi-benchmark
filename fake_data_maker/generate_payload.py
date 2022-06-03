from random import randint, choice
from uuid import uuid4

from fake_data_maker.generate_context import make_fake_session_context
from fake_data_maker.generate_pii import make_fake_login, fake_persons
from fake_data_maker.generate_products import make_fake_product, make_fake_product_purchase
from fake_data_maker.generate_session import get_session_for_email

sources = [str(uuid4()) for _ in range(0, 8)]
profiles = [str(uuid4()) for _ in range(0, 10)]

events = [
    {"type": 'page-view', "props": {}},
    {"type": 'product-search', "props": make_fake_product},
    {"type": 'product-view', "props": make_fake_product},
    {"type": 'product-purchase', "props": make_fake_product_purchase},
    {"type": 'product-in-basket', "props": make_fake_product},
    {"type": 'sign-up', "props": fake_persons[randint(0, 499)]},
    {"type": 'log-in', "props": make_fake_login},
    {"type": 'product-details', "props": make_fake_product}
]


def generate_payload(source, profile_id):
    def _rand(container, threshold=3):
        if randint(0, 10) >= threshold:
            return choice(container)
        else:
            value = str(uuid4())
            container.append(value)
            return value

    def _get_event(event):
        return {
            "type": event['type'],
            "properties": event['props']() if callable(event['props']) else event['props']
        }

    def get_session(events):
        for event in events:
            if event['type'] in ['sign-up', 'log-in']:
                session = get_session_for_email(event['properties']['email'])
                return session[randint(0, len(session) - 1)]
        return str(uuid4())

    no_of_events = randint(1, 5)
    _events = [_get_event(events[randint(0, len(events) - 1)]) for _ in range(0, no_of_events)]

    payload = {
        "source": {
            "id": source,
            "name": "Fake-data"
        },
        "context": make_fake_session_context(),
        "session": {
            "id": get_session(_events)
        },
        "profile": {
            "id": profile_id
        },
        "options": {
            "profile": True
        },
        "events": _events
    }

    return payload
