from uuid import uuid4

from model.observation import ObservationEntity


def generate_entity(type, props):
    return (f"{type}-1",  ObservationEntity(**{
        "instance": f"{type} #{str(uuid4())}",
        "traits": props()
    }))
