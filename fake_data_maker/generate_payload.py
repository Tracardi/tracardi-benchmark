import os
import random
from datetime import datetime
from random import randint
from uuid import uuid4

from fake_data_maker.generate_context import make_fake_session_context
from fake_data_maker.generate_interest import get_random_interest
from fake_data_maker.generate_pii import make_fake_login, fake_persons, fake_identity
from fake_data_maker.generate_products import make_fake_product, checkout_data
from fake_data_maker.generate_profile_data import generate_profile_data

sources = [str(uuid4()) for _ in range(0, int(os.environ.get("NO_OF_SOURCES", 4)))]
profiles = [str(uuid4()) for _ in range(0, int(os.environ.get("NO_OF_PROFILES", 10000)))]
sessions_pool = [str(uuid4()) for _ in range(0, int(os.environ.get("NO_OF_SESSIONS", 3000)))]
entities = ["customer", 'session', 'product', 'delivery']
tags = ['prefix:my-tags', 'system:event', 'behavioural:event']

events = [
    {"type": 'updated',                     "ents": [{"entity": "customer", "props": generate_profile_data}]},
    {"type": 'profile-interest',            "ents": [{"entity": "customer", "props": get_random_interest}]},
    {"type": 'page-viewed',                 "ents": [{"entity": "customer", "props": {}}]},
    {"type": 'searched',                    "ents": [{"entity": "customer", "props": make_fake_product}]},
    {"type": 'product-details-page-viewed', "ents": [{"entity": "customer", "props": make_fake_product}]},
    {"type": 'checkout-started',            "ents": [{"entity": "customer", "props": checkout_data}]},
    {"type": 'product-added-to-basket',     "ents": [{"entity": "customer", "props": make_fake_product}]},
    {"type": 'signed-up',                   "ents": [{"entity": "customer", "props": lambda: fake_persons[randint(0, 499)]}]},
    {"type": 'signed-in',                   "ents": [{"entity": "customer", "props": make_fake_login}]},
    {"type": 'identified',                  "ents": [{"entity": "customer", "props": lambda: fake_identity[randint(0, 499)]}]}
]


def generate_payload(source, events_per_profile=1, queue=False):

    session_id = sessions_pool[randint(0, len(sessions_pool) - 1)]

    # def _get_event(event):
    #     return {
    #         "type": event['type'],
    #         "properties": event['props']() if callable(event['props']) else event['props'],
    #         "options": {"async": True},
    #         "time": {
    #             "create": datetime.utcnow().isoformat() + "Z"
    #         }
    #     }

    # payload = {
    #     "source": {
    #         "id": source,
    #         "name": "Fake data source"
    #     },
    #     "context": make_fake_session_context(),
    #     "session": {
    #         "id": session_id
    #     },
    #     "profile": {
    #         "id": profile_id
    #     },
    #     "options": {
    #         "queue": queue
    #     },
    #     "events": [_get_event(events[randint(0, len(events) - 1)]) for _ in range(0, events_per_profile)]
    # }

    event = random.choice(events)

    payload = {
        "id": str(uuid4()),
        "type": event['type'],
        "source": {
            "id": source
        },
        "session": {
            "id": session_id,
            "context": make_fake_session_context()
        },
        "entities": [],
        "options": {},
        "context": {},
        "measures": [],
        "tags": [random.choice(tags)]
    }

    for e in event['ents']:
        payload["entities"].append(
            {
                "id": str(uuid4()),
                "entity_name": e['entity'],
                "properties": e['props']() if callable(e['props']) else e['props'],
                "measures": []
            }
        )
    return payload
