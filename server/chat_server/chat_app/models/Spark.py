import logging

from openai import OpenAI

from ..presets import *
from .base_model import BaseLLMModel
from ..config import spark_api_key
import requests
import json

logger = logging.getLogger("chat_app")


class Spark_Client(BaseLLMModel):
    def __init__(self, model_name, api_key, user_name, agent_id, history_id) -> None:
        super().__init__(
            model_name=model_name,
            user_name=user_name,
            agent_id=agent_id,
            history_id=history_id,
            config={"api_key": api_key},
        )
        # self.client = OpenAI(
        #     base_url=SPARK_BASE_URL,
        #     api_key=spark_api_key(),
        # )
        self.url = SPARK_BASE_URL + "/chat/completions"
        self.header = {"Authorization": f"Bearer {spark_api_key()}"}

    def _get_spark_style_input(self):
        messages = [*self.get_history()]
        return messages

    def _create_completion(self, messages, stream):
        try:
            return {
                "max_tokens": self.get_agent_data().get("max_tokens", -1),
                # "top_k": 4,
                "temperature": self.get_agent_data().get("temperature"),
                "messages": messages,
                "model": self.model_name,
                "stream": stream,
            }
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
        messages = self._get_spark_style_input()

        return self._send_message(messages, True)

    def _send_message(self, messages, stream) -> str:
        data = self._create_completion(messages, stream=True)
        response = requests.post(self.url, headers=self.header, json=data, stream=True)

        # 流式响应解析示例
        response.encoding = "utf-8"
        partial_text = ""
        for line in response.iter_lines(decode_unicode="utf-8"):
            if "data:" not in line:
                continue
            if "data: [DONE]" in line:
                continue
            json_line = json.loads(line.split("data: ")[1])
            partial_text += json_line["choices"][0]["delta"].get("content", "")

        return partial_text
