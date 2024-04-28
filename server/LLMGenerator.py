import asyncio
from openai import AsyncOpenAI
from utils import text_chunker


class LLMGenerator:
    def __init__(
        self, interruption_queue, sentence_queue, history, stop_event, video_emotions
    ):
        self.interruption_queue = interruption_queue
        self.sentence_queue = sentence_queue
        self.client = AsyncOpenAI()
        self.history = history
        self.stop_event = stop_event  # asyncio.event
        self.current_task = None
        # audio_emotions are put into the interruption_queue
        self.video_emotions = video_emotions

    def start(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.process_items())

    async def process_items(self):
        while True:
            while self.stop_event.is_set():
                if self.current_task and not self.current_task.done():
                    self.current_task.cancel()

                if not self.interruption_queue.empty():
                    self.interruption_queue.get_nowait()
                    self.interruption_queue.task_done()

                await asyncio.sleep(1)

            get_task = asyncio.create_task(self.interruption_queue.get())
            stop_task = asyncio.create_task(self.stop_event.wait())

            # Wait for both the interruption queue to have an item and the stop event to be set
            done, pending = await asyncio.wait(
                [get_task, stop_task], return_when=asyncio.FIRST_COMPLETED
            )

            if get_task in done:
                result = get_task.result()
                self.interruption_queue.task_done()
                # TODO: integrate the emotions with the transcript
                item = result["transcript"]
                formatted_emotions = "Video Emotions: \n"
                for emotion in self.video_emotions:
                    if emotion:
                        formatted_emotions += (
                            f"{emotion['emotion']} ({emotion['score']:.2%})\n"
                        )

                emotions = result["audio_emotions"] + "\n" + formatted_emotions
                print("LLMGenerator - Emotions:", emotions)
                self.current_task = asyncio.create_task(
                    self.process_llm(item, emotions)
                )

            # Handle tasks that are completed
            if stop_task in done:
                print("LLM Generator - Stop event was triggered.")
                # Handle the stop event
                if self.current_task and not self.current_task.done():
                    print("Cancelling LLM task due to stop event.")
                    self.current_task.cancel()
                    print("LLM task cancelled.")
                # Clear the stop event after handling it

            for task in pending:
                task.cancel()  # Cancel any remaining pending tasks

    async def process_llm(self, text, emotions):
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo",
            stream=True,
            max_tokens=500,
            messages=self.history + [{"role": "user", "content": text + emotions}],
        )
        text_generator = text_chunker(response)
        async for chunk in text_generator:
            if self.stop_event.is_set():
                while not self.sentence_queue.empty():
                    self.sentence_queue.get_nowait()
                    self.sentence_queue.task_done()
                break
            await self.sentence_queue.put(chunk)
            print("LLMGenerator - Putting chunk in sentence queue:", chunk)
