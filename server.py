import asyncio
import json

import websockets
from websockets.server import serve

from game import Game

connected = {}
game = Game()

async def chat(websocket, message):
    # Send the chat message to everybody except the person who sent it
    #others = connected
    #del others[message['user']]
    websockets.broadcast(list(connected.values()), json.dumps(message))

async def error(websocket, message):
    await websocket.send(message)

async def join(websocket, message):
    if message['user'] in connected:
        await error(websocket, json.dumps({ 'type': 'error', 'message': 'Error: User already connected' }) )
    else:
        connected[message['user']] = websocket
        print(message)
        print(connected)
        websockets.broadcast(list(connected.values()), json.dumps({ 'type': 'join', 'user': message['user'] }) )

async def handler(websocket):
    async for message in websocket:
        event = json.loads(message)
        print(event)

        if event['type'] == 'chat':
            print(event)
            await chat(websocket, event)
        
        if event['type'] == 'join':
            await join(websocket, event)


async def main():
    async with serve(handler, '0.0.0.0', 42069):
        print("Starting server")
        await asyncio.Future()

asyncio.run(main())
