import json
import logging
import textwrap
import uuid

import os
from groq import Groq


from ..utils import construct_system
from .base_model import BaseLLMModel
from django.http import StreamingHttpResponse

logger = logging.getLogger("chat_app")


class Groq_Client(BaseLLMModel):
    def __init__(self, model_name, api_key, user_name, agent_id, history_id) -> None:
        super().__init__(
            model_name=model_name,
            user_name=user_name,
            agent_id=agent_id,
            history_id=history_id,
            config={"api_key": api_key},
        )
        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY") if api_key is None else api_key,
            base_url=self.api_host,
        )

    def _get_groq_style_input(self):
        messages = [*self.get_history()]
        return messages

    def get_answer_stream_iter(self):
        messages = self._get_groq_style_input()
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=self.get_agent_data().get("temperature"),
            max_tokens=self.get_agent_data().get("max_tokens"),
            top_p=self.get_agent_data().get("top_p"),
            stream=True,
            presence_penalty=self.get_agent_data().get("presence_penalty"),
            frequency_penalty=self.get_agent_data().get("frequency_penalty"),
        )

        partial_text = ""
        for chunk in completion:
            partial_text += chunk.choices[0].delta.content or ""

        return partial_text
