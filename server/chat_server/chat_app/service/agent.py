
import json
import os
from ..presets import *
import uuid
import threading

# 用户存放的模型实例 <p>{1222:{model_name:LALM_11,model_instance:23445}}</p>
_user_agent_instance={}
_user_agent_lock = threading.Lock()


def save_agent(user_name,json_str) ->None:
    """保存智能体文件"""
    try:
        agent_data = json.loads(json_str)
        if agent_data is not None:
            # 智能体名称
            title = agent_data.get("title")
            if title is None:
                raise '智能体名称不能为空'
            # 创建uuid
            id = str(uuid.uuid4()).replace('-', '')
            agent_data['id'] = id
            # 创建目录
            os.makedirs(os.path.join(AGENT_DIR,user_name), exist_ok=True)
            history_file_path = os.path.join(AGENT_DIR,user_name,f'{id}.json')
            with open(history_file_path, "w",encoding='utf-8') as f:
                json.dump(agent_data, f, ensure_ascii=False)
                
            set_user_agent(user_name,id,title)    
    except Exception as e:
        # 抛出异常
        raise Exception(f"Error saving agent file: {e}")
         

def load_agent(user_name,id) ->str:
    """加载智能体文件"""
    try:
        history_file_path = os.path.join(AGENT_DIR,user_name,f'{id}.json')
        with open(history_file_path, "r",encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        # 抛出异常
       raise Exception(f"Error loading agent file: {e}") 
   
 
def get_user_all_agents(user_name,keyword):
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
        if agent_list is None or len(agent_list)==0:
            agent_list = []
            for file in os.listdir(os.path.join(AGENT_DIR,user_name)):
                if file.endswith(".json"):
                    with open(os.path.join(AGENT_DIR,user_name,file), "r",encoding='utf-8')as f:
                        agent_data = json.load(f)
                        agent={
                                'title':agent_data['title'],
                                'id':agent_data['id']
                            }
                        agent_list.append(agent)
                        
        if keyword is not None:
            agent_list = [agent for agent in agent_list if keyword in agent['title']] 
        return agent_list              
    except Exception as e:
        # 抛出异常
        raise Exception(f"Error searching agent file: {e}")                

   
def set_user_agent(user_name, id, title) -> None:
    """设置全局模型"""
    agent = {
        'title': title,
        'id': id
    }
    with _user_agent_lock:
        if user_name not in _user_agent_instance:
            _user_agent_instance[user_name] = []
        agents = _user_agent_instance[user_name]
    agents.append(agent)
      

def get_user_agent(user_name) ->list:
    """获取全局模型"""
    global _user_agent_instance
    if user_name not in _user_agent_instance:
            return None
    return _user_agent_instance[user_name]    