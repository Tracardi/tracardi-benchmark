from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List, Any, Dict
from uuid import uuid4
from zoneinfo import ZoneInfo

from pydantic import BaseModel


def now_in_utc(delay=None) -> datetime:
    now = datetime.utcnow().replace(tzinfo=ZoneInfo('UTC'))

    if delay is None:
        return now

    if delay < 0:
        return now - timedelta(seconds=-1 * delay)

    return now + timedelta(seconds=delay)


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


class StatusEnum(str, Enum):
    on = "on"
    off = "off"
    pending = "pending"


class ObservationTimer(Entity):
    status: StatusEnum
    timeout: Optional[int] = None
    event: Optional[str] = None

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        if self.status != StatusEnum.off:
            if self.timeout is None:
                raise ValueError(
                    "Error. Timer without time-out. Time-out must be set for timers that are on or pending.")
            if self.event is None:
                raise ValueError(
                    "Error. Timer without event type. Event must be set for timers that are on or pending.")


class ObservationEvent(Entity):
    ts: Optional[datetime] = None
    actor: str
    event: str
    object: str
    properties: Optional[dict] = None
    context: Optional[List[str]] = []
    tags: Optional[list] = []
    timer: Optional[ObservationTimer] = None

    actor_type: Optional[str] = None

    def __init__(self, /, **data: Any):
        # create if none
        if data.get('id', None) is None:
            data['id'] = str(uuid4())
        if data.get('ts', None):
            data['ts'] = now_in_utc()
        super().__init__(**data)
        _actor = self.actor.split(':')
        if len(self.actor.split(':')) != 2:
            raise ValueError(
                f"Actor property in ObservationEvent must have <ACTOR_TYPE>:<ACTOR_ID>. Current value `{self.actor}` has incorrect format.")
        self.actor_type, _ = _actor


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
