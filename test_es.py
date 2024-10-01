import asyncio
from time import time

from uuid import uuid4
from tracardi.context import ServerContext, Context
from tracardi.domain.event_metadata import EventMetadata

from tracardi.domain.entity import Entity
from tracardi.domain.event import Event
from tracardi.domain.time import EventTime
from tracardi.service.storage.factory import storage_manager


def create_events():
    return [Event(
        id=str(uuid4()),
        type="test",
        source=Entity(id="49c1f3d1-8199-443d-9642-22887f3d512b"),
        metadata=EventMetadata(time=EventTime()),
        properties={"test": 1}
    ).model_dump(exclude={"operation": ...}) for _ in range(0, 10000)]


async def async_thread1():
    with ServerContext(Context(production=True)):
        s = time()
        for _ in range(0, 1):
            events = create_events()
            tasks = [asyncio.create_task(storage_manager('event').upsert(event)) for event in events]
            print(len(await asyncio.gather(*tasks)), time() - s)
        print(time() - s)

async def async_thread2():
    with ServerContext(Context(production=True)):
        s = time()
        for _ in range(0, 1):
            events = create_events()
            tasks = [asyncio.create_task(storage_manager('event').upsert(event)) for event in events]
        print(time() - s)
        await asyncio.sleep(10)


asyncio.run(async_thread2())
