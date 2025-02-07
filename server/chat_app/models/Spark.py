import logging

from openai import OpenAI

from ..presets import *
from .base_model import BaseLLMModel
from ..config import spark_api_key
import requests
import json

logger = logging.getLogger("chat_app")


class Spark_Client(BaseLLMModel):
    def __init__(self, model_key, api_key, user_name, agent_id, history_id) -> None:
        super().__init__(
            model_key=model_key,
            user_name=user_name,
            agent_id=agent_id,
            history_id=history_id,
            config={"api_key": api_key},
        )
        self.client = OpenAI(api_key=spark_api_key(), base_url=SPARK_BASE_URL)

    def _get_spark_style_input(self):
        messages = [*self.get_history()]
        return messages

    def _create_completion(self, messages, stream):
        try:
            agent_data = self.agent_data
            if not agent_data:
                return self.client.chat.completions.create(
                    model=self.model_key,
                    messages=messages,
                    stream=stream,
                )
            else:
                return self.client.chat.completions.create(
                    model=self.model_key,
                    messages=messages,
                    temperature=agent_data.get("temperature"),
                    max_tokens=agent_data.get("max_tokens"),
                    stream=stream,
                )
        except Exception as e:
            status_code = e.__getattribute__("status_code")
            if status_code == 502:
                raise Exception(ERROR_RETRIEVE_MSG)
            body = e.__getattribute__("body")
            raise Exception(f"{STANDARD_ERROR_MSG}:{body}")

    def get_answer_at_once(self):
        messages = self.get_agent_current_input()

        return self._send_message(messages, True)

    def get_answer_stream_iter(self):
        messages = self.get_history_limits()

        return self._send_message(messages, True)

    def _send_message(self, messages, stream) -> str:
        completion = self._create_completion(messages, stream=True)
        partial_text = ""
        for chunk in completion:
            partial_text += chunk.choices[0].delta.content or ""

        return partial_text
