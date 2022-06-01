from pprint import pprint
from random import randint
from urllib import parse

import faker_commerce
from faker import Faker

fake = Faker()
fake.add_provider(faker_commerce.Provider)

platforms = [
    fake.android_platform_token,
    fake.ios_platform_token,
    fake.mac_platform_token,
    fake.windows_platform_token
]

color_depths = [16, 24, 32]


def make_fake_session_context():
    uri = fake.uri()
    uri_parsed = parse.urlparse(uri)
    return {
        "context": {
            "time": {
                "local": "8/26/2021, 9:36:13 PM",
                "tz": fake.timezone()
            },
            "page": {
                "url": uri,
                "path": uri_parsed.path,
                "hash": "",
                "title": fake.ecommerce_name(),
                "referer": {
                    "host": f"{uri_parsed.scheme}://{uri_parsed.netloc}",
                    "query": None
                },
                "history": {
                    "length": randint(0, 20)
                }
            },
            "browser": {
                "browser": {
                    "name": "Netscape",
                    "engine": "Gecko",
                    "appVersion": "5.0 (X11)",
                    "userAgent": fake.user_agent(),
                    "language": fake.locale(),
                    "onLine": True,
                    "javaEnabled": False,
                    "cookieEnabled": True
                },
                "device": {
                    "platform": platforms[randint(0, 3)]()
                }
            },
            "storage": {
                "local": {
                    "__anon_id": "\"f30ee0a4-be4e-4571-97b2-80b32a18a77f\"",
                    "profileQuery": "",
                    "eventQuery": "",
                    "sessionQuery": "",
                },
                "cookie": {
                    "cookies1": "tracardi-session-id=fb151f11-e6f4-4cbf-9ad9-39414c1219f8; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%22f573ac77-2d68-41f1-b768-d2d4aa986382%22",
                    "cookies2": "tracardi-session-id=fb151f11-e6f4-4cbf-9ad9-39414c1219f8, ajs_user_id=null, ajs_group_id=null, ajs_anonymous_id=\"f573ac77-2d68-41f1-b768-d2d4aa986382\""
                }
            },
            "screen": {
                "width": randint(1000, 3000),
                "height": randint(640, 1080),
                "innerWidth": randint(1000, 3000),
                "innerHeight": randint(640, 1080),
                "availWidth": randint(1000, 3000),
                "availHeight": randint(640, 1080),
                "colorDepth": color_depths[randint(0, 2)],
                "pixelDepth": color_depths[randint(0, 2)],
            }
        }
    }


def make_fake_event_context():
    return {
        "context": {
            "ip": fake.ipv4()
        }
    }

pprint(make_fake_event_context())
