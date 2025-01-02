import os
import json
import uuid
import datetime
import logging
from ..presets import *
from ..utils import *
from .agent import *
from ..cache_utils import *
from ..config import *

logger = logging.getLogger("chat_app")


def get_user_all_history(user_name, keyword):
    """
    获取当前用户所有聊天记录文件

    根据用户名称和关键词获取用户的所有聊天记录文件列表如果关键词不为空，则使用关键词过滤聊天记录列表

    参数:
    user_name (str): 用户名称
    keyword (str): 用于搜索聊天记录标题的关键词

    返回:
    list: 包含聊天记录信息的字典列表，每个字典包含聊天记录的标题和ID
    """
    try:
        history_list = get_user_history(user_name)
        if history_list is None or len(history_list) == 0:
            history_list = []
            # 创建聊天记录
            os.makedirs(os.path.join(HISTORY_DIR, user_name), exist_ok=True)
            # 获取系统默认的聊天记录
            for file in os.listdir(os.path.join(HISTORY_DIR, user_name)):
                if file.endswith(".json"):
                    with open(
                        os.path.join(HISTORY_DIR, user_name, file),
                        "r",
                        encoding="utf-8",
                    ) as f:
                        history_data = json.load(f)

                        history_list.append(cover_history(history_data))

            set_user_history_all(user_name, history_list)

        if keyword is not None:
            history_list = [
                history for history in history_list if keyword in history["title"]
            ]

        return sort_history_list(history_list)
    except Exception as e:
        # 抛出异常
        logger.error(print_err(e))
        raise Exception(f"{STANDARD_ERROR_MSG}:获取当前用户所有聊天记录失败")


def sort_history_list(history_list):
    """根据时间排序聊天记录列表"""
    if history_list is None or len(history_list) == 0:
        return None
    return sorted(history_list, key=lambda x: x["create_time"], reverse=True)


def get_user_history(user_name) -> list:
    """获取用户聊天记录"""
    return get_history_doc_global(user_name)


def set_user_history_all(user_name, jsonDatas) -> None:
    """将用户聊天记录加载进内存中"""
    # 查询id相关详情
    set_history_doc_global(user_name, jsonDatas)


def load_history(user_name, id) -> str:
    """从文件目录中获取历史文件的内容"""
    try:
        history_file_path = os.path.join(HISTORY_DIR, user_name, f"{id}.json")
        with open(history_file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        # 抛出异常
        logger.error(print_err(e))
        raise Exception(f"{STANDARD_ERROR_MSG}:加载历史文件失败")


def rename_history(user_name, id, new_title) -> None:
    """重命名聊天记录"""
    history_list = get_user_history(user_name)
    if history_list is None or len(history_list) == 0:
        return

    for history in history_list:
        if history["id"] == id:
            data = load_history(user_name, id)
            data["title"] = new_title
            # 保存到文件
            save_history(user_name, json.dumps(data))


def del_history(user_name, id) -> None:
    """删除聊天记录文件"""
    # 删除文件
    history_file_path = os.path.join(HISTORY_DIR, user_name, f"{id}.json")
    os.remove(history_file_path)
    # 删除成功后，删除缓存
    clear_history_doc_id_global(user_name, id)


def cretate_new_history(user_name, model_name, input_str) -> str:
    """创建新的聊天记录,没有智能体
    params:input_str 用户输入
    return:history_id 聊天记录id
    """
    agent_data = get_default_agent_data(user_name)
    if agent_data is None:
        raise Exception("系统没有智能体,请先设置智能体")
    agent_data["history_title"] = input_str[:20]
    agent_data["model_name"] = model_name

    return save_history_agent(user_name, agent_data)


def save_history(user_name, json_str) -> None:
    """保存聊天记录文件
    {"id": "1b58a6b59a4a4bcba07078d415d74f0b", "title": "文言文翻译", "content": [{"role": "assistant", "content": "用文言文表达输入的内容"}, {"role": "user", "content": "示例：我很开心，因为今天出去玩了"}], "model_name": "llama-3.2-90b-vision", "temperature": 0.8, "top_p": 0.3, "max_tokens": 84492, "presence_penalty": 1.5, "frequency_penalty": 1.7}
    """
    try:
        history_data = json.loads(json_str)
        if history_data is not None:
            # 聊天记录名称
            title = history_data.get("title")
            id = history_data.get("id")
            if title is None:
                raise "聊天记录名称不能为空"
            if id is None or id == "":
                # 创建uuid
                id = str(uuid.uuid4()).replace("-", "")
                history_data["id"] = id

            save_history_file(user_name, history_data)

            # 将聊天记录的相关参数保存在全局变量
            set_user_history(user_name, history_data)
    except Exception as e:
        # 抛出异常
        logger.error(print_err(e))
        raise Exception(f"{STANDARD_ERROR_MSG}:保存历史文件失败")


def save_history_file(user_name, history_data) -> str:
    """保存聊天记录到硬盘中"""
    # 创建目录
    id = history_data.get("id", str(uuid.uuid4()).replace("-", ""))
    os.makedirs(os.path.join(HISTORY_DIR, user_name), exist_ok=True)
    history_file_path = os.path.join(HISTORY_DIR, user_name, f"{id}.json")
    with open(history_file_path, "w", encoding="utf-8") as f:
        json.dump(history_data, f, ensure_ascii=False)


def save_history_agent(user_name, agentData) -> str:
    """从智能体中创建聊天记录"""
    try:
        id = str(uuid.uuid4()).replace("-", "")
        agent_title = agentData.get("title", "新的聊天")
        history_title = agentData.get("history_title")
        title = (
            agent_title
            if history_title is None or history_title == ""
            else history_title
        )
        history = agentData.get("content", [])
        # model_name = agentData.get("model_name")
        model_key = agentData.get("model_key")
        temperature = agentData["temperature"]
        top_p = agentData["top_p"]
        max_tokens = agentData["max_tokens"]
        presence_penalty = agentData["presence_penalty"]
        frequency_penalty = agentData["frequency_penalty"]
        agent_id = agentData.get("id")
        user_icon = agentData.get("user_icon")
        assistant_icon = agentData.get("assistant_icon")
        # 对话条数
        count = len(history)
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        all_token_counts = count_user_history_token(history)
        history_data = {
            "id": id,
            "title": title,
            "content": history,
            "model_key": model_key,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            "count": count,
            "create_time": create_time,
            "all_token_counts": all_token_counts,
            "agent_id": agent_id,
            "agent_title": agent_title,
            "chatbot": [],
            "user_icon": user_icon,
            "assistant_icon": assistant_icon,
        }
        save_history_file(user_name, history_data)
        # 将聊天记录的相关参数保存在全局变量
        set_user_history(user_name, history_data)

        return id
    except Exception as e:
        # 抛出异常
        logger.error(print_err(e))
        raise Exception(f"{STANDARD_ERROR_MSG}:从智能体中创建聊天记录失败")


def count_user_history_token(contents) -> int:
    """统计聊天记录的token数
    params: contents: [{"role": "user", "content": "示例：我很开心，因为今天出去玩了"}, {"role": "assistant", "content": "用文言文表达输入的内容"}]
    """
    if contents is None:
        return 0
    user_contents = [content["content"] for content in contents]
    return sum(count_token(content) for content in user_contents)


def cover_history(jsonData) -> json:
    """将聊天记录转换为需要的格式"""
    return {
        "id": jsonData.get("id"),
        "title": jsonData.get("title"),
        "active": False,
        "count": jsonData.get("count"),
        "create_time": jsonData.get("create_time"),
        "all_token_counts": jsonData.get("all_token_counts"),
    }


def set_user_history(user_name, jsonData) -> None:
    """将当前聊天记录设置在缓存
    user_name (str): 当前用户名称
    jsonData (json): 聊天记录数据
    """
    # 查询id相关详情
    if jsonData is None:
        return
    set_history_doc_global(user_name, jsonData)


def update_history(
    user_name, history_id, contents, agent_data, max_content_len
) -> None:
    """修改聊天记录，对话防止超限
    history_id(str):id 聊天记录id
    content([]):当前对话
    agent_data(dict):智能体id
    max_content_len(int) 最大上下文
    """
    try:
        history_data = load_history(user_name, history_id)
        if history_data is None:
            raise Exception(f"聊天记录不存在,id={history_id}")
        if agent_data is None:
            raise Exception(f"智能体数据不存在,聊天记录id={history_id}")
        count = history_data.get("count", 0)
        agent_count = agent_data.get("count", 0)
        all_token_counts = history_data.get("all_token_counts", 0)
        content_data = history_data.get("content", [])
        history_data["count"] = count + len(contents)
        cur_chat_token = count_user_history_token(contents)
        history_data["all_token_counts"] = all_token_counts + cur_chat_token
        content_data.extend(contents)
        max_tokens = agent_data.get("max_tokens", 0)
        max_limit = max_content_len if max_content_len > 0 else max_tokens
        if (
            max_tokens is not None
            and history_data["all_token_counts"] > max_limit
            and max_limit > 0
            and max_limit > max_tokens
        ):
            logger.warning("聊天记录对话超过最大限制，自动截断开始。。。。")
            agent_content_data = content_data[:agent_count]
            chat_content_data = content_data[agent_count + 1 :]
            # 智能体的token和当前对话token
            cur_token = count_user_history_token(agent_content_data) + cur_chat_token

            real_chat_data = []
            for history in chat_content_data[::-1]:
                token = count_user_history_token([history])
                if cur_token + token < max_limit:
                    # 倒叙添加
                    real_chat_data.insert(0, history)
                else:
                    break
            content_data = agent_content_data.extend(real_chat_data)
            history_data["content"] = content_data
            history_data["count"] = len(content_data)
            history_data["all_token_counts"] = count_user_history_token(content_data)

        # 保存并修改缓存
        save_history(user_name, json.dumps(history_data))

    except Exception as e:
        logger.error(print_err(e))
        raise Exception(f"{STANDARD_ERROR_MSG}:修改聊天记录失败")


def top_history(user_name, history_id) -> None:
    """置顶聊天记录"""
    try:
        history_data = load_history(user_name, history_id)
        if history_data is None:
            raise Exception(f"聊天记录不存在,id={history_id}")
        history_data["create_time"] = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        save_history(user_name, json.dumps(history_data))
    except Exception as e:
        logger.error(print_err(e))
        raise Exception(f"{STANDARD_ERROR_MSG}:置顶聊天记录失败")


def clear_all_history(user_name) -> None:
    """删除所有聊天记录"""
    # 删除文件
    os.makedirs(os.path.join(HISTORY_DIR, user_name), exist_ok=True)
    for file in os.listdir(os.path.join(HISTORY_DIR, user_name)):
        os.remove(os.path.join(HISTORY_DIR, user_name, file))
    # 清除缓存
    clear_history_doc_global(user_name)


def clear_context(user_name, history_id) -> None:
    """清空上下文"""
    history_data = load_history(user_name, history_id)
    if history_data is None:
        raise Exception(f"聊天记录不存在,id={history_id}")
    agent_id = history_data.get("agent_id")
    if agent_id is None:
        raise Exception(f"聊天记录z中智能体不存在,id={history_id}")
    agent_data = load_agent(user_name, agent_id)
    if agent_data is None:
        raise Exception(f"智能体不存在,智能体id={agent_id}")
    content_data = agent_data.get("content", [])
    history_data["content"] = content_data
    history_data["count"] = len(content_data)
    history_data["all_token_counts"] = count_user_history_token(content_data)

    # 清除缓存
    save_history(user_name, json.dumps(history_data))
