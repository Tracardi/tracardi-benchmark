from random import randint

from locust import HttpUser, between, task

from fake_data_maker.generate_payload import generate_payload, profiles


class WebsiteUser(HttpUser):
    wait_time = between(.5, 1)
    host = "http://async.mt-hetzner.lb"    # Your API

    @task
    def track(self):
        profile_id = profiles[randint(0, len(profiles) - 1)]
        response = self.client.post("/track", json=generate_payload(source="@fake-data", profile_id=profile_id))
        response = response.json()

        try:
            if response['profile']['id'] not in profiles:
                profiles.append(response['profile']['id'])
        except KeyError:
            pass
        except TypeError:
            pass

        # print(response)
