import base64
import json
from typing import Any, Dict
from fastapi import FastAPI

from .security import AIENERGY_HTTP_USERNAME, AIENERGY_HTTP_PASSWORD

async def call_app(app: FastAPI, path: str, request_body: Dict[str, Any], method: str = "POST"):
    """
    Simulate an ASGI request into the FastAPI app.
    Runs lifespan and middlewares.
    """

    def make_basic_auth(username: str, password: str) -> str:
        token = base64.b64encode(f"{username}:{password}".encode()).decode()
        return f"Basic {token}"
    body_bytes = json.dumps(request_body).encode("utf-8")

    # ASGI scope for the request
    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": method,
        "path": path,
        "raw_path": path.encode("ascii"),
        "headers": [
            (b"host", b"testserver"),
            (b"content-type", b"application/json"),
            (b"content-length", str(len(body_bytes)).encode("ascii")),
            (b"authorization", make_basic_auth(AIENERGY_HTTP_USERNAME, AIENERGY_HTTP_PASSWORD).encode())
        ],
        "query_string": b"",
        "server": ("127.0.0.1", 8000),
        "client": ("127.0.0.1", 1234),
        "scheme": "http",
        "app": app,
    }

    # Queues for request/response
    response = {}

    async def receive():
        return {"type": "http.request", "body": body_bytes, "more_body": False}

    async def send(message):
        nonlocal response
        if message["type"] == "http.response.start":
            response["status"] = message["status"]
            response["headers"] = dict((k.decode(), v.decode()) for k, v in message["headers"])
        elif message["type"] == "http.response.body":
            response["body"] = message.get("body", b"").decode()

    # Run app as ASGI
    await app.router.startup()
    async with app.router.lifespan_context(app):
        await app(scope, receive, send)
    # await app(scope, receive, send)
    await app.router.shutdown()

    return response