import json
import pathlib
from threading import Thread

import pytest
from cheroot.ssl.builtin import BuiltinSSLAdapter
from cheroot.wsgi import Server


def mock_wsgi_server(environ, start_response):
    status = environ.get("HTTP_MOCK_STATUS", "200 OK")
    headers = [("Content-Type", "application/json")]
    start_response(status, headers)
    return [
        json.dumps({
            "url": environ.get("PATH_INFO", "/"),
            "method": environ.get("REQUEST_METHOD", "GET"),
            "headers": {
                key: value for key, value in environ.items() if key.startswith("HTTP_")
            },
            "body": environ.get("wsgi.input", b"").read().decode("iso-8859-1"),
        }).encode("utf-8")
    ]


@pytest.fixture(scope="session")
def server():
    server = Server(("127.0.0.1", 58962), mock_wsgi_server, reuse_port=True)
    port = server.bind_addr[1]
    thread = Thread(target=server.safe_start)
    thread.daemon = True
    thread.start()
    try:
        yield f"http://localhost:{port}"
    finally:
        server.stop()
        thread.join()


@pytest.fixture(scope="session")
def https_server():
    cert = pathlib.Path(__file__).parent / "server.crt"
    key = pathlib.Path(__file__).parent / "server.key"
    server = Server(("127.0.0.1", 58963), mock_wsgi_server, reuse_port=True)
    server.ssl_adapter = BuiltinSSLAdapter(certificate=str(cert), private_key=str(key))
    port = server.bind_addr[1]
    thread = Thread(target=server.safe_start)
    thread.daemon = True
    thread.start()
    try:
        yield f"https://localhost:{port}"
    finally:
        server.stop()
        thread.join()
