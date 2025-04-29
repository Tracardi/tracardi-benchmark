import os
import random
from random import randint
from typing import Dict, Tuple, List
from uuid import uuid4

from fake_data_maker.generate_actor import generate_entity
from fake_data_maker.generate_interest import get_random_interest
from fake_data_maker.generate_pii import make_identification_data
from fake_data_maker.generate_products import make_fake_product, checkout_data
from fake_data_maker.generate_profile_data import generate_profile_data
from model.observation import Observation, ObservationEvent, Entity, ObservationSession

sources = [str(uuid4()) for _ in range(0, int(os.environ.get("NO_OF_SOURCES", 4)))]
profiles = [str(uuid4()) for _ in range(0, int(os.environ.get("NO_OF_PROFILES", 10000)))]
sessions_pool = [str(uuid4()) for _ in range(0, int(os.environ.get("NO_OF_SESSIONS", 3000)))]
entity_types = ["customer", 'session', 'product', 'delivery']
tags = ['prefix:my-tags', 'system:event', 'behavioural:event']

entities: Dict[str, List[Tuple[str, dict]]] = {
    "customer": [generate_entity('customer', generate_profile_data) for _ in range(0, 100)],
    "product": [generate_entity('product', make_fake_product) for _ in range(0, 100)],
    "check-out": [generate_entity('product', checkout_data) for _ in range(0, 100)],
    "identity": [generate_entity('identity', make_identification_data) for _ in range(0, 100)],
    "interest": [generate_entity('interest', get_random_interest) for _ in range(0, 100)]
}


def get_random_entity(type) -> Dict[str, dict]:
    return random.choice(entities[type])


events = {
    ("customer", "product-added-to-basket"): [get_random_entity('product')],
    ("customer", "signed-up"): [],
    ("customer", "signed-in"): [],
    ("customer", "updated"): [],
    ("customer", "identified"): [get_random_entity('identity')],
    ("customer", "checkout-started"): [get_random_entity('check-out')],
    ("product", "searched"): [get_random_entity('customer')],
    ("product", "page-viewed"): [get_random_entity('customer')],
    ("customer", "interest-increased"): [get_random_entity('interest')],
}


def generate_payload(source):
    session_id = sessions_pool[randint(0, len(sessions_pool) - 1)]

    key = random.choice(list(events.keys()))

    actor_type, event_type = key
    actor_id, actor_props = get_random_entity(actor_type)
    context = events[key]

    context_ids = []
    entities = {actor_id:actor_props}
    for id, c in context:
        entities[id] = c
        context_ids.append(id)

    return Observation(
        id=str(uuid4()),
        type="Observations",
        source=Entity(id=source),
        session=ObservationSession(id=session_id),
        entities=entities,
        events=[ObservationEvent(
            event=event_type,
            actor=actor_id, # ID only
            context=context_ids, # IDS only
            tag=random.choice(tags)
        )]
    )
