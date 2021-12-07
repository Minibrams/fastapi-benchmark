from locust import HttpUser, task, constant

class ApiUser(HttpUser):
    wait_time = constant(1)

    @task
    def health_check(self):
        self.client.get('/sync/')
