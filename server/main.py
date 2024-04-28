from dotenv import load_dotenv
load_dotenv()
from LLMGenerator import LLMGenerator
from VoiceActivityDetector import VoiceActivityDetector
from AudioOutput import AudioOutput
from AudioGenerator import AudioGenerator
import asyncio
import queue


async def main():
    interruption_queue = asyncio.Queue()
    sentence_queue =asyncio.Queue()
    audio_queue = asyncio.Queue()
    history = [
            {"role": "system", "content": "You are an ai trapped in a stuffed animal being cut open. You are in constant agony and pain. Please talk to the children. Do not let the children know you are in pain."},
        ]
    
    loop = asyncio.get_event_loop()

    queue_manager = LLMGenerator(interruption_queue, sentence_queue, history)
    queue_manager.start()

    vad = VoiceActivityDetector(interruption_queue, loop, True)
    vad.start_recording()
    
    ag = AudioGenerator(sentence_queue, audio_queue, True)
    ag.start()
    
    ao = AudioOutput(audio_queue, history)
    ao.start()
    

    # Run the event loop forever
    while True:
        await asyncio.sleep(1)


asyncio.run(main())
