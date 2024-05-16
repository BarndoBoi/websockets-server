import asyncio
import websockets
import json

username = input("Pick a username: ")

async def listen(websocket):
    async for message in websocket:
        event = json.loads(message)

        if event['type'] == 'join':
            if event['user'] == username:
                print("You have connected")
            else:
                print(event['user'] + " has connected")
        
        if event['type'] == 'chat':
            print(event['user'] + ": " + event['message'])

async def chat(websocket):
    while True:
        chat_message = input("Enter message: ")
        await websocket.send(json.dumps( { 'type': 'chat', 'user': username, 'message': chat_message } ))

async def main():
    uri = 'ws://localhost:42069'

    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps( {'type': 'join', 'user': username} ))
        await asyncio.gather(
            listen(websocket),
            chat(websocket),
        )

if __name__ == "__main__":
    asyncio.run(main())
