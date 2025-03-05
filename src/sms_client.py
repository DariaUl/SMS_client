import base64
import socket
import json

class Request:
    def __init__(self, method: str, url: str, headers: dict, body: str):
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body

    def to_bytes(self) -> bytes:
        request_lines = [
            f"{self.method} {self.url} HTTP/1.1",
            *[f"{key}: {value}" for key, value in self.headers.items()],
            "",
            self.body
        ]
        return "\r\n".join(request_lines).encode("utf-8")

    @classmethod
    def from_bytes(cls, data: bytes) -> 'Request':
        lines = data.decode("utf-8").split("\r\n")
        method, url, _ = lines[0].split()
        headers = {}
        body = ""
        header_section = True

        for line in lines[1:]:
            if not line:
                header_section = False
                continue
            if header_section:
                key, value = line.split(": ", 1)
                headers[key] = value
            else:
                body += line

        return cls(method=method, url=url, headers=headers, body=body)


class Response:
    def __init__(self, status_code: int, headers: dict, body: str):
        self.status_code = status_code
        self.headers = headers
        self.body = body

    def to_bytes(self) -> bytes:
        response_lines = [
            f"HTTP/1.1 {self.status_code} OK",
            *[f"{key}: {value}" for key, value in self.headers.items()],
            "",
            self.body
        ]
        return "\r\n".join(response_lines).encode("utf-8")

    @classmethod
    def from_bytes(cls, data: bytes) -> 'Response':
        lines = data.decode("utf-8").split("\r\n")
        status_line = lines[0]
        status_code = int(status_line.split()[1])

        headers = {}
        body = ""
        header_section = True

        for line in lines[1:]:
            if not line:
                header_section = False
                continue
            if header_section:
                key, value = line.split(": ", 1)
                headers[key] = value
            else:
                body += line

        return cls(status_code=status_code, headers=headers, body=body)


class SMSClient:
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def send_sms(self, sender: str, recipient: str, message: str) -> Response:
        auth = f"{self.username}:{self.password}"
        auth_header = f"Basic {base64.b64encode(auth.encode()).decode()}"

        body = json.dumps({
            "sender": sender,
            "recipient": recipient,
            "message": message
        })

        request = Request(
            method="POST",
            url="/send_sms",
            headers={
                "Host": f"{self.host}:{self.port}",
                "Authorization": auth_header,
                "Content-Type": "application/json",
                "Content-Length": str(len(body))
            },
            body=body
        )

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(request.to_bytes())

            response_data = b""
            while True:
                data = s.recv(4096)
                if not data:
                    break
                response_data += data

        return Response.from_bytes(response_data)