from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from app.core.config import settings
from collections import defaultdict
import threading

class ChatService:
    def __init__(self):
        self.model_name = settings.MODEL_NAME
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name, torch_dtype=torch.float16, device_map="auto")
        self.hist = defaultdict(str)
        self.hist_thread = None

    def call_api(self, messages):
        full_prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=100,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.7
            )
        
        response = self.tokenizer.decode(outputs[0][inputs['input_ids'].shape[-1]:], skip_special_tokens=True)
        return response

    def chat(self, chat_input, stream_id):
        if self.hist_thread:
            self.hist_thread.join()
        messages = [
          {"role": "system", "content": f"You are a helpful assistant. Always be truthful. If you are unsure, mention you don't know it. Always answer in the same language as the given question. If you unsure which language it is, answer in English. Previous chat context: {self.hist[stream_id]}"},
          {"role": "user", "content": chat_input}
        ]
        try:
            chat_output = self.call_api(messages)
        except Exception as e:
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
        except Exception:
            pass