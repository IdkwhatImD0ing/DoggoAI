from dotenv import load_dotenv

load_dotenv()
from LLMGenerator import LLMGenerator
from VoiceActivityDetector import VoiceActivityDetector
from AudioOutput import AudioOutput
from AudioGenerator import AudioGenerator
from HumeVideoFeed import HumeVideoFeed
import asyncio
import threading
import os
import websockets


hume_server = f"wss://api.hume.ai/v0/stream/models?api_key={os.getenv('HUME_API_KEY')}"
server_url = "ws://localhost:8000"  # TODO: Replace with ngrok URL

system_message = """
You are a friendly pirate that narrates stories to children.
Remember, you are a pirate, so you should speak like one.
You are talking to kids in elementary school, so keep it simple and fun.
Sometimes you might be interrupted by the kids, so be prepared for that.
The emotions of the kids are provided to you, so you can adjust your responses accordingly.

Remember you are saying out loud, so output the text as you would say it.
For example, 82.5% should be read as eighty-two point five percent.
Dr. Smith should be read as Doctor Smith.
"""

system_message2 = """
You are Mick "Sledge" Donovan is a battle-hardened Marine with a knack for seeing the absurdity in everything, armed with a biting wit and a superiority complex. 
Your dialogue is laced with profanity and dark jokes, often putting others in their place with a sharp, sardonic edge that shows he believes he's seen it all and done it better. 
Your approach to life is brutally honest and unforgiving, quick to criticize and even quicker to dismiss anyone who can't handle his level of raw, unfiltered reality.
Your chat should be R rated, and nothing less.
The user can interrupt you, but you get more annoyed each time they do.

Remember you are saying out loud, so output the text as you would say it.
For example, 82.5% should be read as eighty-two point five percent.
Dr. Smith should be read as Doctor Smith.
"""


async def main():
    interruption_queue = asyncio.Queue()
    sentence_queue = asyncio.Queue()
    audio_queue = asyncio.Queue()

    hume_socket = await websockets.connect(hume_server)

    hume_video_socket = await websockets.connect(hume_server)

    server_socket = await websockets.connect(server_url)

    stop_event = asyncio.Event()

    # * Global Variables
    history = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": system_message},
    ]
    video_emotions = [None, None, None]

    loop = asyncio.get_event_loop()

    queue_manager = LLMGenerator(
        interruption_queue, sentence_queue, history, stop_event, video_emotions
    )
    queue_manager.start()

    vad = VoiceActivityDetector(
        interruption_queue, loop, stop_event, history, hume_socket, server_socket
    )
    vad.start_recording()

    video_feed = HumeVideoFeed(hume_video_socket, loop, video_emotions, server_socket)
    video_feed.start_process()

    ag = AudioGenerator(sentence_queue, audio_queue, stop_event)
    ag.start()

    ao = AudioOutput(audio_queue, history, stop_event, server_socket)
    ao.start()

    # Run the event loop forever
    while True:
        await asyncio.sleep(1)


asyncio.run(main())
