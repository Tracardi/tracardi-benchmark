from datetime import datetime
from typing import Optional, List, Any, Dict
from uuid import uuid4

from pydantic import BaseModel


class Entity(BaseModel):
    id: str


class NamedEntity(Entity):
    name: str


class EntityMeta(Entity):
    type: str
    # schema: str


class ObservationSession(Entity):
    ts: Optional[datetime] = None
    context: Optional[dict] = {}


class ObservationMeasurement(NamedEntity):
    value: float


class ObservationEntity(BaseModel):
    entity: EntityMeta
    properties: Optional[dict] = {}
    measures: Optional[List[ObservationMeasurement]] = []


class ObservationEvent(Entity):
    ts: Optional[datetime] = None
    actor: str
    event: str
    context: Optional[List[str]] = []
    tags: Optional[list] = []

    def __init__(self, /, **data: Any):
        # create if none
        if data.get('id', None) is None:
            data['id'] = str(uuid4())
        if data.get('ts', None):
            data['ts'] = datetime.now()
        super().__init__(**data)


class EventTimer(Entity):
    trigger: Optional[int] = 1
    events: Optional[List[ObservationEvent]] = []


class Observation(Entity):
    type: Optional[str] = None
    source: Entity
    session: Optional[ObservationSession] = None
    entities: Dict[str, dict]
    events: List[ObservationEvent]
    options: Optional[dict] = {}
    context: Optional[dict] = {}
    timer: Optional[EventTimer] = None

    def __init__(self, /, **data: Any):
        data['id'] = f"anon-{str(uuid4())}"
        super().__init__(**data)
