import os
import random
from random import randint
from typing import Dict, Tuple, List
from uuid import uuid4

from fake_data_maker.generate_interest import get_random_interest
from fake_data_maker.generate_pii import make_identification_data
from fake_data_maker.generate_products import make_fake_product, checkout_data
from fake_data_maker.generate_profile_data import generate_profile_data
from tracardi.domain.entity import Entity
from tracardi.domain.payload.instance_link import InstanceLink

from tracardi.domain.payload.observation import Observation, ObservationRelation, ObservationEntity


def generate_entity(type, props):
    return (f"{type}-1", ObservationEntity(**{
        "instance": f"{type} #{str(uuid4())}",
        "traits": props()
    }))



sources = [str(uuid4()) for _ in range(0, int(os.environ.get("NO_OF_SOURCES", 4)))]
profiles = [str(uuid4()) for _ in range(0, int(os.environ.get("NO_OF_PROFILES", 10000)))]
sessions_pool = [str(uuid4()) for _ in range(0, int(os.environ.get("NO_OF_SESSIONS", 3000)))]
entity_types = ["customer", 'session', 'product', 'delivery']
tags = ['prefix:my-tags', 'system:event', 'behavioural:event']

entities: Dict[str, List[Tuple[str, dict]]] = {
    "customer": [generate_entity('customer', generate_profile_data) for _ in range(0, 10000)],
    "product": [generate_entity('product', make_fake_product) for _ in range(0, 5000)],
    "check-out": [generate_entity('product', checkout_data) for _ in range(0, 1000)],
    "identity": [generate_entity('identity', make_identification_data) for _ in range(0, 1000)],
    "interest": [generate_entity('interest', get_random_interest) for _ in range(0, 1000)]
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

    entity_type, event_type = key
    actor_link, actor_props = get_random_entity(entity_type)
    object_link, object_props = get_random_entity(entity_type)
    context = events[key]

    context_ids = []
    _entities = {actor_link: actor_props, object_link: object_props}
    for id, c in context:
        _entities[id] = c
        context_ids.append(id)

    return Observation(
        id=session_id,
        type="Test Observation",
        source=Entity(id=source),
        entities=_entities,
        relation=[ObservationRelation(
            type="event",
            label=event_type,
            actor=InstanceLink(actor_link),  # ID only
            objects=[InstanceLink(object_link)],
            context=context_ids,  # IDS only
            tags=[random.choice(tags)],
            traits={"data": f"$entities['{actor_link}']"}
        )]
    )
