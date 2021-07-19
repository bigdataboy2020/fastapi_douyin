# -*- coding: utf-8 -*-
# @Time    : 20210719
# @Author  : 大数据男孩
# @Blog    ：https://bigdataboy.cn

import requests
import re


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
            url=f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/',
            headers={
                'Host': 'www.douyin.com',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36',
            },
            params={'item_ids': self.video_num}
        )
        if r.status_code == 200:
            self.video_info = r.json()
            return True
        else:
            return False

    def get_info(self):
        # 标题
        desc = self.video_info.get('item_list')[0].get('share_info').get('share_title')
        # 原视频
        video_url = self.video_info.get('item_list')[0].get('video').get('play_addr').get('url_list')[0].replace("playwm", "play")
        # 动图
        dynamic_cover = self.video_info.get('item_list')[0].get("video").get("dynamic_cover").get("url_list")
        # 静图
        origin_cover = self.video_info.get('item_list')[0].get("video").get("origin_cover").get("url_list")

        return {"title": desc, "img_run": dynamic_cover, "img": origin_cover, "url": video_url}

    def get(self):
        try:
            if not self.get_video_num():
                return None
            # print(self.video_num)
            if not self.get_video_info():
                return None
        except:
            return None
        else:
            return self.get_info()


if __name__ == '__main__':
    dys = DYSpider(share_url="https://v.douyin.com/esXYJaY/").get()
    print(dys)
