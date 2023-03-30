import json
import unittest
import requests


class TestCalendarAPI(unittest.TestCase):
    token = None

    def setUp(self):
        self.url = "http://localhost:5000"
        self.headers = {"Content-Type": "application/json"}
        self.login_data = {
            "nickname": "test_nickname",
            "password": "test_password",
            "email": "test_email@test.com"
        }
        self.event_data = {
            "header": "test_event",
            "description": "test description",
            "date": "2023-03-18",
            "time": "15:00"
        }

    def test1_register_new_user(self):
        response = requests.post(f"{self.url}/signup", json=self.login_data, headers=self.headers)

        # check if user added to db
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["isAddedToDB"], True)

        # check if user with the same credentials cannot be added to db
        response = requests.post(f"{self.url}/signup", json=self.login_data, headers=self.headers)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["isAddedToDB"], False)
        self.assertEqual(response.json()["reason"], "user exist")

    def test2_login_right_credentials(self):
        global token
        response = requests.post(f"{self.url}/login", json=self.login_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("token" in response.json())
        token = response.json()["token"]

    def test3_login_wrong_credentials(self):
        data = {
            "nickname": "test_nickname",
            "password": "wrong_password"
        }
        response = requests.post(f"{self.url}/login", json=data, headers=self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"isLogged": False})

    def test4_create_event(self):
        global token

        self.headers['Authorization'] = f'Bearer {token}'
        response = requests.post(f"{self.url}/create_event", json=self.event_data, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["msg"], "success")

    def test4_get_events_by_date_added_in_previous_test(self):
        global token
        self.headers['Authorization'] = f'Bearer {token}'

        response = requests.get(url=f'{self.url}/get_events_by/{self.event_data["date"]}', headers=self.headers)

        response_data = json.loads(response.json()[0])

        self.assertEqual(response_data["header"], self.event_data["header"])
        self.assertEqual(response_data["time"], self.event_data["time"])

    def test6_delete_event_added_in_previous_test(self):
        global token
        self.headers['Authorization'] = f'Bearer {token}'

        response = requests.get(url=f'{self.url}/delete_event_by/{self.event_data["header"]}', headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["isDeleted"])

    def test7_delete_user_by_email(self):
        response = requests.get(f"{self.url}/delete_user_by/{self.login_data['email']}", headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["is_deleted"], True)


if __name__ == "__main__":
    unittest.main()

    #
    # def test_add_event_to_calendar(self):
    #     data = {
    #         "title": "Test event",
    #         "date": "2023-04-01",
    #         "time": "14:00",
    #         "description": "This is a test event"
    #     }
    #
    #     response = requests.post(self.url + "/create_event", json=data, headers=self.headers)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json()["title"], "Test event")
    #     self.assertEqual(response.json()["date"], "2023-04-01")
    #     self.assertEqual(response.json()["time"], "14:00")
    #
    #
    # def test_get_event_from_calendar(self):
    #     date = "2023-04-01"
    #     response = requests.get(self.url + f"/get_events_by/{date}")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json()["title"], "Test event")
    #     self.assertEqual(response.json()["start_date"], "2023-04-01")
    #     self.assertEqual(response.json()["time"], "14:00")

    # def test_edit_event_in_calendar(self):
    #     event_id = 1
    #     data = {
    #         "title": "Test event",
    #         "date": "2023-04-01",
    #         "time": "14:00",
    #         "description": "This is a test event"
    #     }
    #     response = requests.put(self.url + f"/{event_id}", json=data, headers=self.headers)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json()["title"], "Edited test event")
    #     self.assertEqual(response.json()["start_date"], "2023-04-01")
    #     self.assertEqual(response.json()["end_date"], "2023-04-05")
    #
    # def test_delete_event_from_calendar(self):
    #     event_id = 1
    #     response = requests.delete(self.url + f"/{event_id}")
    #     self.assertEqual(response.status_code, 204)
    #
