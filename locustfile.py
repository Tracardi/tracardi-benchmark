import os
import sys

sys.path.append('/home/risto/PycharmProjects/dev-bizmory/bizmory')
from locust import HttpUser, between, task
from fake_data_maker.generate_payload import generate_payload

source_id = os.environ.get("SOURCE_ID", '8351737-a9ad-4c29-a01b-2f3180bec592')
tenant = '8504a'

if source_id is None:
    raise ValueError("No SOURCE_ID is set.")


class WebsiteUser(HttpUser):
    wait_time = between(.005, .01)
    # wait_time = between(1.5, 2)
    host = os.environ.get("HOST", "http://localhost:8585")

    @task
    def track(self):
        payload = [generate_payload(source=source_id).model_dump(mode="json") for _ in range(1, 20)]
        response = self.client.put("/", json=payload, headers={
            'Content-Type': 'application/json',
            'x-tenant': tenant
        })

        if response.status_code != 200:
            print(response.content)
