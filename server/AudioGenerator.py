import asyncio
import websockets
import os
import json

HUME_API_KEY = os.getenv("HUME_API_KEY")
websocket_url = f"wss://api.hume.ai/v0/evi/chat?api_key={HUME_API_KEY}"

class AudioGenerator:
    def __init__(self, sentence_queue, audio_queue, flag):
        self.sentence_queue = sentence_queue
        self.audio_queue = audio_queue
        self.websocket = None
        self.flag = flag
        
    def start(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.process_items())
        loop.create_task(self.connect_websocket())
    
    async def process_items(self):
        while True:
            # if (not self.flag):
            #     item = await self.sentence_queue.get()
            # else:
            #     self.sentence_queue = asyncio.Queue()
            #     continue
            item = await self.sentence_queue.get()
            
            self.sentence_queue.task_done()
            
            try:
                await self.send_and_receive(item)
            # Catch disconnect error
            except websockets.exceptions.ConnectionClosedError:
                print("Websocket connection is closed.")
                self.websocket = await websockets.connect(websocket_url)
                await self.send_and_receive(item)
                
                
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
        