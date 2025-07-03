import asyncio
import websockets

async def send_audio():
    uri = "wss://uzscbp093r2me5-7860.proxy.runpod.net/stream"
    async with websockets.connect(uri) as websocket:
        with open("output.wav", "rb") as audio:
            chunk = audio.read(2048)
            while chunk:
                await websocket.send(chunk)
                chunk = audio.read(2048)
                await asyncio.sleep(0.05)
        await websocket.close()
        # Done sending — now wait for server to respond
        response = await websocket.recv()
        print("Transcription:", response)

asyncio.run(send_audio())
