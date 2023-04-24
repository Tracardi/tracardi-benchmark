from random import randint

from locust import HttpUser, between, task

from fake_data_maker.generate_payload import generate_payload, profiles


class WebsiteUser(HttpUser):
    wait_time = between(.5, 1)
    host = "http://localhost:8686"  # Your API

    @task
    def track(self):
        profile_id = profiles[randint(0, len(profiles) - 1)]
        profile_id = "123"

        payload = generate_payload(source="07d766bc-bbe8-4aae-b2f5-642b28563c32",
                                   profile_id=profile_id)
        print(payload)

        response = self.client.post("/track", json=payload)
        print(response.content)
        try:
            response = response.json()
            if response['profile']['id'] not in profiles:
                profiles.append(response['profile']['id'])
        except KeyError:
            pass
        except Exception as e:
            print(str(e))

        # print(response)
