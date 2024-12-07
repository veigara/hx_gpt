from django.core.cache import cache

# 设置全局变量
# 全局变量历史记录对话
_history_key = "history_global_"
# 智能体配置
_agent_key = "agent_global_"
# 全局变量历史记录文档
_history_doc_key = "history_doc_global_"


def set_history_global(user_name, data):
    if data is None or (isinstance(data, list) and len(data) == 0):
        return
    history_data = cache.get(get_user_history_key(user_name))
    if history_data is None:
        history_data = []
    if isinstance(data, list):
        history_data.extend(data)
    elif isinstance(data, dict):
        history_data.append(data)
    # timeout=None 表示永不过期
    cache.set(get_user_history_key(user_name), history_data, timeout=None)


def get_history_global(user_name):
    data = cache.get(get_user_history_key(user_name))
    return data if data is not None else []


def clear_history_global(user_name):
    cache.delete(get_user_history_key(user_name))


def get_user_history_key(user_name):
    return f"{_history_key}{user_name}"


def set_history_doc_global(user_name, data):
    if data is None or (isinstance(data, list) and len(data) == 0):
        return
    history_doc_data = cache.get(get_history_doc_global(user_name))
    if history_doc_data is None:
        history_doc_data = []
    if isinstance(data, list):
        history_doc_data.extend(data)
    elif isinstance(data, dict):
        # 判断是否已经存在,先删除
        clear_history_doc_id_global(user_name, data["id"])
        history_doc_data.append(data)
    # timeout=None 表示永不过期
    cache.set(get_history_doc_global(user_name), history_doc_data, timeout=None)


def get_history_doc_global(user_name):
    data = cache.get(get_user_history_doc_key(user_name))
    return data if data is not None else []


def clear_history_doc_global(user_name):
    cache.delete(get_user_history_doc_key(user_name))


def clear_history_doc_id_global(user_name, id):
    data = cache.get(get_user_history_doc_key(user_name))
    if data is not None:
        # 删除id相同的
        for i in range(len(data)):
            if data[i]["id"] == id:
                data.pop(i)
                break
    # 设置缓存
    cache.set(get_user_history_doc_key(user_name), data, timeout=None)


def get_user_history_doc_key(user_name):
    return f"{_history_doc_key}{user_name}"


def get_user_agent_key(user_name):
    return f"{_agent_key}{user_name}"


def set_agent_data_global(user_name, data):
    if data is None:
        return

    cache.set(get_user_agent_key(user_name), data, timeout=None)


def get_agent_data_global(user_name):
    data = cache.get(get_user_agent_key(user_name))
    return data if data is not None else {}
