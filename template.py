import random
from uuid import uuid4

profiles = [
    "2b5fffcc-8311-4b95-879d-4debab0f5a80"
]

sessions = ["41904a2a-b6ef-421d-8e83-f2883d75a847"]

events = [
    {
        "properties": {
            "product": "Sun glasses - Badoo",
            "price": 13.45
        },
        "type": "purchase-order",
        "options": {
            "saveSession": True,
            "saveEvents": True
        }
    },
    {
        "properties": {
            "Vacation": 1
        },
        "type": "profile-interest",
        "options": {
            "saveSession": True,
            "saveEvents": True
        }
    },
    {
        "properties": {
            "custom-data": 123
        },
        "type": "page-view",
        "options": {
            "saveSession": True,
            "saveEvents": True
        }
    },
    {
        "properties": {
            "id": 0.5455296669319577,
            "name": "Joe",
            "surname": "Doe",
            "email": "john.doe@gmail.com",
            "location": "Berlin/Germany"
        },
        "type": "personal-data",
        "options": {
            "saveSession": True,
            "saveEvents": True
        }
    }
]


def _rand(container, threshold=3):
    if random.randint(0, 10) >= threshold:
        return random.choice(container)
    else:
        value = str(uuid4())
        container.append(value)
        return value


def get_random_payload(source):
    session = _rand(container=sessions)
    profile = _rand(container=profiles)
    payload = {
        "source": {
            "id": source
        },
        "context": {
            "time": {
                "local": "8/26/2021, 9:36:13 PM",
                "tz": "Europe/Warsaw"
            },
            "page": {
                "url": "http://localhost:8686/tracker/?source=" + source,
                "path": "/tracker/",
                "hash": "",
                "title": "Test page",
                "referer": {
                    "host": None,
                    "query": None
                },
                "history": {
                    "length": 11
                }
            },
            "browser": {
                "browser": {
                    "name": "Netscape",
                    "engine": "Gecko",
                    "appVersion": "5.0 (X11)",
                    "userAgent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
                    "language": "en-US",
                    "onLine": True,
                    "javaEnabled": False,
                    "cookieEnabled": True
                },
                "device": {
                    "platform": "Linux x86_64"
                }
            },
            "storage": {
                "local": {
                    "__anon_id": "\"f30ee0a4-be4e-4571-97b2-80b32a18a77f\"",
                    "profileQuery": "",
                    "eventQuery": "",
                    "sessionQuery": "",
                    "tracardi-profile-id": "\"2b5fffcc-8311-4b95-879d-4debab0f5a80\"",
                },
                "cookie": {
                    "cookies1": "tracardi-session-id=fb151f11-e6f4-4cbf-9ad9-39414c1219f8; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%22f573ac77-2d68-41f1-b768-d2d4aa986382%22",
                    "cookies2": "tracardi-session-id=fb151f11-e6f4-4cbf-9ad9-39414c1219f8, ajs_user_id=null, ajs_group_id=null, ajs_anonymous_id=\"f573ac77-2d68-41f1-b768-d2d4aa986382\""
                }
            },
            "screen": {
                "width": 1728,
                "height": 972,
                "innerWidth": 1728,
                "innerHeight": 442,
                "availWidth": 1728,
                "availHeight": 948,
                "colorDepth": 24,
                "pixelDepth": 24
            }
        },
        "session": {
            "id": str(uuid4()) if session is None else session
        },
        "options": {
            "profile": True
        },
        "events": random.choices(events, k=random.randint(1, 3))
    }

    if profile is not None:
        payload['profile'] = {
            "id": profile
        }

    return payload
