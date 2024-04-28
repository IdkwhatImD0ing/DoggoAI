import asyncio
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
        self.count = 0
        
    def start(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.play_audio())
    
    async def play_audio(self):
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=26000,
            output=True,
        )
        while True:
            try:
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
                # audio_segment.export(f"output_{self.count}.wav", format="wav")
                # self.count += 1
                
                # Play the audio
                self.text += message
                
                frame_count = int(audio_segment.frame_rate * 0.1)  # Calculate frame count for 0.1 seconds
                total_frames = len(audio_segment.get_array_of_samples())
                print("AudioOutput - Playing audio:", message)
                for i in range(0, total_frames, frame_count):
                    if self.stop_event.is_set():
                        print("AudioOutput - Stop Triggered")
                        
                        # Clear the queue
                        while not self.audio_queue.empty():
                            print("AudioOutput - Clearing the audio queue.")
                            self.audio_queue.get_nowait()
                            self.audio_queue.task_done()
                            
                        if self.text != "":
                            self.history += [{"role": "assistant", "content": self.text + "User Interrupted"}]
                            self.text = ""
                            
                        break
                        
                    end_frame = min(i + frame_count, total_frames)
                    chunk = audio_segment[i:end_frame].raw_data
                    stream.write(chunk) 
            except Exception as e:
                print("AudioOutput - Error:", e)
                continue
                
            
            
            