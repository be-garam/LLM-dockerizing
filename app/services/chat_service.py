from openai import OpenAI, OpenAIError
from app.core.config import settings
from collections import defaultdict
import threading

class ChatService:
    def __init__(self):
        self.api = OpenAI(base_url=settings.OPENAI_API_ROOT, api_key=settings.OPENAI_API_KEY)
        # Rest of the code remains the same
        self.model = self.api.models.list().data[0].id
        self.hist = defaultdict(str)
        self.hist_thread = None

    def call_api(self, messages):
        completion = self.api.chat.completions.create(
          model=self.model,
          messages=messages,
          extra_body={"stop_token_ids": [128001, 128009]}
        )
        return completion.choices[0].message.content

    def chat(self, chat_input, stream_id):
        if self.hist_thread:
            self.hist_thread.join()
        messages = [
          {"role": "system", "content": f"You are a helpful assistant. Always be truthful. If you are unsure, mention you don't know it. Always answer in the same language as the given question. If you unsure which language it is, answer in English. Previous chat context: {self.hist[stream_id]}"},
        ]
        messages.append({"role": "user", "content": chat_input})
        try:
            chat_output = self.call_api(messages)
        except OpenAIError as e:
            chat_output = str(e)
        self.hist_thread = threading.Thread(target=self.save_history, args=(stream_id, chat_input, chat_output))
        self.hist_thread.start()
        return chat_output

    def save_history(self, stream_id, q, a):
        messages = [
          {"role": "system", "content": "Summarize the given conversation so that you still understand what was the topic. Reduce the text as much as possible. Previous chat context:\n" + self.hist[stream_id]},
          {"role": "user", "content": f"user:\n{q}\nbot:\n{a}"}
        ]
        try:
            chat_output = self.call_api(messages)
            if chat_output:
                self.hist[stream_id] = chat_output
        except OpenAIError:
            pass