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
            # If the stop event is set, wait for clear without doing anything
            while self.stop_event.is_set():
                await asyncio.sleep(1)

            get_task = asyncio.create_task(self.sentence_queue.get())
            stop_task = asyncio.create_task(self.stop_event.wait())
            # Wait for either the sentence queue to have an item or the stop event to be set
            done, pending = await asyncio.wait(
                [get_task, stop_task], return_when=asyncio.FIRST_COMPLETED
            )

            # Handle tasks that are completed
            if get_task in done:
                item = get_task.result()  # Retrieve the item from the queue task
                self.sentence_queue.task_done()
                print("AudioGenerator - Processing item:", item)

                try:
                    # Wait for the previous task to finish
                    await self.send_and_receive(item)
                # Catch disconnect error
                except websockets.exceptions.ConnectionClosedError:
                    print("Websocket connection is closed.")
                    self.websocket = await websockets.connect(websocket_url)
                    # Wait for the previous task to finish
                    await self.send_and_receive(item)

            if stop_task in done:
                print("AudioGenerator - Stop event was triggered.")
                # Clear the queue
                while not self.sentence_queue.empty():
                    self.sentence_queue.get_nowait()
                    self.sentence_queue.task_done()

            for task in pending:
                task.cancel()

    async def send_and_receive(self, sentence):

        if self.stop_event.is_set():
            self.clear_queue()
            print("AudioGenerator - Stop event was triggered.")
            return

        if sentence == None:
            await self.audio_queue.put(None)
            return
        try:
            await self.websocket.send(
                json.dumps({"type": "assistant_input", "text": sentence})
            )
        except Exception as e:
            print("AudioGenerator - Failed to send to server:", str(e))

        if self.stop_event.is_set():
            self.clear_queue()
            print("AudioGenerator - Stop event was triggered.")
            return

        while True:
            data = json.loads(await self.websocket.recv())
            if "data" in data:
                break

        if self.stop_event.is_set():
            self.clear_queue()
            print("AudioGenerator - Stop event was triggered.")
            return

        await self.audio_queue.put({"text": sentence, "audio": data["data"]})

        print("AudioGenerator - Added to audio queue:", sentence)

    async def connect_websocket(self):
        print("Connecting to websocket...")
        self.websocket = await websockets.connect(websocket_url)

    def clear_queue(self):
        while not self.sentence_queue.empty():
            self.sentence_queue.get_nowait()
            self.sentence_queue.task_done()
