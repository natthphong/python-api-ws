import json
import requests
import asyncio
import websockets
import logging


async def call_api():
    api_url = 'http://localhost:8000/loan'
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


async def on_message(message):
    msg = json.loads(message)
    print(f'Received from WebSocket: {msg}')


async def websocket_handler():
    await  call_api()
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        async def send_periodic_messages():
            while True:
                message = json.dumps({"message": "hello world"})
                await websocket.send(message)
                print(f'Sent to WebSocket: {message}')
                await asyncio.sleep(60)

        send_task = asyncio.create_task(send_periodic_messages())

        try:
            async for message in websocket:
                await on_message(message)
        finally:
            send_task.cancel()


if __name__ == "__main__":
    asyncio.run(websocket_handler())
