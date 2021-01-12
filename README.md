# Zhihu_Spider

## 简介

本项目是一个简易知乎爬虫，用来获取想法和文章的相关数据，并存入 SQLite 数据库。

其中登录部分参考 [2020 年最新 Python 模拟登录知乎 支持验证码和 Cookies](https://github.com/zkqiang/zhihu-login)。

## 运行

1. 在项目根目录下新建 Python 虚拟环境。

   ```bash
   python -m venv venv
   ```

2. 进入虚拟环境并安装 Python 第三方库。

   ```bash
   . venv/bin/activate
   pip install -r requirements.txt
   ```

3. 安装 `jsdom`。

   ```bash
   npm install jsdom
   ```

4. 新建配置文件 `private_config.py` 并保存以下内容。

   ```python
   #!/usr/bin/python3
   # -*- coding:utf-8 -*-
   
   username = '***'  # 知乎登录用户名，手机号或邮箱
   password = '***'  # 知乎登录密码
   
   sqlite_file = '***'  # SQLite 文件路径
   ```

5. 运行 `get_data.py`。

   ```bash
   python get_data.py
   ```

   

   