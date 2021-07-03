## 前言
这个是 2.1 版本，使用现在流行的前后端分离思想重构。

体验网址：https://douyin.bigdataboy.cn

## 更新日志
2021.07.03：抖音更新网页版，已恢复正常使用

2020.05.30：使用 FastAPI 前后端分离重构

2020.05.02：已更新，正常使用

2020.04.27：抖音结构更新，已修复视频有水印。（失效了）

## 使用到的技术
后端：
- 语言：Python
- WEB框架：FastAPI （现代、快速（高性能）的 Web 框架）
- 服务器框架：Uvicorn（基于asyncio开发的一个轻量级高效的web服务器框架）
- 反向代理：Nginx (高性能的HTTP和反向代理web服务器)
- 进程管理：Supervisor (ython开发的一套通用的进程管理程序)

前端：
- UI框架：LayUI
- 静态文件存放：Nginx

## 目录结构说明
app：后端源码

fastapi_html：前端源码

## 部署教程
部署教程访问：[点击访问](https://bigdataboy.cn/post-271.html)
