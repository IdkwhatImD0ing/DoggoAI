import asyncio
import websockets
import os
import json

HUME_API_KEY = os.getenv("HUME_API_KEY")
websocket_url = f"wss://api.hume.ai/v0/evi/chat?api_key={HUME_API_KEY}"

class AudioGenerator:
    def __init__(self, sentence_queue, audio_queue, stop_event):
        self.sentence_queue = sentence_queue
        self.audio_queue = audio_queue
        self.websocket = None
        self.stop_event = stop_event
        
    def start(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.process_items())
        loop.create_task(self.connect_websocket())
    
    async def process_items(self):
        while True:
            while not self.stop_event.is_set():
                item = await self.sentence_queue.get()
                
                self.sentence_queue.task_done()
                
                try:
                    await self.send_and_receive(item)
                # Catch disconnect error
                except websockets.exceptions.ConnectionClosedError:
                    print("Websocket connection is closed.")
                    self.websocket = await websockets.connect(websocket_url)
                    await self.send_and_receive(item)
            
            # Clear the queue
            while not self.sentence_queue.empty():
                self.sentence_queue.get_nowait()
                self.sentence_queue.task_done()
                
                
    async def send_and_receive(self, sentence):
        if sentence == None:
            await self.audio_queue.put(None)
            return
        await self.websocket.send(
            json.dumps(
                {"type": "assistant_input", "text": sentence}
            )
        )
        
        while True:
            data = json.loads(await self.websocket.recv())
            if "data" in data:
                break
        
        await self.audio_queue.put({
            "text": sentence,
            "audio": data['data']
        })
    
    async def connect_websocket(self):
        print("Connecting to websocket...")
        self.websocket = await websockets.connect(websocket_url)
        