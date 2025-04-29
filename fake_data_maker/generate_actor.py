from uuid import uuid4

def generate_entity(type, props):
    return (f"{type}:{str(uuid4())}",  props())
