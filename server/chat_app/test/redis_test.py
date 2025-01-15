"""测试向量库"""

from langchain_core.documents import Document
from typing import List
from langchain_huggingface import HuggingFaceEmbeddings


from chat_app.knowledge.docment_loaders.agent_docloader import (
    RapidOCRDocLoader,
)
from langchain.schema import Document
from langchain.text_splitter import TokenTextSplitter
from langchain_redis import RedisVectorStore


def get_load() -> List[Document]:
    """获取加载器"""
    file_path = "E:/idea_workspace/pythonProject/hx_gpt/server/knowledge/upload_file/3bad75c2-ea22-4fb3-bf83-da8322761aca.docx"
    loader = RapidOCRDocLoader(file_path=file_path)
    return loader


def get_embedding():
    """获取向量模型"""
    model_name = "E:/plugIn/models/huggingface/sentence-transformers/BAAI/bge-large-zh"
    encode_kwargs = {"normalize_embeddings": True}
    return HuggingFaceEmbeddings(model_name=model_name, encode_kwargs=encode_kwargs)


def test_chroma_db():
    print("开始测试向量库")
    """创建token分词器
    @param chunk_size: 切割文本的大小
    @param chunk_overlap: 切割文本的重叠度
    """
    text_splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=30)
    documents = []

    texts = get_load().load()

    if texts is not None:
        texts = text_splitter.split_documents(texts)
        documents.extend(texts)
    print("开始生成索引。。。。")
    # 向量入库
    from langchain_redis import RedisConfig, RedisVectorStore

    index_name = "rag_kom"
    config = RedisConfig(index_name=index_name, redis_url="redis://192.168.0.147:6379")
    vector_store = RedisVectorStore(get_embedding(), config=config)
    ids = vector_store.add_documents(documents)
    print("ids:", ids)
    print("生成索引成功。。。。")

    return


def search_text():
    """检索文本"""

    new_rdvs = RedisVectorStore(
        get_embedding(),
        redis_url="redis://192.168.0.147:6379",
        index_name="rag_kom",
    )
    print("开始检索。。。。")
    fake_inputs = "身份证号码"

    # 检索
    results = new_rdvs.similarity_search_with_score("兴业银行重庆南岸支行", k=10)

    for doc, score in results:
        print(f"Score: {score}")
        print(f"Content: {doc.page_content[:100]}...")
        print(f"Metadata: {doc.metadata}")


def delete_index(index_name):
    """删除索引"""
    new_rdvs = RedisVectorStore(
        get_embedding(),
        redis_url="redis://localhost:6379",
        index_name="rag-chroma1",
    )
    ids = [
        "rag-chroma1:d0bc88e794864be29559a6cc94e1b6af",
        "rag-chroma1:12800b1872ab4dbe9307cf70ccfb7880",
    ]
    flag = new_rdvs.delete(ids)
    print(f"删除结果：{flag}")


if __name__ == "__main__":
    """进入根目录 然后使用python -m chat_server.chat_app.test.redis_test测试"""
    test_chroma_db()
    # search_text()
