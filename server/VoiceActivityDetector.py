import pyaudio
import numpy as np
import threading
import collections
import wave
import io
import asyncio
import base64
from concurrent.futures import ThreadPoolExecutor
from openai import AsyncOpenAI
import json


class VoiceActivityDetector:
    def __init__(
        self,
        interruption_queue,
        loop,
        stop_event,
        history,
        hume_socket,
        rate=16000,
        format=pyaudio.paInt16,
        channels=1,
        chunk_size=512,
        silence_threshold=200,
    ):
        self.loop = loop
        self.stop_event = stop_event  #! TODO: Implement flagging code
        self.history = history
        self.hume_socket = hume_socket
        self.interruption_queue = interruption_queue  # Interruption Queue
        self.rate = rate
        self.format = format
        self.channels = channels
        self.chunk_size = chunk_size
        self.silence_threshold = silence_threshold
        self.count = 0

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            rate=self.rate,
            format=self.format,
            channels=self.channels,
            input=True,
            frames_per_buffer=self.chunk_size,
        )
        self.audio_buffer = collections.deque(
            maxlen=int((self.rate // self.chunk_size) * 0.5)
        )
        self.frames = []
        self.long_term_noise_level = 0.0
        self.current_noise_level = 0.0
        self.voice_activity_detected = False
        self.is_recording = False
        self.executor = ThreadPoolExecutor(max_workers=1)

        self.client = AsyncOpenAI()

    def get_levels(self, data):
        pegel = np.abs(np.frombuffer(data, dtype=np.int16)).mean()
        self.long_term_noise_level = self.long_term_noise_level * 0.995 + pegel * (
            1.0 - 0.995
        )
        self.current_noise_level = self.current_noise_level * 0.920 + pegel * (
            1.0 - 0.920
        )
        return pegel, self.long_term_noise_level, self.current_noise_level

    def start_recording(self):
        self.is_recording = True
        self.thread = threading.Thread(target=self.record)
        self.thread.start()

    def stop_recording(self):
        self.is_recording = False
        self.thread.join()

    def record(self):
        ambient_noise_level = 0
        print("Start speaking.")
        while self.is_recording:
            data = self.stream.read(self.chunk_size, exception_on_overflow=False)
            pegel, long_term_noise_level, current_noise_level = self.get_levels(data)
            self.audio_buffer.append(data)

            if (
                not self.voice_activity_detected
                and current_noise_level > long_term_noise_level + self.silence_threshold
            ):
                self.voice_activity_detected = True
                print("Listening.")
                self.stop_event.set()
                ambient_noise_level = long_term_noise_level
                self.frames.extend(list(self.audio_buffer))

            if self.voice_activity_detected:
                self.frames.append(data)
                if current_noise_level < ambient_noise_level + 100:
                    print("Stopped listening.")
                    self.stop_event.clear()
                    self.send_voice_data(b"".join(self.frames))
                    self.frames.clear()
                    self.voice_activity_detected = False

    def send_voice_data(self, audio_data):
        # Transcribe audio data asynchronously and add to queue
        print("Transcribing...")
        asyncio.run_coroutine_threadsafe(
            self.transcribe_and_enqueue(audio_data), self.loop
        )

    async def transcribe_and_enqueue(self, audio_data):
        try:
            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, "wb") as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(audio_data)
            wav_data = wav_buffer.getvalue()

            # Save to file
            # with open(f"input{self.count}.wav", "wb") as f:
            #     self.count +=1
            #     f.write(wav_data)
            audio_stream = io.BytesIO(wav_data)
            audio_stream.name = "audio.wav"

            # Save as wav file
            with open("audio.wav", "wb") as f:
                f.write(wav_data)

            transcript_task = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_stream,
                response_format="text",
                language="en",
            )

            # base64 encode wav
            base64_audio = base64.b64encode(wav_data).decode()

            audio_task = self.process_hume(base64_audio)

            transcript, audio_emotions = await asyncio.gather(
                transcript_task, audio_task
            )
            print("VoiceActivityDetector - Emotions:", audio_emotions)

            # TODO: pass audio and video to GPT
            emotional_context_transcript = {
                "transcript": transcript,
                "audio_emotions": audio_emotions,
            }

            await self.interruption_queue.put(emotional_context_transcript)
            self.history.append({"role": "user", "content": transcript})
            print("VoiceActivityDetector - Added to queue:", transcript)

        except Exception as e:
            print("Failed to transcribe:", str(e))

    async def process_hume(self, audio_base64):
        data = {"data": audio_base64, "models": {"prosody": {}}}

        await self.hume_socket.send(json.dumps(data))

        response = await self.hume_socket.recv()
        response = json.loads(response)

        # * Emotions has {"name": "anger", "score": 0.5}
        emotions = (
            response.get("prosody", {}).get("predictions", [])[0].get("emotions", [])
        )
        # Find top 3 emotions and format them
        emotions = sorted(emotions, key=lambda e: e["score"], reverse=True)[:3]
        pretty_emotions = "Voice Emotions:\n"
        for i, emotion in enumerate(emotions):
            pretty_emotions += (
                f"Emotion {i + 1}: {emotion['name']} ({emotion['score']:.2%})\n"
            )

        return pretty_emotions

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
