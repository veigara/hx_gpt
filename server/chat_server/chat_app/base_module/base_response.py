from dataclasses import dataclass, asdict

"""返回消息"""


@dataclass
class AgentResponse:
    # 状态码
    code: int
    # 数据
    data: any
    # 消息
    msg: str

    @staticmethod
    def success(data: object):
        """返回成功的响应"""
        data = AgentResponse(code=200, data=data, msg="Success")
        return asdict(data)

    @staticmethod
    def fail(fail_msg: str):
        """返回失败的响应"""
        return asdict(AgentResponse(code=500, msg=fail_msg, data=None))
