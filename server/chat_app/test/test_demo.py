from enum import Enum


class TextSplitter(Enum):
    """分词器"""

    ChineseTextSplitter = "1"
    ChineseRecursiveTextSplitter = "2"
    CharacterTextSplitter = "3"
    RecursiveCharacterTextSplitter = "4"

    @staticmethod
    def get_text_splitter(value) -> str:
        """根据value获取枚举名称"""
        for type in TextSplitter:
            if type.value == value:
                return type.name


if __name__ == "__main__":
    print(TextSplitter.get_text_splitter("1"))
