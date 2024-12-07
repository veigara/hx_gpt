import json
import os
from ..presets import *
import uuid
import threading

# 用户存放的模型实例 <p>{1222:{model_name:LALM_11,model_instance:23445}}</p>
_user_agent_instance = {}
_user_agent_lock = threading.Lock()


def save_agent(user_name, json_str) -> None:
    """保存智能体文件
    {"id": "1b58a6b59a4a4bcba07078d415d74f0b", "title": "文言文翻译", "content": [{"role": "assistant", "content": "用文言文表达输入的内容"}, {"role": "user", "content": "示例：我很开心，因为今天出去玩了"}], "model_name": "llama-3.2-90b-vision", "temperature": 0.8, "top_p": 0.3, "max_tokens": 84492, "presence_penalty": 1.5, "frequency_penalty": 1.7}
    """
    try:
        agent_data = json.loads(json_str)
        if agent_data is not None:
            # 智能体名称
            title = agent_data.get("title")
            id = agent_data.get("id")
            if title is None:
                raise "智能体名称不能为空"
            if id is None or id == "":
                # 创建uuid
                id = str(uuid.uuid4()).replace("-", "")
                agent_data["id"] = id
                agent_data["user_name"] = user_name
                agent_data["count"] = len(agent_data.get("content", []))

            # 创建目录
            os.makedirs(os.path.join(AGENT_DIR, user_name), exist_ok=True)
            history_file_path = os.path.join(AGENT_DIR, user_name, f"{id}.json")
            with open(history_file_path, "w", encoding="utf-8") as f:
                json.dump(agent_data, f, ensure_ascii=False)

            # 将智能体的相关参数保存在全局变量
            set_user_agent(user_name, agent_data)
    except Exception as e:
        # 抛出异常
        raise Exception(f"Error saving agent file: {e}")


def load_agent(user_name, id) -> str:
    """从文件目录中获取智能体文件的内容"""
    try:
        agent_data = None
        try:
            with open(get_file_path(user_name, id), "r", encoding="utf-8") as f:
                agent_data = json.load(f)
        except Exception as e:
            # 从内置中加载
            with open(
                get_default_agent_path(user_name, id), "r", encoding="utf-8"
            ) as f:
                agent_data = json.load(f)
        return agent_data
    except Exception as e:
        # 抛出异常
        raise Exception(f"Error loading agent file: {e}")


def get_file_path(user_name, id):
    """获取智能体的文件路径"""
    return os.path.join(AGENT_DIR, user_name, f"{id}.json")


def get_default_agent_path(user_name, id):
    """获取内置的智能体的文件路径"""
    return os.path.join(DEFALUE_AGENT_DIR, f"{id}.json")


def get_user_all_agents(user_name, keyword):
    """
    获取当前用户所有智能体文件

    根据用户名称和关键词获取用户的所有智能体文件列表如果关键词不为空，则使用关键词过滤智能体列表

    参数:
    user_name (str): 用户名称
    keyword (str): 用于搜索智能体标题的关键词

    返回:
    list: 包含智能体信息的字典列表，每个字典包含智能体的标题和ID
    """
    try:
        agent_list = get_user_agent(user_name)
        if agent_list is None or len(agent_list) == 0:
            # 获取系统默认的智能体
            agent_list = get_sys_agent()
            # 获取用户的智能体
            os.makedirs(os.path.join(AGENT_DIR, user_name), exist_ok=True)
            for file in os.listdir(os.path.join(AGENT_DIR, user_name)):
                if file.endswith(".json"):
                    with open(
                        os.path.join(AGENT_DIR, user_name, file), "r", encoding="utf-8"
                    ) as f:
                        agent_data = json.load(f)
                        agent_data["content"] = []
                        agent_data["edit"] = user_name == agent_data.get("user_name")
                        agent_list.append(agent_data)
            set_user_agent_all(user_name, agent_list)

        if keyword is not None:
            agent_list = [agent for agent in agent_list if keyword in agent["title"]]

        return agent_list
    except Exception as e:
        # 抛出异常
        raise Exception(f"Error searching agent file: {e}")


def set_user_agent(user_name, jsonData) -> None:
    """设置全局模型
    user_name (str): 当前用户名称
    jsonData (json): 智能体数据
    """
    # 查询id相关详情
    if jsonData is None:
        return
    jsonData["content"] = []
    jsonData["edit"] = (user_name == jsonData.get("user_name"),)
    with _user_agent_lock:
        if user_name not in _user_agent_instance:
            _user_agent_instance[user_name] = []
        agents = _user_agent_instance[user_name]

        # 遍历 agents 列表，查找并修改具有相同 id 的元素
        found = False
        for i, existing_agent in enumerate(agents):
            if existing_agent and existing_agent["id"] == jsonData["id"]:
                agents[i] = jsonData
                found = True
                break

        # 如果没有找到具有相同 id 的元素，则追加新元素
        if not found:
            agents.append(jsonData)


def set_user_agent_all(user_name, jsonData) -> None:
    """将用户智能体加载进内存中"""
    # 查询id相关详情
    _user_agent_instance[user_name] = jsonData


def get_user_agent(user_name) -> list:
    """获取全局模型"""
    global _user_agent_instance
    if user_name not in _user_agent_instance:
        return None
    return _user_agent_instance[user_name]


def get_sys_agent():
    """获取系统默认的所有智能体"""
    agent_list = []
    for file in os.listdir(os.path.join(DEFALUE_AGENT_DIR)):
        if file.endswith(".json"):
            with open(
                os.path.join(DEFALUE_AGENT_DIR, file), "r", encoding="utf-8"
            ) as f:
                agent_data = json.load(f)
                agent_data["content"] = []
                # 系统内置，不允许编辑
                agent_data["edit"] = False
                agent_list.append(agent_data)
    return agent_list


def del_agent(user_name, id) -> None:
    """删除智能体文件"""
    agent_list = get_user_agent(user_name)
    if agent_list is None:
        return
    for i, agent in enumerate(agent_list):
        if agent["id"] == id:
            # 删除文件
            file_user_name = agent.get("user_name")

            history_file_path = get_file_path(file_user_name, id)
            os.remove(history_file_path)
            agent_list.pop(i)
            break


def get_default_agent_data(user_name):
    """获取默认的智能体数据"""
    agent_list = get_user_all_agents(user_name, None)
    if agent_list is None or len(agent_list) == 0:
        return None
    """默认第一个"""
    return agent_list[0]
