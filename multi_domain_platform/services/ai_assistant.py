from typing import List, Dict
from openai import OpenAI
class AIAssistant:
    def __init__(self, system_prompt: str = "You are a helpful assistant."):
        self._system_prompt = system_prompt
        self._history: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]

    def set_system_prompt(self, prompt: str):
        self._system_prompt = prompt
        self.clear_history()
        self._history.append({"role": "system", "content": prompt})

    def send_message(self, user_message: str, client: OpenAI):
        # Add user message
        self._history.append({"role": "user", "content": user_message})

        # Call OpenAI API
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=self._history,
            stream=True
        )

        # Stream response
        full_reply = ""
        for chunk in completion:
            delta = chunk.choices[0].delta
            if delta.content:
                full_reply += delta.content
        # Add assistant response to history
        self._history.append({"role": "assistant", "content": full_reply})
        return full_reply

    def clear_history(self):
        self._history = [{"role": "system", "content": self._system_prompt}]