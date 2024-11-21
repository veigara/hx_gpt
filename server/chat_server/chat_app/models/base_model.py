from ..presets import *
from enum import Enum
import logging
from ..utils import *
from ..config import set_default_model_params,get_default_model_params

logger = logging.getLogger('chat_app')


class BaseLLMModel:
    def __init__(
        self,
        model_name,
        user="",
        config=None,
    ) -> None:
        # # 设置默认的模型参数
        set_default_model_params()
        # 使用全局变量 MODEL_METADATA 获取模型参数
        MODEL_METADATA =get_default_model_params()
        
        if config is not None:
            temp = MODEL_METADATA[model_name].copy()
            keys_with_diff_values = {key: temp[key] for key in temp if key in DEFAULT_METADATA and temp[key] != DEFAULT_METADATA[key]}
            config.update(keys_with_diff_values)
            temp.update(config)
            config = temp
        else:
            config = MODEL_METADATA[model_name]

        self.model_name = config["model_name"]
        self.multimodal = config["multimodal"]
        self.description = config["description"]
        #self.placeholder = config["placeholder"]
        self.token_upper_limit = config["token_limit"]
        self.system_prompt = config["system"]
        self.api_key = config["api_key"]
        self.api_host = config["api_host"]
        self.stream = config["stream"]

        self.interrupted = False
        self.need_api_key = self.api_key is not None
        self.history = []
        self.all_token_counts = []
        self.model_type = ModelType.get_type(model_name)
        #self.history_file_path = get_first_history_name(user)
        self.user_name = user
        self.chatbot = []

        self.default_single_turn = config["single_turn"]
        self.default_temperature = config["temperature"]
        self.default_top_p = config["top_p"]
        self.default_n_choices = config["n_choices"]
        self.default_stop_sequence = config["stop"]
        self.default_max_generation_token = config["max_generation"]
        self.default_presence_penalty = config["presence_penalty"]
        self.default_frequency_penalty = config["frequency_penalty"]
        self.default_logit_bias = config["logit_bias"]
        self.default_user_identifier = user
        self.default_stream = config["stream"]

        self.single_turn = self.default_single_turn
        self.temperature = self.default_temperature
        self.top_p = self.default_top_p
        self.n_choices = self.default_n_choices
        self.stop_sequence = self.default_stop_sequence
        self.max_generation_token = self.default_max_generation_token
        self.presence_penalty = self.default_presence_penalty
        self.frequency_penalty = self.default_frequency_penalty
        self.logit_bias = self.default_logit_bias
        self.user_identifier = user

        self.metadata = config["metadata"]

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

    def get_answer_at_once(self):
        """predict at once, need to be implemented
        conversations are stored in self.history, with the most recent question, in OpenAI format
        Should return:
        the answer (str)
        total token count (int)
        """
        logger.warning("at once predict not implemented, using stream predict instead")
        response_iter = self.get_answer_stream_iter()
        count = 0
        for response in response_iter:
            count += 1
        return response, sum(self.all_token_counts) + count

    def count_token(self, user_input):
        """get token count from input, implement if needed"""
        # logger.warning("token count not implemented, using default")
        return len(user_input)
      

    def stream_next_chatbot(self, inputs) ->str:
        """发送一个回答"""
        logging.info(
                "用户"
                + f"{self.user_name}"
                + "的输入为：{inputs}"
            )
        user_token_count = self.count_token(inputs)
        self.all_token_counts.append(user_token_count)
        logger.debug(f"输入token计数: {user_token_count}")
        self.history.append(construct_user(inputs))
        stream_iter = self.get_answer_stream_iter()
        logging.info(
                "回答为："
                + f"{stream_iter}"
            )
        self.history.append(construct_assistant(stream_iter))
        
        return stream_iter

    def next_chatbot_at_once(self, inputs, chatbot, fake_input=None, display_append=""):
        if fake_input:
            chatbot.append((fake_input, ""))
        else:
            chatbot.append((inputs, ""))
        if fake_input is not None:
            user_token_count = self.count_token(fake_input)
        else:
            user_token_count = self.count_token(inputs)
        self.all_token_counts.append(user_token_count)
        ai_reply, total_token_count = self.get_answer_at_once()
        self.history.append(construct_assistant(ai_reply))
        if fake_input is not None:
            self.history[-2] = construct_user(fake_input)
        chatbot[-1] = (chatbot[-1][0], ai_reply + display_append)
        if fake_input is not None:
            self.all_token_counts[-1] += count_token(construct_assistant(ai_reply))
        else:
            self.all_token_counts[-1] = total_token_count - sum(self.all_token_counts)
        status_text = self.token_message()
        return chatbot, status_text
    

class ModelType(Enum):
    Unknown = -1
    Groq = 1
    LMStudio= 2

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