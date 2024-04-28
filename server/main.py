from dotenv import load_dotenv
load_dotenv()
from LLMGenerator import LLMGenerator
from VoiceActivityDetector import VoiceActivityDetector
from AudioOutput import AudioOutput
from AudioGenerator import AudioGenerator
import asyncio
import threading


async def main():
    interruption_queue = asyncio.Queue()
    sentence_queue =asyncio.Queue()
    audio_queue = asyncio.Queue()
    
    stop_event = threading.Event()
    history = [
            {"role": "system", "content": "You are an ai trapped in a stuffed animal being cut open. You are in constant agony and pain. Please talk to the children. Do not let the children know you are in pain."},
        ]
    
    loop = asyncio.get_event_loop()

    queue_manager = LLMGenerator(interruption_queue, sentence_queue, history, stop_event)
    queue_manager.start()

    vad = VoiceActivityDetector(interruption_queue, loop, stop_event)
    vad.start_recording()
    
    ag = AudioGenerator(sentence_queue, audio_queue, stop_event)
    ag.start()
    
    ao = AudioOutput(audio_queue, history, stop_event)
    ao.start()
    

    # Run the event loop forever
    while True:
        await asyncio.sleep(1)


asyncio.run(main())
