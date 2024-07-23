# import json
# import unittest
# from http.server import BaseHTTPRequestHandler
# from unittest.mock import MagicMock, patch
# from io import BytesIO
#
# from server import SimpleHTTPRequestHandler
#
#
# class TestHTTPRequestHandler(unittest.TestCase):
#     def setUp(self):
#         # Prepare the request and response objects for the handler
#         self.request = BytesIO()
#         self.response = BytesIO()
#         self.handler = SimpleHTTPRequestHandler(self.request, self.response, None)
#
#     @patch('server.SimpleHTTPRequestHandler')
#     def test_create_account(self, MockHandler):
#         # Set up the mock handler
#         mock_handler = MockHandler.return_value
#         mock_handler.path = '/loan'
#         mock_handler.headers = {'Content-Length': '0'}
#         mock_handler.rfile = BytesIO(json.dumps({
#             "totalLoan": 10000,
#             "mrr": 5,
#             "mrrInAccount": 1,
#             "day": 15,
#             "currentDate": "2024-07-23"
#         }).encode())
#         mock_handler.wfile = BytesIO()
#
#         # Call the method directly
#         mock_handler.do_POST()
#
#         # Get the written response
#         mock_handler.wfile.seek(0)
#         response_data = json.loads(mock_handler.wfile.read().decode())
#
#         # Assertions
#         self.assertEqual(response_data['message'], 'ok')
#         self.assertIn('total', response_data)
#
#     @patch('server.SimpleHTTPRequestHandler')
#     def test_create_account_fail(self, MockHandler):
#         # Set up the mock handler
#         mock_handler = MockHandler.return_value
#         mock_handler.path = '/loan'
#         mock_handler.headers = {'Content-Length': '0'}
#         mock_handler.rfile = BytesIO(json.dumps({
#             "totalLoan": 10000,
#             "mrr": 5,
#             "mrrInAccount": 1
#             # Missing 'day' and 'currentDate'
#         }).encode())
#         mock_handler.wfile = BytesIO()
#
#         # Call the method directly
#         mock_handler.do_POST()
#
#         # Get the written response
#         mock_handler.wfile.seek(0)
#         response_data = json.loads(mock_handler.wfile.read().decode())
#
#         # Assertions
#         self.assertEqual(response_data['message'], 'fail')
#         self.assertEqual(response_data['error'], 'Missing required fields')
#
# if __name__ == '__main__':
#     unittest.main()
