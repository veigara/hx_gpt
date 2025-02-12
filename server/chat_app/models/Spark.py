import logging

from openai import OpenAI
from django.http import StreamingHttpResponse
from django.db import transaction

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
        """单次对话"""
        full_content = []
        save_required = True  # 用于跟踪是否需要保存

        return StreamingHttpResponse(
            self.event_stream(full_content, save_required, None, None, True),
            content_type="text/event-stream",
        )

    def get_answer_stream_iter(self, history_id, user_content):
        full_content = []
        save_required = True  # 用于跟踪是否需要保存

        return StreamingHttpResponse(
            self.event_stream(
                full_content, save_required, history_id, user_content, False
            ),
            content_type="text/event-stream",
        )

    def update_history_record(self, history_id, user_content, full_content):
        """更新历史记录"""
        super().update_history_record(history_id, user_content, full_content)

    def event_stream(
        self, full_content, save_required, history_id, user_content, is_once: bool
    ):
        """发布stram流"""

        try:
            if not is_once:
                messages = self.get_history_limits()
            else:
                messages = self.get_agent_current_input()
            response = self._create_completion(messages, stream=True)

            for chunk in response:
                if content := chunk.choices[0].delta.content:
                    full_content.append(content)
                    # 添加格式标识前缀,保证前端格式
                    show_content = content.replace("\r\n", "\n").replace("\n", "<br>")
                    formatted_content = f"[TEXT]{show_content}[/TEXT]"
                    # SSE格式
                    yield f"data: {formatted_content}\n\n"

        except Exception as e:
            save_required = False
            yield f"event: error\ndata: {str(e)}\n\n"
            raise
        finally:
            # 确保在流结束时保存
            if save_required and full_content:
                full_content = "".join(full_content)
                logger.info(f"模型输出为：{full_content}")
                if not is_once:
                    with transaction.atomic():
                        self.update_history_record(
                            history_id, user_content, full_content
                        )
