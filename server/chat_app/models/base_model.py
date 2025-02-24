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
from ..service.history import count_user_history_token as COUNT_USER_HISTORY_TOKEN
from ..service.knowledge_stores import parse_file as PARSE_FILE

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
        # 视觉模型
        self.model_multimodal = config["multimodal"]
        self.user_name = user_name
        self.agent_id = agent_id
        self.history_id = history_id
        self.config = config
        self.history_data = []
        self.agent_history_data = []
        self.history_content = []
        self.agent_data = None
        if user_name is None:
            raise AgentException("当前用户不能为空")
        if history_id is not None:
            history_data = load_history(id=history_id)
            if history_data is None:
                raise AgentException(f"聊天记录不存在,id={history_id}")
            self.history_data = history_data
            agent_data = history_data.get("agent_data", {})
            self.agent_data = agent_data
            self.agent_history_data = [*agent_data.get("content", [])]
            self.history_content = history_data.get("content", [])

    def stream_next_chatbot(
        self, inputs, history_id, file_path=None, file_name=None, parse_file_id=None
    ) -> str:
        """发送一个回答"""
        logger.info(f"用户输入为：{inputs}")

        user_content = self.parse_document(
            inputs=inputs,
            history_id=history_id,
            is_once=False,
            file_path=file_path,
            file_name=file_name,
            parse_file_id=parse_file_id,
        )
        self.set_history(user_content)
        self.inputs = user_content

        stream_iter = self.get_answer_stream_iter(history_id, user_content)

        return stream_iter

    def parse_document(
        self,
        inputs,
        history_id,
        is_once=False,
        file_path=None,
        file_name=None,
        parse_file_id=None,
    ) -> dict:
        """解析文档/图片
        @param inputs: 用户输入
        @param history_id: 历史记录id
        @param is_once: 是否单次
        @param file_path: 文件路径
        @param file_name: 文件名称
        @param parse_file_id: 解析文件id
        @return 返回当前组装对话
        """
        if file_path is not None and file_path != "":
            # 判断是不是图片
            imag_flag = is_file_image(file_path)
            orc_flag = True
            if imag_flag == True:
                if self.model_multimodal == True:
                    # 是视觉模型模型,支持图片
                    if imag_flag == True:
                        orc_flag = False
                        user_content = construct_user_image(file_path, inputs)
            # 使用orc解析
            if orc_flag == True:
                if parse_file_id is None:
                    raise AgentException("解析文件不存在,请重新上传文件")
                # 读取解析文件
                user_dir = os.path.join(CHAT_PARSE_FILE_DIR, self.user_name)
                target_path = os.path.join(user_dir, parse_file_id)
                try:
                    with open(target_path, "r", encoding="utf-8") as f:
                        text = f.read()
                except Exception as e:
                    logger.error(f"读取解析文件失败,{e}")
                    raise AgentException(f"读取解析文件失败,{e}")

                # 添加文件名称到历史中，并保存
                if is_once == False:
                    file_text = f"<file_content>根据您上传的文件 {file_name}，解析得到的文本内容如下：\n{text}</file_content>"

                    update_history(
                        self.user_name,
                        history_id,
                        [
                            construct_file(file_name, file_path),
                            construct_assistant(file_text),
                        ],
                    )
                    self.set_history(construct_file(file_name, file_path))
                    self.set_history(construct_assistant(file_text))
                    user_content = construct_user(inputs)
                else:
                    # 单次
                    user_content = construct_user(f"附加的文本内容:{text}\n{inputs}")

        else:
            user_content = construct_user(inputs)

        return user_content

    def update_history_record(self, history_id, user_content, full_content):
        """修改历史记录"""
        assistant_content = construct_assistant(full_content)
        self.set_history(assistant_content)
        # 修改历史记录
        update_history(self.user_name, history_id, [user_content, assistant_content])

    def get_answer_stream_iter(self, history_id, user_content):
        return "未实现功能"

    def get_answer_at_once(self):
        """没有上下文"""
        return "未实现功能"

    def get_answer_chatbot_at_once(
        self, inputs, file_path=None, file_name=None, parse_file_id=None
    ):
        """没有上下文，只回答一次"""
        """发送一个回答"""
        logger.info(f"用户输入为：{inputs}")
        user_content = self.parse_document(
            inputs=inputs,
            history_id=None,
            is_once=True,
            file_path=file_path,
            file_name=file_name,
            parse_file_id=parse_file_id,
        )
        # 将当前内容保存
        self.input_txt = user_content
        stream_iter = self.get_answer_at_once()
        logger.info(f"模型输出为：{stream_iter}")

        return stream_iter

    def set_history(self, history):
        history_data = self.get_history()
        if not history_data:
            history_data = []
        if isinstance(history, list):
            history_data.extend(history)
        elif isinstance(history, dict):
            history_data.append(history)
        self.history_content = history_data
        self.history_data["content"] = history_data

    def get_history(self):
        return self.history_content

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

    def get_history_limits(self) -> list:
        """获取限制的上下文"""
        inputs = self.inputs
        if not inputs:
            return []
        history_data = self.history_data
        if history_data is not None:
            agent_data = history_data.get("agent_data", {})
            all_token_counts = history_data["all_token_counts"]
            content_data = self.exclude_file_type(history_data.get("content", []))
            if agent_data:
                max_tokens = agent_data.get("max_tokens", 0)
                agent_count = agent_data.get("count", 0)
                max_limit = int(max_tokens)
                cur_chat_token = COUNT_USER_HISTORY_TOKEN([inputs])
                if all_token_counts >= max_tokens:
                    logger.warning("聊天记录对话超过最大限制，自动截断开始。。。。")
                    agent_content_data = content_data[:agent_count]
                    chat_content_data = content_data[agent_count + 1 :]
                    # 智能体的token和当前对话token
                    cur_token = (
                        COUNT_USER_HISTORY_TOKEN(agent_content_data) + cur_chat_token
                    )

                    real_chat_data = []
                    total_token = cur_token
                    for history in chat_content_data[::-1]:
                        token = COUNT_USER_HISTORY_TOKEN([history])
                        total_token = total_token + token
                        if total_token < max_limit:
                            # 倒叙添加
                            real_chat_data.insert(0, history)
                        else:
                            break
                    agent_content_data.extend(real_chat_data)

                    return agent_content_data

            if len(content_data) == 0:
                content_data = [inputs]
            return content_data

        return [inputs]

    # 排除类型为file的函数
    def exclude_file_type(self, content_data: list) -> list:
        # 排除type为file的数据
        return [item for item in content_data if item.get("role") is not None]
