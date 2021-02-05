from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from exceptions.public import ResponseException
from routers import douyin
import uvicorn
import settings

app = FastAPI(
    # 禁用 /docs
    docs_url=None,
    # 禁用 /redoc
    redoc_url=None
)

# 异常响应
@app.exception_handler(ResponseException)
async def unicorn_exception_handler(request: Request, exc: ResponseException):
    return JSONResponse(
        # 错误响应状态码
        status_code= exc.status_code,
        # 错误返回内容格式
        content={"msg": exc.msg},
    )

# 自定义验证错误提示
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc):
    return JSONResponse(content={"msg":"链接错误 ！！！"}, status_code=422)

# 设置跨域资源请求限制
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=settings.allow_methods,
    allow_headers=settings.allow_headers,
)

# 添加路径
app.include_router(douyin.router)


if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host="127.0.0.1",
        port=5000,
    )
