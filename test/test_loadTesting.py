from locust import HttpUser, task, between, SequentialTaskSet
from time import sleep

class UserBehavior(SequentialTaskSet):
    def on_start(self):
        """Login before starting any tasks."""
        self.login()

    def login(self):
        """Simulate login to get a session."""
        response = self.client.post("/login", data={
            "email": "test@user.com",  # Use an actual email for the test
            "password": "123"     # Use the correct password
        })
        if response.status_code == 200:
            print("Login successful!")
        else:
            print(f"Login failed with status code {response.status_code}")
            self.interrupt()

    @task(1)
    def create_task(self):
        """Simulate posting a task."""
        response = self.client.post("/create_task", data={
            "task_title": "Sample Task",
            "task_description": "Description of the task",
            "budget": 100,
            "location": "Sample Location",
            "user_id": 1  # This should be a valid user ID
        })
        if response.status_code == 200:
            print("Task posted successfully!")
        else:
            print(f"Failed to post task with status code {response.status_code}")

    @task(2)
    def search_task(self):
        """Simulate searching for tasks."""
        response = self.client.post("/filter_jobs", data={
            "location": "Sample Location",
            "budget": 100
        })
        if response.status_code == 200:
            print("Search successful!")
        else:
            print(f"Failed to search tasks with status code {response.status_code}")


class PlatformLoadTest(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)  # Wait between 1 to 3 seconds between tasks
    host = "http://localhost:5000" 


