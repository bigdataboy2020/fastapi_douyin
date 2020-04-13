# -*- coding: utf-8 -*-
# @Time    : 20200411
# @Author  : 大数据男孩
# @Blog    ：https://bigdataboy.cn

import requests
import re

class DYSpider:

    def __init__(self):
        # get 获取3个参数 item_ids mid u_code
        self.share_url = ""
        self.item_ids = ""
        self.mid = ""
        self.u_code = ""

        # get 获取参数 dytk 后面大括号需要 item_ids
        self.dytk_url = "https://www.iesdouyin.com/share/video/{}/"
        self.dytk = ""

        # 获取信息接口 get
        self.infor_url = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/"

        self.headers = {
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        }

    def setUrl(self,url):
        self.share_url = url

    def get_imu(self):
        r = requests.get(url=self.share_url)
        dytk_data = r.url
        self.item_ids = re.search(r'video/(.+?)/', dytk_data).group(1)
        self.mid = re.search(r'mid=(.+?)&', dytk_data).group(1)
        self.u_code = re.search(r'u_code=(.+?)&', dytk_data).group(1)

    def get_dytk(self):
        url = self.dytk_url.format(self.item_ids)
        r = requests.get(url=url,headers = self.headers,params={
                                                                    "region": "CN",
                                                                    "mid": self.mid,
                                                                    "u_code": self.u_code,
                                                                    "titleType": "title",
                                                                    "utm_source": "copy_link",
                                                                    "utm_campaign": "client_share",
                                                                    "utm_medium": "android",
                                                                    "app": "aweme",
                                                                })
        self.dytk = re.search(r'dytk: "(.+?)" }\);', r.text)

    def get_infor(self):
        r = requests.get(url=self.infor_url,headers = self.headers ,params={
                                                                            "item_ids": self.item_ids,
                                                                            "dytk": self.dytk,
                                                                        })
        data_json = r.json()
        print(data_json)
        item_list = data_json.get("item_list")[0]
        # 标题
        desc = item_list.get("desc")
        # 原视频
       download_addr = item_list.get("video").get("play_addr").get("url_list")[0]
        # 动图
        dynamic_cover = item_list.get("video").get("dynamic_cover").get("url_list")
        # 静图
        origin_cover = item_list.get("video").get("origin_cover").get("url_list")
        return {"title":desc,"img_run":dynamic_cover,"img":origin_cover,"url":download_addr,'code': '200'}

    def run(self):
        res = {'code': '200', 'title': "", 'img': "", 'url': ""}
        try:
            self.get_imu()
            self.get_dytk()
        except:
            res["code"] = "502"
            return res  # 解析失败
        return self.get_infor()

if __name__ == '__main__':

    dys = DYSpider()
    dys.setUrl("https://v.douyin.com/cCcyF5/")
    print(dys.run())




