import asyncio
import json

import websockets
from websockets.server import serve

from game import Game

connected = {}
game = Game()

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

async def chat(websocket, message):
    # Send the chat message to everybody except the person who sent it
    others = connected
    del others[message['user']]
    await websockets.broadcast(others, message)

async def error(websocket, message):
    await websocket.send(message)

async def join(websocket, message):
    if message['user'] in connected:
        await error(websocket, json.dumps({ 'type': 'error', 'message': 'Error: User already connected' }) )
    else:
        connected[message['user']] = websocket
        websockets.broadcast(connected.values, json.dumps({ 'type': 'join', 'user': message['user'] }) )

async def handler(websocket):
    async for message in websocket:
        event = json.loads(message)

        if event['type'] == 'chat':
            await chat(websocket, message)
        
        if event['type'] == 'join':
            await join(websocket, message)


async def main():
    async with serve(echo, '0.0.0.0', 42069):
        await asyncio.Future()

asyncio.run(main())
