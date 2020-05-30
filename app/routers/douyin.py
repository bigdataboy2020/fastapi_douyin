from fastapi import APIRouter, Query
from exceptions.public import ResponseException
import re
# 导入解析
from spiders.douyinSpider import DYSpider

router = APIRouter()

# 接口
@router.get("/douyin")
async def douyinapi(
        # 接口验证
        url: str = Query(
            ...,
            title="视频链接",
            description="抖音视频分享链接",
            min_length=6,
            regex=re.compile(r".*https:\/\/v\.douyin\.com\/[a-zA-Z0-9/]+").pattern
        )
):
    # 取出链接
    share_url = re.search(r"https://v\.douyin\.com/[a-zA-Z0-9/]+",url).group()
    # 链接解析
    dys = DYSpider(share_url=share_url)
    res = dys.get()
    # 判断是否解析成功
    if res == None:
        raise ResponseException(status_code= 422,msg="解析失败，检查链接重试，还不行联系 QQ：876545500")
    else:
        return res