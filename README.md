# LaGou_Crawler / 拉勾网爬虫
爬取拉勾网岗位数据

## 说明
用python爬取拉勾网的岗位信息，并保存到MySQL数据库中

## 开发环境
- Arch Linux
- python 3.7.3
- mysql  Ver 15.1 Distrib 10.4.6-MariaDB, for Linux (x86_64) using readline 5.1
- 第三方库requests, pymysql

## 使用说明
1. 在MySQL中创建名为“lagou”的数据库
2. 安装第三方库requests, pymysql
3. 直接运行程序lagou.py, 按照提示输入相应的岗位信息，mysql用户名和密码
4. 重复爬取相同关键词时，需删除lagou数据库中相应的表

## 其他说明
1. 该项目为小白爬虫练习项目，练习如何获取ajax请求，解析Python字段。对反爬虫机制进行一定基础的了解。熟悉pymysql模块数据库相关操作。
2. 拉勾网一次最多显示30页信息，所以可以修改代码url，按条件爬取，可获取更多数据
