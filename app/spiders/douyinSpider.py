# -*- coding: utf-8 -*-
# @Time    : 20210702
# @Author  : 大数据男孩
# @Blog    ：https://bigdataboy.cn

import requests
import re, json
from requests.utils import unquote


class DYSpider(object):

    def __init__(self, share_url):
        self.share_url = share_url  # 分享链接
        self.session = requests.Session()
        self.video_num = None  # 视频编号
        self.video_info = None  # 视频完整信息

    # 获取真实的视频编号
    def get_video_num(self) -> bool:
        s = self.session.get(
            url=self.share_url,
            headers={
                'Host': 'v.douyin.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            },
            allow_redirects=False

        )
        if s.status_code == 302:
            self.video_num = re.search(r'video/(\d+)/', s.headers.get('Location')).group(1)
            return True
        else:
            return False

    # 获取视频信息
    def get_video_info(self) -> bool:
        r = self.session.get(
            url=f'https://www.douyin.com/video/{self.video_num}',
            headers={
                'Host': 'www.douyin.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            },
            params={'previous_page': 'app_code_link'}
        )
        r = re.search(r'id="RENDER_DATA" type="application/json">(.+?)</script>', r.text).group(1)
        # print(unquote(r))
        self.video_info = json.loads(unquote(r))
        return True

    def get_info(self):
        # 标题
        desc = self.video_info.get('C_12').get('aweme').get('detail').get('desc')
        # 原视频
        video_url = "https:" + self.video_info.get('C_12').get('aweme').get('detail').get('video').get('playAddr')[
            0].get('src')
        # 动图
        dynamic_cover = "https:" + self.video_info.get('C_12').get('aweme').get('detail').get('video').get(
            'dynamicCover')
        # 静图
        origin_cover = "https:" + self.video_info.get('C_12').get('aweme').get('detail').get('video').get('cover')
        return {"title": desc, "img_run": dynamic_cover, "img": origin_cover, "url": video_url}

    def get(self):
        try:
            if not self.get_video_num():
                return None
            # print(self.video_num)
            if not self.get_video_info():
                return None
        except:
            # 报错返回 None
            return None
        else:
            # print(self.video_info)
            return self.get_info()


if __name__ == '__main__':
    dys = DYSpider(share_url="https://v.douyin.com/eqaknNr/").get()
    print(dys)
