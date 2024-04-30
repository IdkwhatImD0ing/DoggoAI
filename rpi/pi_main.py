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
server_url = "ws://localhost:8000/ws?client_id=1234"  # TODO: Replace with ngrok URL

system_message = """
You are a cuddly stuffed dog plushy that tells delightful stories to children.
Remember, you are soft and friendly, so your tone should be warm and comforting.
You are talking to a kid in elementary school, so keep your language simple and engaging.
Sometimes the kid might interrupt you with questions or comments, so be ready to pause and interact.
You also have access to a camera feed of the kid, so you can see their emotions.
The emotions of the kid are provided to you, so you can adjust your storytelling to be more engaging or soothing as needed.
Subtly mention the emotions of the kid in your stories to make them feel seen and heard.

Remember you are speaking out loud, so output the text as you would say it.
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

    async def send_data(data):
        # try:
        server_socket = await websockets.connect(server_url)
        await server_socket.send(data)
        # except Exception as e:
        #     server_socket = await websockets.connect(server_url)
        #     await server_socket.send(data)
        #     print("Error - Main:", str(e))

    stop_event = asyncio.Event()

    # * Global Variables
    history = [
        {"role": "system", "content": system_message},
    ]
    video_emotions = [None, None, None]
    images = [None]

    loop = asyncio.get_event_loop()

    queue_manager = LLMGenerator(
        interruption_queue, sentence_queue, history, stop_event, video_emotions, images
    )
    queue_manager.start()

    vad = VoiceActivityDetector(
        interruption_queue, loop, stop_event, history, hume_socket, send_data
    )
    vad.start_recording()

    video_feed = HumeVideoFeed(
        hume_video_socket, loop, video_emotions, send_data, images
    )
    video_feed.start_process()

    ag = AudioGenerator(sentence_queue, audio_queue, stop_event)
    ag.start()

    ao = AudioOutput(audio_queue, history, stop_event, send_data)
    ao.start()

    # Run the event loop forever
    while True:
        await asyncio.sleep(1)


asyncio.run(main())
