import sys
import os
# getting the name of the directory
current = os.path.dirname(os.path.realpath(__file__))
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
# adding the parent directory to 
# the sys.path.
sys.path.append(parent)

import unittest
from fastapi.testclient import TestClient
from main import app, model, session_manager

class TestEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello World, please head over to /docs"})

    def test_chatModel_endpoint(self):
        # Test case for /api/gpmodel/ endpoint
        input_data = {"user_input": "i have malria", "session_id": "123sess"}
        response = self.client.post("/api/gpmodel/", params=input_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("AI_out", response.json())

    def test_langModel_endpoint(self):
        # Test case for /api/langchainmodel/ endpoint
        input_data = {"user_input": "i have headache"}
        response = self.client.post("/api/langchainmodel/", params=input_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("AI_out", response.json())

    def test_llamaModel_endpoint(self):
        # Test case for /api/llama2model/ endpoint
        input_data = {"user_input": "i have headace"}
        response = self.client.post("/api/llama2model/", params=input_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("AI_out", response.json())

if __name__ == '__main__':
    unittest.main()
