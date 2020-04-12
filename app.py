# -*- coding: utf-8 -*-
# @Time    : 20200411
# @Author  : 大数据男孩
# @Blog    ：https://bigdataboy.cn

from flask import Flask,render_template,request,abort
import json
from api import DYSpider
import re

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/douyin",methods=["GET"])
def douyin():
    print(request.headers)
    # 防盗
    if '127.0.0.1' not in str(request.referrer):
        abort(403)
    # 默认返回内容
    return_dict = {'code': '200', 'info': '处理成功', 'title': None, 'img': None, 'url': None,'img_run':None}

    # 获取传入的params参数
    get_data = request.args.to_dict()
    url = get_data.get('url')

    # 判断 url 是否为空
    if url is "":
        return_dict["code"] = "5004"
        return_dict["info"] = "请输入网址"
        return json.dumps(return_dict, ensure_ascii=False)

    # 网址有效性检验
    try:
        url = re.search(r"https://v\.douyin\.com/(.+)",url).group()
    except Exception:
        return_dict["code"] = "5000"
        return_dict["info"] = "请检查网址格式是否正确"
        return json.dumps(return_dict, ensure_ascii=False)
    else:
        print(url)
        # 请求接口
        dys= DYSpider()
        dys.setUrl(url)
        r = dys.run()
        # 判断接口解析情况
        if r.get("code") == "502" :
            # 有时候会因为没有加 右端的反斜杠 会造成解析失败，所以加了一个判断
            if url[-1] == "/":
                return_dict["code"] = "5001"
                return_dict["info"] = "网址抽风了，请再试一次"
            else:
                return_dict["code"] = "5002"
                return_dict["info"] = "视频解析失败，请检查链接是否有效"
            return json.dumps(return_dict, ensure_ascii=False)
        elif r.get("code") == "200" :
            # 对参数进行操作
            return_dict["title"] = r.get("title")
            return_dict["img"] = r.get("img")
            return_dict["url"] = r.get("url")
            return_dict["img_run"] = r.get("img_run")
            return  json.dumps(return_dict, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=True)
