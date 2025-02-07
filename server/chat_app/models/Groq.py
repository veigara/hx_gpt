import logging
from groq import Groq

from .base_model import BaseLLMModel
from ..config import groq_api_key
from ..presets import *

logger = logging.getLogger("chat_app")


class Groq_Client(BaseLLMModel):
    def __init__(
        self, model_key, api_key, user_name, agent_id=None, history_id=None
    ) -> None:
        super().__init__(
            model_key=model_key,
            user_name=user_name,
            agent_id=agent_id,
            history_id=history_id,
            config={"api_key": api_key},
        )
        self.client = Groq(
            api_key=groq_api_key() if api_key is None else api_key,
            base_url=self.api_host,
        )

    def _get_groq_style_input(self):
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
                    top_p=agent_data.get("top_p"),
                    stream=stream,
                    presence_penalty=agent_data.get("presence_penalty"),
                    frequency_penalty=agent_data.get("frequency_penalty"),
                )
        except Exception as e:
            status_code = e.__getattribute__("status_code")
            if status_code == 403:
                raise Exception(ERROR_RETRIEVE_MSG)
            body = e.__getattribute__("body")
            raise Exception(f"{STANDARD_ERROR_MSG}:{body}")

    def get_answer_stream_iter(self):
        messages = self.get_history_limits()
        completion = self._create_completion(messages, stream=True)

        partial_text = ""
        for chunk in completion:
            partial_text += chunk.choices[0].delta.content or ""

        return partial_text

    def get_answer_at_once(self):
        """单次对话"""
        messages = self.get_agent_current_input()
        completion = self._create_completion(messages, stream=True)

        partial_text = ""

        for chunk in completion:
            partial_text += chunk.choices[0].delta.content or ""

        return partial_text
