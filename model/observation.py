from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List, Any, Dict, Union, Set
from uuid import uuid4
from zoneinfo import ZoneInfo

from pydantic import BaseModel, RootModel

from model.instance import Instance
from model.instance_link import InstanceLink


def now_in_utc(delay=None) -> datetime:
    now = datetime.utcnow().replace(tzinfo=ZoneInfo('UTC'))

    if delay is None:
        return now

    if delay < 0:
        return now - timedelta(seconds=-1 * delay)

    return now + timedelta(seconds=delay)

class ObservationCollectConsent(BaseModel):
    allow: bool


class Entity(BaseModel):
    id: str


class NamedEntity(Entity):
    name: str


class EntityMeta(Entity):
    type: str
    # schema: str


class ObservationMeasurement(NamedEntity):
    value: float


class ObservationEntity(BaseModel):
    instance: Instance

    part_of: Optional[List[Instance]] = None
    is_a: Optional[Instance] = None
    has_a: Optional[List[Instance]] = None

    traits: Optional[dict] = {}

    consents: Optional[ObservationCollectConsent] = None


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

class EntityRefs(RootModel[Dict[str, ObservationEntity]]):

    def get(self, link) -> Optional[ObservationEntity]:
        return self.root.get(link)

    def index(self) -> Dict[str, ObservationEntity]:
        return self.root



class ObservationConsents(ObservationCollectConsent):
    granted: Set[str]

class ObservationRelation(BaseModel):
    id: Optional[str] = None
    ts: Optional[datetime] = None
    actor: Optional[Union[List[InstanceLink], InstanceLink]] = None
    event: str
    entities: Optional[Union[List[InstanceLink], InstanceLink]] = None
    traits: Optional[dict] = None
    context: Optional[List[InstanceLink]] = []
    tags: Optional[list] = []
    timer: Optional[ObservationTimer] = None

    consents: Optional[ObservationCollectConsent] = None

class ObservationMetaEntity(BaseModel):
    ip_location: Optional[bool] = False
    browser: Optional[bool] = False
    device: Optional[bool] = False

class ObservationMetadata(BaseModel):
    data: Optional[dict] = {}
    entity: ObservationMetaEntity = ObservationMetaEntity()

class Observation(BaseModel):
    id: Optional[str] = None
    type: Optional[str] = None
    aspect: Optional[str] = None
    source: Entity
    entities: Optional[EntityRefs] = {}
    relation: List[ObservationRelation]  # Should be relation
    context: Optional[dict] = {}
    metadata: Optional[ObservationMetadata] = ObservationMetadata()
    consents: Optional[ObservationConsents] = None

    def __init__(self, /, **data: Any):
        data['id'] = f"anon-{str(uuid4())}"
        super().__init__(**data)
