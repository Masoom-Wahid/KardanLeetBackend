from locust import HttpUser, task, SequentialTaskSet
import logging
from locust import events




@events.quitting.add_listener
def _(environment, **kw):
    if environment.stats.total.fail_ratio > 0.01:
        logging.error("Test failed due to failure ratio > 1%")
        environment.process_exit_code = 1


class RegisteredUser(SequentialTaskSet):
    @task
    def testSubmission(self):
        lang = "java"

        question_id = "1"
        with open("access.txt","r") as file:
            ACCESSTOKEN = file.read()
        
        files = {'code': open(f'solutions/factorial.{lang if lang != "python" else "py"}', 'rb')}
        data = {
            "lang": lang,
            "type": "submit",
            "id": question_id,
        }
        headers = {'Authorization': f"Bearer {ACCESSTOKEN}"}
        self.client.post("/competition/", files=files, data=data, headers=headers)


class ApiUser(HttpUser):
    tasks = [RegisteredUser]





