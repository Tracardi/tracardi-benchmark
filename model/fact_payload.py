from datetime import datetime
from typing import Optional, List, Tuple, Any
from uuid import uuid4

from pydantic import BaseModel

class Time(BaseModel):
    insert: Optional[datetime] = None
    create: Optional[datetime] = None
    update: Optional[datetime] = None

class Entity(BaseModel):
    id: str

class NamedEntity(BaseModel):
    id: str
    name: str

class DefaultNamedEntity(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    metadata: Optional[Time] = None


class SessionPayload(Entity):
    metadata: Optional[Time] = None
    context: Optional[dict] = {}

class OldEventPayload(BaseModel):
    type: str
    entity: DefaultNamedEntity
    properties: Optional[dict] = {}
    context: Optional[dict] = {}




class FactPayload(NamedEntity):
    events: List[OldEventPayload]
    context: Optional[dict] = {}

class MeasurePayload(NamedEntity):
    value: float

class EntityPayload(Entity):
    entity_name: str
    properties: Optional[dict] = {}
    measures: Optional[List[MeasurePayload]] = []

class EventPayload(Entity):
    type: str
    name: Optional[str] = None  # TODO Maybe not needed
    metadata: Optional[Time] = Time()
    source: Entity
    session: Optional[SessionPayload] = None
    entities: List[EntityPayload]
    options: Optional[dict] = {}
    context: Optional[dict] = {}
    measures: Optional[List[MeasurePayload]] = []
    tags: Optional[list] = []

