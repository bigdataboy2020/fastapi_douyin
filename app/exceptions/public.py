# 异常参数类
class ResponseException(Exception):
    def __init__(self, status_code: int, msg: str):
        # 错误状态码
        self.status_code = status_code
        # 错误内容
        self.msg = msg

