import redis
import logging
import time
from typing import List
from langchain_redis import RedisVectorStore
from langchain_core.embeddings import Embeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain_redis import RedisConfig, RedisVectorStore
from functools import lru_cache
from ..base_module.agent_exception import AgentException
from ..config import (
    redis_url as REDIS_URL_CONFIG,
    embedding_address as EMBEDDING_ADDRESS,
)

logger = logging.getLogger("chat_app")


# 创建 Redis 客户端实例并确保连接成功
# REDIS_URL = "redis://localhost:6379"
# redis_client_instance = None


@lru_cache(maxsize=1)
def redis_client():
    REDIS_URL = str(REDIS_URL_CONFIG())
    if not REDIS_URL:
        raise AgentException("未配置向量数据库地址,请配置向量数据库地址")
    try:
        client = redis.from_url(REDIS_URL)
        logger.info(f"connect Redis address: {REDIS_URL}")
        if client.ping():
            logger.info(
                f"Redis connect success at {time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
        else:
            logger.error(f"Redis connect fail at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            raise AgentException("Redis连接失败")
    except (redis.ConnectionError, redis.TimeoutError) as e:
        logger.error(
            f"Redis connection error: {e} at {time.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        raise AgentException("Redis连接失败")
    except redis.RedisError as e:
        logger.error(f"Redis error: {e} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        raise AgentException("Redis连接失败")
    except Exception as e:
        logger.error(f"Unexpected error: {e} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        raise AgentException("Redis连接失败")
    return client


def get_embedding():
    """获取向量模型"""
    # model_name = "E:/plugIn/models/huggingface/sentence-transformers/BAAI/bge-large-zh"
    EMBEDDING_URL = EMBEDDING_ADDRESS()
    model_name = EMBEDDING_URL
    if not model_name:
        logger.warning("未配置向量模型，请配置向量模型")
    encode_kwargs = {"normalize_embeddings": True}
    return HuggingFaceEmbeddings(model_name=model_name, encode_kwargs=encode_kwargs)


def get_redis_store(index_name: str) -> RedisVectorStore:
    # 创建Redis配置对象，包含索引名称和Redis客户端
    config = RedisConfig(index_name=index_name, redis_client=redis_client())

    # 创建Redis向量存储对象，并传入嵌入模型和配置
    vector_store = RedisVectorStore(get_embedding(), config=config)
    return vector_store


def add_redis_store(
    index_name: str,
    documents: List[Document],
) -> List[str]:
    """
    将文档添加到Redis存储中，并生成索引。

    参数:
    index_name: str - 索引的名称。
    documents: List[Document] - 待添加到Redis的文档列表。
    """
    try:
        if not documents:
            logger.warning("文档列表为空，无需添加")
            return []

        # 创建Redis向量存储对象，并传入嵌入模型和配置
        vector_store = get_redis_store(index_name)

        # 将文档添加到向量存储中，并获取文档ID
        ids = vector_store.add_documents(documents)
        logger.info(f"生成索引成功: {ids}")

        return ids

    except Exception as e:
        logger.error(f"添加文档到Redis存储失败: {e}")
        raise AgentException(f"添加文档到Redis存储失败")


def del_keys(index_name, keys: list[str]) -> bool:
    """
    批量删除Redis中与给定键名列表匹配的键。

    这个函数接收一个字符串键名列表作为参数，通过调用Redis客户端的delete方法来删除匹配的键。
    此函数的主要用途是批量清理Redis中不再需要的数据，以维护数据的一致性和节省存储空间。

    参数:
    keys (list[str]): 包含多个键名的列表，每个键名是一个字符串。

    返回:
    bool: 如果所有删除操作都尝试执行则返回True，否则返回False。
    """
    try:
        # 使用 Redis 的 delete 方法支持多个键的特性
        if not keys:
            return True  # 空列表直接返回 True

        # 执行批量删除
        # 创建Redis向量存储对象，并传入嵌入模型和配置
        vector_store = get_redis_store(index_name)

        # 检查删除结果
        deleted_count = vector_store.index.drop_keys(keys)
        if deleted_count != len(keys):
            logger.warning(
                f"Warning: Not all keys were successfully deleted. Expected {len(keys)}, but deleted {deleted_count}."
            )

        return True

    except redis.RedisError as e:
        logger.error(f"Redis error occurred: {e}")
        raise AgentException("删除Redis数据失败")


def search_text(index_name: str, query: str, top_k: int = 10):
    """
    在指定的索引中搜索文本，并返回最相关的前top_k个结果。

    参数:
    - index_name: str, 索引的名称，用于指定在哪个索引中进行搜索。
    - query: str, 查询字符串，用户输入的搜索内容。
    - top_k: int, 返回的搜索结果数量，默认为10。

    返回:
    - list, 包含搜索结果的列表，每个搜索结果都是一个字典，包含分数、内容和元数据。

    异常:
    - AgentException: 当输入参数不符合要求或Redis搜索失败时抛出。
    """
    try:
        # 检查top_k参数是否为大于0的整数
        if not isinstance(top_k, int) or top_k <= 0:
            raise AgentException("参数 top_k 必须是大于0的整数")

        # 检查query参数是否为非空字符串
        if not isinstance(query, str) or not query.strip():
            raise AgentException("查询字符串不能为空")

        # 创建Redis向量存储对象，并传入嵌入模型和配置
        vector_store = get_redis_store(index_name)

        # 执行相似度搜索，并返回最相关的前top_k个结果
        # 简单查询
        # results = vector_store.similarity_search(query, k=top_k)
        # 最大边界相关性
        results = vector_store.max_marginal_relevance_search(query, k=top_k, fetch_k=20)
        logger.debug(f"知识库检索搜索成功: {results}")
        # 如果没有搜索结果，返回空列表
        if not results:
            return []

        # 初始化搜索结果列表
        list_result = []
        # 遍历搜索结果，构造搜索结果列表,score分数越低，相关度越高
        for doc in results:
            list_result.append({"content": doc.page_content, "metadata": doc.metadata})

        # 返回搜索结果列表
        return list_result

    except Exception as e:
        # 记录Redis错误
        logger.error(f"Redis error occurred: {e}")
        # 抛出搜索失败异常
        raise AgentException("Redis搜索失败")
