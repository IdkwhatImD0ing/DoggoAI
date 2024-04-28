import asyncio
from openai import AsyncOpenAI
from utils import text_chunker


class LLMGenerator:
    def __init__(self, interruption_queue, sentence_queue, history):
        self.interruption_queue = interruption_queue
        self.sentence_queue = sentence_queue
        self.client = AsyncOpenAI()
        self.history = history
        
    def start(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.process_items())

    async def process_items(self):
        while True:
            item = await self.interruption_queue.get()

            # Cancel the current task if it is running
            self.history.append({"role": "user", "content": item})

            # Start a new task for processing the item
            self.current_task = asyncio.create_task(self.process_llm(item))
            self.interruption_queue.task_done()

    async def process_llm(self, text):
        print("Current history:", self.history)
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo",
            stream=True,
            max_tokens=500,
            messages=self.history + [{"role": "user", "content": text}],
        )
        text_generator = text_chunker(response)
        async for chunk in text_generator:
            print("Generated text:", chunk)
            await self.sentence_queue.put(chunk)

    
