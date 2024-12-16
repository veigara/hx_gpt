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
    def __init__(self, model_name, api_key, user_name, agent_id, history_id) -> None:
        super().__init__(
            model_name=model_name,
            user_name=user_name,
            agent_id=agent_id,
            history_id=history_id,
            config={"api_key": api_key},
        )
        self.client = OpenAI(
            base_url="http://" + lmstudio_host() + "/v1",
            api_key=lmstudio_api_key(),
        )

    def _get_lm_style_input(self):
        messages = [*self.get_history()]
        return messages

    def get_answer_at_once(self):
        messages = self.get_agent_current_input()
        completion = self.client.chat.completions.create(
            messages=messages,
            model=self.model_name,
            temperature=self.get_agent_data().get("temperature"),
            max_tokens=(
                self.get_agent_data().get("max_tokens")
                if self.get_agent_data().get("max_tokens") is None
                else -1
            ),
            top_p=self.get_agent_data().get("top_p"),
            stream=True,
            presence_penalty=self.get_agent_data().get("presence_penalty"),
            frequency_penalty=self.get_agent_data().get("frequency_penalty"),
        )
        partial_text = ""
        for chunk in completion:
            partial_text += chunk.choices[0].delta.content or ""

        return partial_text

    def get_answer_stream_iter(self):
        messages = self._get_lm_style_input()
        completion = self.client.chat.completions.create(
            messages=messages,
            model=self.model_name,
            temperature=self.get_agent_data().get("temperature"),
            max_tokens=(
                self.get_agent_data().get("max_tokens")
                if self.get_agent_data().get("max_tokens") is None
                else -1
            ),
            top_p=self.get_agent_data().get("top_p"),
            stream=True,
            presence_penalty=self.get_agent_data().get("presence_penalty"),
            frequency_penalty=self.get_agent_data().get("frequency_penalty"),
        )
        partial_text = ""
        for chunk in completion:
            partial_text += chunk.choices[0].delta.content or ""

        return partial_text
