import asyncio
import websockets
import os
import json
import pyaudio
import base64
from io import BytesIO
from pydub import AudioSegment


class AudioOutput:
    def __init__(self, audio_queue, history, stop_event):
        self.audio_queue = audio_queue
        self.history = history
        self.websocket = None
        self.flag = False
        self.text = ""
        self.stop_event = stop_event
        
    def start(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.play_audio())
    
    async def play_audio(self):
        # TODO: play the audio lollllllllllllllllllllllllll
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=26000,
            output=True,
        )
        while True:
            while not self.stop_event.is_set():
                data = await self.audio_queue.get()
                self.audio_queue.task_done()
                
                if data == None:
                    self.history += [{"role": "assistant", "content": self.text}]
                    self.text = ""
                    continue
                
                audio = base64.b64decode(data["audio"])
                message = data["text"]
                audio_segment = AudioSegment.from_file(BytesIO(audio))
                
                # Save the audio to a file
                audio_segment.export("output.wav", format="wav")
                
                # Play the audio
                print("Playing audio:", message)
                self.text += message
                stream.write(audio_segment.raw_data)
                
            # Clear the queue
            while not self.audio_queue.empty():
                self.audio_queue.get_nowait()
                self.audio_queue.task_done()
                
            if self.text != "":
                self.history += [{"role": "assistant", "content": self.text + "User Interrupted"}]
                self.text = ""
            
            