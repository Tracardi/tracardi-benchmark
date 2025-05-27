import os

from locust import HttpUser, between, task
from fake_data_maker.generate_payload import generate_payload

source_id = os.environ.get("SOURCE_ID", '5f6caead-3fc5-4ba1-9c0c-70d460d00e2a')
tenant = '8504a'

if source_id is None:
    raise ValueError("No SOURCE_ID is set.")


class WebsiteUser(HttpUser):
    # wait_time = between(.005, .01)
    wait_time = between(1.5, 2)
    host = os.environ.get("HOST", "http://localhost:8585")

    @task
    def track(self):

        payload = generate_payload(source=source_id)
        response = self.client.put("/", json=[payload.model_dump(mode="json")], headers={
            'Content-Type': 'application/json',
            'x-tenant': tenant
        })


        if response.status_code != 200:
            print(response.content)
