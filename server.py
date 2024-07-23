import asyncio
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import websockets

from loan_calculation import loan_calculation


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, directory=None, **kwargs):
        self.accounts = []
        super().__init__(*args, **kwargs)

    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        if self.path == "/":
            response = {"message": "Hello, World!"}
        elif self.path.startswith("/accounts"):
            response = {"accounts": self.accounts}
        else:
            self._set_headers(404)
            response = {"error": "Not Found"}
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)
        payload = json.loads(data)
        path = self.path
        if path == "/account/create":
            self.accounts.append(payload)
            self._set_headers()
            response = {"message": "Account created", "account": payload}
        elif path == "/loan":
            required_fields = {"totalLoan", "mrr", "mrrInAccount", "day"}
            if not all(field in payload for field in required_fields):
                self._set_headers(400)
                response = {"message": "fail", "error": "Missing required fields"}
            else:
                self._set_headers()
                total = loan_calculation(payload)
                response = {"message": "ok", "total": total}
        else:
            self._set_headers(404)
            response = {"error": "Not Found"}
        self.wfile.write(json.dumps(response).encode())


async def websocket_handler(websocket, path):
    print(f"path: {path}")
    if path != "/ws":
        await websocket.send(json.dumps({"error": "Invalid path"}))
        return

    async def send_periodic_messages():
        while True:
            msg = json.dumps({"message": "test"})
            await websocket.send(msg)
            await asyncio.sleep(1)

    send_task = asyncio.create_task(send_periodic_messages())

    try:
        async for message in websocket:
            data = json.loads(message)
            response = {"message": "Received", "data": data}
            await websocket.send(json.dumps(response))
    finally:
        send_task.cancel()


async def run_websocket_server(port=8765):
    async with websockets.serve(websocket_handler, "localhost", port):
        print(f'Starting websocket server on port {port}...')
        await asyncio.Future()


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()


async def main():
    loop = asyncio.get_event_loop()
    http_server = loop.run_in_executor(None, run)
    websocket_server = run_websocket_server()
    await asyncio.gather(http_server, websocket_server)


if __name__ == '__main__':
    asyncio.run(main())
