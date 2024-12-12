import json
import logging
import textwrap
import uuid

import os
from openai import OpenAI


from ..utils import count_token, construct_system
from .base_model import BaseLLMModel
from ..config import lmstudio_api_key, lmstudio_host

logger = logging.getLogger("chat_app")


class LMStudio_Client(BaseLLMModel):
    def __init__(self, model_name, api_key, user_name="") -> None:
        super().__init__(
            model_name=model_name, user=user_name, config={"api_key": api_key}
        )
        self.client = OpenAI(
            base_url="http://" + lmstudio_host() + "/v1",
            api_key=lmstudio_api_key(),
        )

    def _get_lm_style_input(self):
        messages = [construct_system(self.system_prompt), *self.history]
        return messages

    def get_answer_at_once(self):
        messages = self._get_lm_style_input()
        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=self.model_name,
        )
        return (
            chat_completion.choices[0].message.content,
            chat_completion.usage.total_tokens,
        )

    def get_answer_stream_iter(self):
        messages = self._get_lm_style_input()
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature,
            max_tokens=(
                self.max_generation_token
                if self.max_generation_token is not None
                else -1
            ),
            top_p=self.top_p,
            stream=True,
            stop=self.stop_sequence,
        )

        partial_text = ""
        for chunk in completion:
            partial_text += chunk.choices[0].delta.content or ""
            yield partial_text
