import os

from locust import HttpUser, between, task
from fake_data_maker.generate_payload import generate_payload
from model.fact_payload import EventPayload

source_id = os.environ.get("SOURCE_ID", '4dd4482d-95c3-435a-a254-0a7866301030')
type_of_stress = os.environ.get("TYPE_OF_STRESS", 'regular')
tenant = '8504a'

if source_id is None:
    raise ValueError("No SOURCE_ID is set.")


class WebsiteUser(HttpUser):
    wait_time = between(.8, 1.2)
    # host = os.environ.get("HOST", "http://8504a.localhost.com:8686")
    # host = os.environ.get("HOST", "http://tracardi.mobiletronics.net:28686")
    host = os.environ.get("HOST", "http://localhost:8585")

    @task
    def track(self):

        payload = generate_payload(source=source_id, events_per_profile=4)
        EventPayload(**payload)
        response = self.client.put("/", json=payload, headers={
            'Content-Type': 'application/json',
            'x-tenant': tenant
        })


        if response.status_code != 200:
            print(response.content)
        # print(response.content)
