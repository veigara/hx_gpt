from ..presets import *
from enum import Enum
import logging
from ..utils import *
from ..config import set_default_model_params, get_default_model_params
from ..service.agent import *
from ..service.history import *
from ..cache_utils import *

logger = logging.getLogger("chat_app")


class BaseLLMModel:
    def __init__(
        self,
        model_name,
        user_name="",
        agent_id=None,
        history_id=None,
        config=None,
    ) -> None:
        # 设置默认的模型参数
        set_default_model_params()
        # 使用全局变量 MODEL_METADATA 获取模型参数
        MODEL_METADATA = get_default_model_params()
        if config is not None:
            temp = MODEL_METADATA[model_name].copy()
            keys_with_diff_values = {
                key: temp[key]
                for key in temp
                if key in DEFAULT_METADATA and temp[key] != DEFAULT_METADATA[key]
            }
            config.update(keys_with_diff_values)
            temp.update(config)
            config = temp
        else:
            config = MODEL_METADATA[model_name]

        self.api_key = config["api_key"]
        self.api_host = config["api_host"]
        self.stream = config["stream"]
        self.model_name = config["model_name"]

        self.user_name = user_name
        self.agent_id = agent_id
        self.history_id = history_id
        self.config = config

        if user_name is None:
            raise ValueError("user_name is None")

        history_data = self.get_history()
        if len(history_data) == 0:
            # 初始化历史记录
            history_data = load_history(user_name=user_name, id=history_id)
            if history_data is not None:
                for data in history_data.get("content", []):
                    self.set_history(data)
        agent_data = self.get_agent_data()
        if len(agent_data) == 0:
            # 初始化智能体配置
            agent_list = get_user_all_agents(self.user_name, None)
            for agent in agent_list:
                if agent["id"] == agent_id:
                    self.set_agent_data(agent)
                    break

    def stream_next_chatbot(self, inputs, history_id, agent_id) -> str:
        """发送一个回答"""
        logger.info(f"用户输入为：{inputs}")
        user_content = construct_user(inputs)
        self.set_history(user_content)
        stream_iter = self.get_answer_stream_iter()
        logger.info(f"模型输出为：{stream_iter}")
        assistant_content = construct_assistant(stream_iter)
        self.set_history(construct_assistant(stream_iter))
        # 修改文件
        update_history(
            self.user_name,
            history_id,
            [user_content, assistant_content],
            self.get_agent_data(),
        )

        return stream_iter

    def get_answer_stream_iter(self):
        """Implement stream prediction.
        Conversations are stored in self.history, with the most recent question in OpenAI format.
        Should return a generator that yields the next word (str) in the answer.
        """
        logger.warning(
            "Stream prediction is not implemented. Using at once prediction instead."
        )
        response, _ = self.get_answer_at_once()
        yield response

    def set_history(self, history):
        set_history_global(self.user_name, history)

    def get_history(self):
        return get_history_global(self.user_name)

    def clear_history(self):
        clear_history_global(self.user_name)

    def set_agent_data(self, data):
        set_agent_data_global(self.user_name, data)

    def get_agent_data(self):
        return get_agent_data_global(self.user_name)


class ModelType(Enum):
    Unknown = -1
    Groq = 1
    LMStudio = 2

    @classmethod
    def get_type(cls, model_name: str):
        # 1. get model type from model metadata (if exists)
        model_type = MODEL_METADATA[model_name]["model_type"]
        if model_type is not None:
            for member in cls:
                if member.name == model_type:
                    return member

        # 2. infer model type from model name
        model_type = None
        model_name_lower = model_name.lower()

        if "groq" in model_name_lower:
            model_type = ModelType.Groq

        else:
            model_type = ModelType.LMStudio
        return model_type
