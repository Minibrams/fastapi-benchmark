import os
from locust import HttpUser, task

class ApiUser(HttpUser):

    @task
    def health_check(self):
        self.client.get(os.environ.get('LOCUST_ENDPOINT'))
