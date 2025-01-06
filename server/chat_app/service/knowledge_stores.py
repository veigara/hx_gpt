import logging
import importlib
import chardet
import os
from functools import lru_cache
from enum import Enum
from typing import Dict, List, Optional
import threading
import typing as t
from langchain_community.document_loaders import JSONLoader, TextLoader
from langchain.docstore.document import Document
from langchain.text_splitter import MarkdownHeaderTextSplitter, TextSplitter

from ..base_module.base_response import AgentResponse
from .knowledge_redis import add_redis_store

logger = logging.getLogger("chat_app")


# def add_stores(file_path, file_type, index_name, file_config: Dict, title) -> Dict:
#     """把文件添加到向量库"""
#     kb_file = KnowDocumentFile(
#         title=title,
#         file_path=file_path,
#         file_type=file_type,
#         file_config=file_config,
#     )
#     doc = kb_file.file2text()

#     ids = add_redis_store(index_name, doc)
#     # 转为字符串
#     ids = ",".join(ids)

#     return {"document_count": len(doc), "document_ids": ids}


def parse_file(file_path, file_type, file_config: Dict, title) -> List[Document]:
    """把文件解析成Document对象"""
    kb_file = KnowDocumentFile(
        title=title,
        file_path=file_path,
        file_type=file_type,
        file_config=file_config,
    )
    doc = kb_file.file2text()
    return doc


def add_db_store(
    index_name: str,
    documents: List[Document],
) -> List[str]:
    """把文件添加到Redis存储中，并生成索引。"""
    return add_redis_store(index_name, documents)


LOADER_DICT = {
    "UnstructuredHTMLLoader": [".html", ".htm"],
    "MHTMLLoader": [".mhtml"],
    "TextLoader": [".md"],
    "UnstructuredMarkdownLoader": [".md"],
    "JSONLoader": [".json"],
    "JSONLinesLoader": [".jsonl"],
    "CSVLoader": [".csv"],
    "RapidOCRPDFLoader": [".pdf"],
    "RapidOCRDocLoader": [".docx"],
    "RapidOCRPPTLoader": [
        ".ppt",
        ".pptx",
    ],
    "RapidOCRLoader": [".png", ".jpg", ".jpeg", ".bmp"],
    "UnstructuredFileLoader": [
        ".eml",
        ".msg",
        ".rst",
        ".rtf",
        ".txt",
        ".xml",
        ".epub",
        ".odt",
        ".tsv",
    ],
    "UnstructuredEmailLoader": [".eml", ".msg"],
    "UnstructuredEPubLoader": [".epub"],
    "UnstructuredExcelLoader": [".xlsx", ".xls", ".xlsd"],
    "NotebookLoader": [".ipynb"],
    "UnstructuredODTLoader": [".odt"],
    "PythonLoader": [".py"],
    "UnstructuredRSTLoader": [".rst"],
    "UnstructuredRTFLoader": [".rtf"],
    "SRTLoader": [".srt"],
    "TomlLoader": [".toml"],
    "UnstructuredTSVLoader": [".tsv"],
    "UnstructuredWordDocumentLoader": [".docx"],
    "UnstructuredXMLLoader": [".xml"],
    "UnstructuredPowerPointLoader": [".ppt", ".pptx"],
    "EverNoteLoader": [".enex"],
}
# 支持的文件格式
SUPPORTED_TYPE = [ext for sublist in LOADER_DICT.values() for ext in sublist]

"""知识库中单段文本长度(不适用MarkdownHeaderTextSplitter)"""
CHUNK_SIZE: int = 750

"""知识库中相邻文本重合长度(不适用MarkdownHeaderTextSplitter)"""
OVERLAP_SIZE: int = 150


#
# 获取文档加载器类
def get_LoaderClass(file_extension):
    for LoaderClass, extensions in LOADER_DICT.items():
        if file_extension in extensions:
            return LoaderClass


def get_loader(loader_name: str, file_path: str, loader_kwargs: Dict = None):
    """
    根据loader_name和文件路径或内容返回文档加载器。
    """
    loader_kwargs = loader_kwargs or {}
    try:
        if loader_name in [
            "RapidOCRPDFLoader",
            "RapidOCRLoader",
            "FilteredCSVLoader",
            "RapidOCRDocLoader",
            "RapidOCRPPTLoader",
        ]:
            document_loaders_module = importlib.import_module(
                "chat_app.knowledge.docment_loaders"
            )
        else:
            document_loaders_module = importlib.import_module(
                "langchain_community.document_loaders"
            )
        DocumentLoader = getattr(document_loaders_module, loader_name)
    except Exception as e:
        msg = f"为文件{file_path}查找加载器{loader_name}时出错：{e}"
        logger.error(f"{e.__class__.__name__}: {msg}")
        document_loaders_module = importlib.import_module(
            "langchain_community.document_loaders"
        )
        DocumentLoader = getattr(document_loaders_module, "UnstructuredFileLoader")

    if loader_name == "UnstructuredFileLoader":
        loader_kwargs.setdefault("autodetect_encoding", True)
    elif loader_name == "CSVLoader":
        if not loader_kwargs.get("encoding"):
            # 如果未指定 encoding，自动识别文件编码类型，避免langchain loader 加载文件报编码错误
            with open(file_path, "rb") as struct_file:
                encode_detect = chardet.detect(struct_file.read())
            if encode_detect is None:
                encode_detect = {"encoding": "utf-8"}
            loader_kwargs["encoding"] = encode_detect["encoding"]

    elif loader_name == "JSONLoader":
        loader_kwargs.setdefault("jq_schema", ".")
        loader_kwargs.setdefault("text_content", False)
    elif loader_name == "JSONLinesLoader":
        loader_kwargs.setdefault("jq_schema", ".")
        loader_kwargs.setdefault("text_content", False)

    loader = DocumentLoader(file_path, **loader_kwargs)
    return loader


@lru_cache()
def make_text_splitter(
    splitter_name, chunk_size, chunk_overlap, character_separators, recursive_separators
):
    """
    根据参数获取特定的分词器
    """
    splitter_name = splitter_name or "SpacyTextSplitter"
    try:
        if (
            splitter_name == "MarkdownHeaderTextSplitter"
        ):  # MarkdownHeaderTextSplitter特殊判定
            headers_to_split_on = KnowTextSplitter.MarkdownHeaderTextSplitter.value[
                "headers_to_split_on"
            ]
            text_splitter = MarkdownHeaderTextSplitter(
                headers_to_split_on=headers_to_split_on, strip_headers=False
            )
        else:
            try:  # 优先使用用户自定义的text_splitter
                text_splitter_module = importlib.import_module(
                    "chat_app.knowledge.text_splitter"
                )
                TextSplitter = getattr(text_splitter_module, splitter_name)
                print(f"TextSplitter type: {type(TextSplitter)}")  # 调试信息
            except:  # 否则使用langchain的text_splitter
                text_splitter_module = importlib.import_module(
                    "langchain.text_splitter"
                )
                TextSplitter = getattr(text_splitter_module, splitter_name)
            params = {"chunk_size": chunk_size, "chunk_overlap": chunk_overlap}
            # 长度分词器分隔符
            if splitter_name == "CharacterTextSplitter":
                params["separators"] = character_separators
            # 结构分词器分隔符
            if splitter_name == "RecursiveCharacterTextSplitter":
                params["separators"] = recursive_separators

            text_splitter = TextSplitter(**params)
    except Exception as e:
        print(e)
        text_splitter_module = importlib.import_module("langchain.text_splitter")
        TextSplitter = getattr(text_splitter_module, "RecursiveCharacterTextSplitter")
        text_splitter = TextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    return text_splitter


class KnowTextSplitter(Enum):
    """分词器"""

    ChineseTextSplitter = {"value": "1", "class_name": "ChineseTextSplitter"}
    ChineseRecursiveTextSplitter = {
        "value": "2",
        "class_name": "ChineseRecursiveTextSplitter",
    }
    CharacterTextSplitter = {"value": "3", "class_name": "CharacterTextSplitter"}
    RecursiveCharacterTextSplitter = {
        "value": "4",
        "class_name": "RecursiveCharacterTextSplitter",
    }
    MarkdownHeaderTextSplitter = {
        "value": "5",
        "class_name": "MarkdownHeaderTextSplitter",
        "headers_to_split_on": [
            ("#", "head1"),
            ("##", "head2"),
            ("###", "head3"),
            ("####", "head4"),
        ],
    }

    @staticmethod
    def get_text_splitter(value) -> str:
        """根据value获取枚举名称"""
        for type in KnowTextSplitter:
            if type.value["value"] == value:
                return type.value["class_name"]


class KnowDocumentFile:
    """文档对象"""

    def __init__(
        self,
        title: str,
        file_path: str,
        file_type: str,
        file_config: Dict = {},
    ):
        """
        对应知识库目录中的文件，必须是磁盘上存在的才能进行向量化等操作。

        参数:
        - title (str): 文件名称。
        - file_path (str): 文件路径。
        - file_type (str): 文件类型。
        - file_config (Dict, optional): 文件配置字典，默认为空字典。

        异常:
        - 如果文件类型不在支持的文件类型列表中，则抛出异常。
        """
        self.lock = threading.Lock()
        self.file_type = file_type
        self.file_path = file_path
        self.title = title
        self.file_config = file_config if file_config is not None else {}
        # 检查文件类型是否在支持的类型列表中
        if self.file_type not in SUPPORTED_TYPE:
            raise AgentResponse(f"暂未支持的文件格式 {title}{file_type}")
        # 验证文件路径是否存在
        if not self.file_exist():
            raise AgentResponse(f"文件路径 {file_path} 不存在")
        self.docs = None
        self.splited_docs = None

        # 根据文件扩展名获取文档加载器名称
        self.document_loader_name = get_LoaderClass(self.file_type)

        # 设置默认的块大小和重叠大小
        self.chunk_size = CHUNK_SIZE
        self.chunk_overlap = OVERLAP_SIZE

        # 如果文件配置不为空，则根据配置设置文本分割器和相关参数
        if self.file_config:
            text_splitter = file_config.get("text_splitter")
            self.text_splitter_name = KnowTextSplitter.get_text_splitter(text_splitter)
            self.chunk_size = file_config.get("max_length")
            self.chunk_overlap = file_config.get("overlap_length")
            # 长度分词器分隔符列表
            char_separators = file_config.get("char_separators")
            if char_separators is not None:
                self.character_separators = char_separators.replace("/n", "\n")
            # 结构分词器分隔符列表
            self.recursive_separators = file_config.get("recursive_separators")
            if self.recursive_separators is not None:
                self.recursive_separators = self.recursive_separators.replace(
                    "/n", "\n"
                )

    def file2docs(self):
        """
        将文件转换为文档集合。

        如果文档集合(self.docs)尚未加载，则使用指定的文档加载器(self.document_loader_name)
        从文件路径(self.file_path)中加载文档数据。此方法首先检查文档集合是否为空，
        如果为空则表示尚未加载，接着根据指定的加载器名称获取相应的加载器实例，
        并根据情况设置编码格式（针对TextLoader）。

        返回:
        - self.docs: 加载后的文档集合。
        """
        # 检查文档集合是否已经加载
        if self.docs is None:
            # 记录日志信息，说明使用了哪个加载器以及文件路径
            logger.info(f"{self.document_loader_name} used for {self.file_path}")

            # 获取文档加载器实例
            loader = get_loader(
                loader_name=self.document_loader_name,
                file_path=self.file_path,
                loader_kwargs=None,
            )

            # 针对TextLoader类型的加载器设置编码格式为utf8
            if isinstance(loader, TextLoader):
                loader.encoding = "utf8"

            # 使用加载器加载文档数据
            self.docs = loader.load()

        # 返回加载的文档集合
        return self.docs

    def docs2texts(
        self,
        docs: List[Document] = None,
        text_splitter: TextSplitter = None,
    ) -> List[Document]:
        """
        将文档对象列表转换为文本列表。

        如果未提供文档列表，将调用`self.file2docs()`生成。
        根据文件扩展名和文本分割器对文档进行分割。

        参数:
        - docs (List[Document], optional): 文档对象列表。默认为None。
        - text_splitter (TextSplitter, optional): 文本分割器。默认为None。

        返回:
        - List[Document]: 分割后的文档对象列表。
        """
        # 如果未提供docs参数，调用self.file2docs()生成
        docs = docs or self.file2docs()
        # 如果docs为空，返回空列表
        if not docs:
            return []

        # 如果文件扩展名不在指定列表中，根据提供的或默认的文本分割器进行分割
        if self.file_type not in [".csv"]:
            # 如果未提供text_splitter，创建一个
            if text_splitter is None:
                text_splitter = make_text_splitter(
                    splitter_name=self.text_splitter_name,
                    chunk_size=self.chunk_size,
                    chunk_overlap=self.chunk_overlap,
                    character_separators=self.character_separators,
                    recursive_separators=self.recursive_separators,
                )
            # 根据文本分割器的类型，执行不同的分割策略
            if self.text_splitter_name == "MarkdownHeaderTextSplitter":
                docs = text_splitter.split_text(docs[0].page_content)
            else:
                docs = text_splitter.split_documents(docs)

        # 如果分割后的docs为空，返回空列表
        if not docs:
            return []
        else:
            # 增加文本标题来源
            if len(docs) > 0:
                for doc in docs:
                    doc.metadata["title"] = self.title

        # 打印文档分割示例
        print(f"文档切分示例：{docs[0]}")
        # 保存分割后的文档
        self.splited_docs = docs
        # 返回分割后的文档列表
        return self.splited_docs

    def file2text(
        self,
    ) -> List[Document]:
        """
        将文件转换为文本片段。

        如果尚未分割文档，则从文件中提取文档并将其转换为文本片段。

        参数:
        - text_splitter: 文本分割器，用于将文档分割成文本片段。如果未提供，则使用默认分割器。

        返回:
        - list: 文本片段的列表。
        """
        # 检查是否已经分割了文档，以避免重复处理
        with self.lock:
            if self.splited_docs is None:
                try:
                    # 从文件中提取文档
                    docs = self.file2docs()
                    # 将提取的文档转换为文本片段
                    self.splited_docs = self.docs2texts(docs=docs, text_splitter=None)
                except Exception as e:
                    logging.error(f"Error processing file: {e}")
                    raise AgentResponse("从文件中提取文档失败")

        return self.splited_docs

    def file_exist(self):
        return os.path.isfile(self.file_path)

    def get_mtime(self):
        return os.path.getmtime(self.file_path)

    def get_size(self):
        return os.path.getsize(self.file_path)
