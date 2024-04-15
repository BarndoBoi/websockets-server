import asyncio

from websockets.server import serve

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

async def main():
    async with serve(echo, '0.0.0.0', 42069):
        await asyncio.Future()

asyncio.run(main())
