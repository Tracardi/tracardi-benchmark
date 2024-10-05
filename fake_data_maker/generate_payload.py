import os
from datetime import datetime
from random import randint
from uuid import uuid4

from fake_data_maker.generate_context import make_fake_session_context
from fake_data_maker.generate_interest import get_random_interest
from fake_data_maker.generate_pii import make_fake_login, fake_persons, fake_identity
from fake_data_maker.generate_products import make_fake_product, checkout_data
from fake_data_maker.generate_profile_data import generate_profile_data

sources = [str(uuid4()) for _ in range(0, int(os.environ.get("NO_OF_SOURCES", 4)))]
profiles = [str(uuid4()) for _ in range(0, int(os.environ.get("NO_OF_PROFILES", 1000)))]
sessions_pool = [str(uuid4()) for _ in range(0, int(os.environ.get("NO_OF_SESSIONS", 2000)))]

events = [
    {"type": 'profile-update', "props": generate_profile_data},
    {"type": 'profile-interest', "props": get_random_interest},
    {"type": 'page-view', "props": {}},
    {"type": 'search', "props": make_fake_product},
    {"type": 'product-details-page-view', "props": make_fake_product},
    {"type": 'checkout-started', "props": checkout_data},
    {"type": 'product-added-to-basket', "props": make_fake_product},
    {"type": 'sign-up', "props": lambda: fake_persons[randint(0, 499)]},
    {"type": 'sign-in', "props": make_fake_login},
    {"type": 'identification', "props": lambda: fake_identity[randint(0, 499)]},
]


def generate_payload(source, events_per_profile=1):

    profile_id = profiles[randint(0, len(profiles) - 1)]
    session_id = sessions_pool[randint(0, len(sessions_pool) - 1)]

    def _get_event(event):
        return {
            "type": event['type'],
            "properties": event['props']() if callable(event['props']) else event['props'],
            "options": {"async": True},
            "time": {
                "create": datetime.utcnow().isoformat() + "Z"
            }
        }

    payload = {
        "source": {
            "id": source,
            "name": "Fake data source"
        },
        "context": make_fake_session_context(),
        "session": {
            "id": session_id
        },
        "profile": {
            "id": profile_id,
            "ids": ['b']
        },
        "events": [_get_event(events[randint(0, len(events) - 1)]) for _ in range(0, events_per_profile)]
    }

    return payload
