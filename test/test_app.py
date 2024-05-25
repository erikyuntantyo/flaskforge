import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)

from utils.boot import Boot


class TestApp:
    def setup_method(self):
        self.app = Boot.configure_app("development", "Testing-App")
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_index(self):
        response = self.client.get("/")
        assert response.status_code == 200, "Expected status code is 200"

    def test_response(self):
        response = self.client.get("/")
        assert response.get_json(True, True) != None, "Expected have response"
