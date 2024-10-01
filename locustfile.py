from random import randint

from locust import HttpUser, between, task

from fake_data_maker.generate_payload import generate_payload, profiles


class WebsiteUser(HttpUser):
    wait_time = between(.5, 1)
    # host = "http://c01.unifonic.hz:38585"  # Your API
    # host = "http://65.109.120.125:48686/"  # Your API
    # host = "http://192.168.1.119:48686"  # Your API
    # host = "http://localhost:8686"  # Your API
    # host = "http://test.localpdctr.com:48686"
    # host = "http://65.109.11.219:8686"
    host="http://localhost:8686"
    # host= 'http://5.161.192.200:48585'

    @task
    def track(self):

        source_id = "5b564e75-3bd6-4da2-897a-d6de654881c1"

        payload = generate_payload(source=source_id)
        # payload = [generate_payload(source=source_id) for _ in range(0, 500)]

        response = self.client.patch("/track", json=payload)
        # response = self.client.put("/track", json=payload)

        print(response.content)
        # try:
        #     response = response.json()
        #     if response['profile']['id'] not in profiles:
        #         profiles.append(response['profile']['id'])
        # except KeyError:
        #     pass
        # except Exception as e:
        #     print(str(e))

        # print(response)
