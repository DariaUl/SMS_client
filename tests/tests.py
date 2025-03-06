import unittest
from src.sms_client import Request, Response


class TestRequest(unittest.TestCase):
    def test_to_bytes(self):
        request = Request(
            method="POST",
            url="http://localhost:4010/send_sms",
            headers={"Content-Type": "application/json"},
            body={"from": "12345", "to": "67890", "text": "Hello"}
        )
        expected = (
            b"POST /send_sms HTTP/1.1\r\n"
            b"Host: localhost:4010\r\n"
            b"Content-Type: application/json\r\n"
            b"\r\n"
            b'{"from": "12345", "to": "67890", "text": "Hello"}'
        )
        self.assertEqual(request.to_bytes(), expected)


class TestResponse(unittest.TestCase):
    def test_from_bytes(self):
        binary_data = (
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: application/json\r\n"
            b"\r\n"
            b'{"status": "success", "message_id": "12345"}'
        )
        response = Response.from_bytes(binary_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, '{"status": "success", "message_id": "12345"}')

    def test_error_response(self):
        binary_data = (
            b"HTTP/1.1 400 Bad Request\r\n"
            b"Content-Type: application/json\r\n"
            b"\r\n"
            b'{"error": "Invalid parameters"}'
        )
        response = Response.from_bytes(binary_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.body, '{"error": "Invalid parameters"}')


if __name__ == "__main__":
    unittest.main()