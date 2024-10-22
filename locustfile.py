import os

from locust import HttpUser, between, task
from fake_data_maker.generate_payload import generate_payload

source_id = os.environ.get("SOURCE_ID", 'locust-test')
type_of_stress = os.environ.get("TYPE_OF_STRESS", 'bulk-queue')

if source_id is None:
    raise ValueError("No SOURCE_ID is set.")


class WebsiteUser(HttpUser):
    wait_time = between(.8, 1.2)
    host = os.environ.get("HOST", "http://localhost:8686")

    @task
    def track(self):

        if type_of_stress == 'queue':

            payload = generate_payload(source=source_id)
            response = self.client.patch("/track", json=payload)

        elif type_of_stress == 'bulk':
            payload = [generate_payload(source=source_id) for _ in range(0, 20)]
            response = self.client.put("/track", json=payload)

        elif type_of_stress == 'bulk-queue':
            payload = [generate_payload(source=source_id, queue=True) for _ in range(0, 10)]
            response = self.client.put("/track", json=payload)

        elif type_of_stress == 'regular':
            payload = generate_payload(source=source_id)

            response = self.client.post("/track", json=payload)


        else:
            raise ValueError("Unknown TYPE_OF_STRESS is set. Available: 'regular', 'bulk', 'queue'.")

        if response.status_code == 500:
            print(response.content)

        # print(type_of_stress, len(payload['events']))
        # print(response.content)
