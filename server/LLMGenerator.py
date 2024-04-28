import asyncio
from openai import AsyncOpenAI
from utils import text_chunker


class LLMGenerator:
    def __init__(self, interruption_queue, sentence_queue, history, stop_event):
        self.interruption_queue = interruption_queue
        self.sentence_queue = sentence_queue
        self.client = AsyncOpenAI()
        self.history = history
        self.stop_event = stop_event # asyncio.event
        self.current_task = None 
        
    def start(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.process_items())

    async def process_items(self):
        while True:
            while self.stop_event.is_set():
                if self.current_task and not self.current_task.done():
                    self.current_task.cancel()
                await asyncio.sleep(1)

            get_task = asyncio.create_task(self.interruption_queue.get())
            stop_task = asyncio.create_task(self.stop_event.wait())
            
            # Wait for both the interruption queue to have an item and the stop event to be set
            done, pending = await asyncio.wait([get_task, stop_task], return_when=asyncio.FIRST_COMPLETED)   
            
            if get_task in done:
                item = get_task.result()
                self.interruption_queue.task_done()
                print("LLM Generator - Processing item:", item)
                self.history.append({"role": "user", "content": item})
                self.current_task = asyncio.create_task(self.process_llm(item))

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

    async def process_llm(self, text):
        # print("Current history:", self.history)
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo",
            stream=True,
            max_tokens=500,
            messages=self.history + [{"role": "user", "content": text}],
        )
        text_generator = text_chunker(response)
        async for chunk in text_generator:
            if self.stop_event.is_set():
                break
            await self.sentence_queue.put(chunk)
            print("LLMGenerator - Putting chunk in sentence queue:", chunk)

    
