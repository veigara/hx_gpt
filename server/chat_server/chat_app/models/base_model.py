from ..presets import *
from enum import Enum
from duckduckgo_search import DDGS
from itertools import islice
import urllib3
import logging
import json
from ..utils import *
from ..config import get_default_model_params
from ..service.agent import *
from ..service.history import *
from ..cache_utils import *

logger = logging.getLogger("chat_app")


class BaseLLMModel:
    def __init__(
        self,
        model_key,
        user_name="",
        agent_id=None,
        history_id=None,
        config=None,
    ) -> None:
        """
        @param model_key: 模型名称

        """
        # 使用全局变量 MODEL_METADATA 获取模型参数
        config = get_default_model_params(user_name, model_key)

        self.api_key = config["api_key"]
        self.api_host = config["api_host"]
        self.stream = config["stream"]
        self.model_key = config["model_key"]
        self.max_content_len = config["max_content_len"]
        self.user_name = user_name
        self.agent_id = agent_id
        self.history_id = history_id
        self.config = config
        self.agent_history_data = []

        if user_name is None:
            raise ValueError("user_name is None")
        if history_id is not None:
            # 历史记录id存在才加载
            history_data = self.get_history()

            if len(history_data) == 0:
                # 初始化聊天记录
                history_data = load_history(user_name=user_name, id=history_id)
                if history_data is not None:
                    for data in history_data.get("content", []):
                        self.set_history(data)
        if agent_id is not None:
            agent_data = self.get_agent_data()
            if len(agent_data) == 0:
                # 初始化智能体配置
                self.init_agent_data(agent_id)
            else:
                # 判断当前智能体数据是否一样
                if agent_id != agent_data["id"]:
                    agent_data = self.init_agent_data(agent_id)

            self.agent_history_data = [*agent_data.get("content", [])]

    def stream_next_chatbot(self, inputs, history_id) -> str:
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
            max_content_len=self.max_content_len,
        )

        return stream_iter

    def get_answer_stream_iter(self):
        return "未实现功能"

    def get_answer_at_once(self):
        """没有上下文"""
        return "未实现功能"

    def get_answer_chatbot_at_once(self, inputs):
        """没有上下文，只回答一次"""
        """发送一个回答"""
        logger.info(f"用户输入为：{inputs}")
        user_content = construct_user(inputs)
        # 将当前内容保存
        self.input_txt = user_content
        stream_iter = self.get_answer_at_once()
        logger.info(f"模型输出为：{stream_iter}")

        return stream_iter

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

    def init_agent_data(self, agent_id) -> list:
        """初始化智能体配置"""
        agent_data = load_agent(self.user_name, agent_id)
        if agent_data is not None:
            self.set_agent_data(agent_data)
        else:
            agent_data = {}
        return agent_data

    def get_agent_current_input(self):
        """上下文只有智能体和当前对话的"""
        if self.agent_history_data is None:
            self.agent_history_data = []
        messages = [*self.agent_history_data, self.input_txt]
        return messages

    def online_search(self, input):
        """使用在线搜索"""
        search_results = []
        with DDGS(proxies=None) as ddgs:
            ddgs_gen = ddgs.text(input, backend="lite")
            for r in islice(ddgs_gen, 10):
                search_results.append(r)
        reference_results = []
        for idx, result in enumerate(search_results):
            logger.debug(f"搜索结果{idx + 1}：{result}")
            reference_results.append([result["body"], result["href"]])
        reference_results = add_source_numbers(reference_results)

        today = datetime.datetime.today().strftime("%Y-%m-%d")
        real_input = (
            WEBSEARCH_PTOMPT_TEMPLATE.replace("{current_date}", today)
            .replace("{query}", input)
            .replace("{web_results}", "\n\n".join(reference_results))
        )

        return real_input
