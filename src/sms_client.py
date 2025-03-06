import socket
import json
from typing import Dict, Any


class Request:
    def __init__(self, method: str, url: str, headers: Dict[str, str], body: Dict[str, Any]):
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body

    def to_bytes(self) -> bytes:
        host, port, path = parse_url(self.url)
        
        body_json = json.dumps(self.body)
        
        host_header = f"Host: {host}:{port}" if port else f"Host: {host}"
        
        request_lines = [
            f"{self.method} {path} HTTP/1.1",
            host_header,
            *[f"{key}: {value}" for key, value in self.headers.items()],
            "",
            body_json
        ]
        
        return "\r\n".join(request_lines).encode("utf-8")

    def send(self, timeout=5) -> 'Response':
        host, port, path = parse_url(self.url)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                sock.connect((host, port))
                sock.sendall(self.to_bytes())
                response_data = sock.recv(4096)
            return Response.from_bytes(response_data)
        except (socket.timeout, ConnectionRefusedError) as error:
            raise ConnectionError(f"Network error: {error}")


class Response:
    def __init__(self, status_code: int, body: str):
        self.status_code = status_code
        self.body = body

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> 'Response':
        data = binary_data.decode("utf-8")
        lines = data.split("\r\n")
        status_line = lines[0]
        status_code = int(status_line.split()[1])
        body = "\n".join(lines[3:])
        return cls(status_code, body)


def parse_url(url: str):
    if "://" not in url:
        url = f"http://{url}"
    parts = url.split("/")
    host_port = parts[2]
    path = "/" + "/".join(parts[3:])
    if ":" in host_port:
        host, port = host_port.split(":")
        port = int(port.strip("/"))
    else:
        host = host_port
        port = 4010
    return host, port, path