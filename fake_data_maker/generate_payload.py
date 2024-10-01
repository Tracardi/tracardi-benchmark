from datetime import datetime
from random import randint, choice
from uuid import uuid4

from fake_data_maker.generate_context import make_fake_session_context
from fake_data_maker.generate_interest import get_random_interest
from fake_data_maker.generate_pii import make_fake_login, fake_persons, fake_identity
from fake_data_maker.generate_products import make_fake_product, checkout_data

sources = [str(uuid4()) for _ in range(0, 4)]
profiles = [str(uuid4()) for _ in range(0, 700)]
sessions_pool = [str(uuid4()) for _ in range(0, 200000)]

events = [
    # {"type": 'profile-update', "props": {
    #     "pii": {
    #         "firstname": "test-data"
    #     }
    # }},
    # {"type": 'profile-created', "props": {}},
    # {"type": 'session-opened', "props": {}},
    # {"type": 'session-closed', "props": {}},
    # {"type": 'profile-interest', "props": get_random_interest},
    {"type": 'page-view', "props": {}},
    {"type": 'search', "props": make_fake_product},
    # {"type": 'product-details-page-view', "props": make_fake_product},
    # {"type": 'checkout-started', "props": checkout_data},
    # {"type": 'product-added-to-basket', "props": make_fake_product},
    # {"type": 'sign-up', "props": lambda: fake_persons[randint(0, 499)]},
    # {"type": 'sign-in', "props": make_fake_login},
    # {"type": 'identification', "props": lambda: fake_identity[randint(0, 499)]},
]


def generate_payload(source):

    profile_id = profiles[randint(0, len(profiles) - 1)]
    # profile_id = "asjkajsk"
    session_id = sessions_pool[randint(0, len(sessions_pool) - 1)]
    # session_id = "@debug-session"

    def _get_event(event):
        return {
            "type": event['type'],
            "properties": event['props']() if callable(event['props']) else event['props'],
            # "options": {"async": False},
            "time": {
                "create": datetime.utcnow().isoformat() + "Z"
            }
        }

    def get_session():
        return sessions_pool[randint(0, len(sessions_pool) - 1)]

    # no_of_events = randint(40, 50)
    no_of_events = 1
    _events = [_get_event(events[randint(0, len(events) - 1)]) for _ in range(0, no_of_events)]

    payload = {
        "source": {
            "id": source,
            "name": "Fake data source"
        },
        # "context": make_fake_session_context(),
        "session": {
            "id": str(uuid4())
        },
        "profile": {
            "id": str(uuid4()),
            "ids": ['b']
        },
        # "options": {
        #     "profile": True
        # },
        "events": _events
    }

    return payload
