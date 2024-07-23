import json
import threading
import unittest
import time
from http.server import HTTPServer
from unittest.mock import patch, MagicMock

import requests

from server import SimpleHTTPRequestHandler


class TestHTTPRequestHandler(unittest.TestCase):
    def setUp(self):
        self.server_address = ("127.0.0.1", 12345)
        self.server = HTTPServer(self.server_address, SimpleHTTPRequestHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()
        time.sleep(1)

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.server_thread.join()

    @patch('server.SimpleHTTPRequestHandler')
    def test_create_account(self, mockHandler):
        mock_handler = mockHandler.return_value
        mock_handler.path = '/loan'
        mock_handler.headers = {'Content-Length': '0'}
        mock_handler.rfile.read = MagicMock(return_value=json.dumps({'account': 'test'}).encode())
        mock_handler.do_POST()
        res = mock_handler.wfile.getvalue()
        print(f"res {res}")
        pass

    def test_real(self):
        api_url = f'http://{self.server_address[0]}:{self.server_address[1]}/loan'
        headers = {
            'Content-Type': 'application/json',
            'RequestRef': '33ac9718-f6e5-4807-9cad-ccbe80ea2849'
        }
        data = {
            "totalLoan": 5890123,
            "mrr": 8.25,
            "mrrInAccount": -4,
            "day": 25,
            "currentDate": "2024-03-24"
        }

        response = requests.post(api_url, headers=headers, json=data)
        print(f'API Response: {response.json()}')

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['message'], 'ok')
        self.assertIn('total', response_data)


if __name__ == '__main__':
    unittest.main()
