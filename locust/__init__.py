from locust import HttpLocust, TaskSet, task


class WebsiteTasks(TaskSet):
    def on_start(self):
        self.client.post("/login", {
            "username": "test_user",
            "password": ""
        })

    @task
    def index(self):
        self.client.get("https://www.google.com/")

    @task
    def about(self):
        self.client.get("https://www.guru99.com/controllers-in-jmeter.html")


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 5000
    max_wait = 15000