<p align="center">
    <h3>为ChatGPT等多种LLM提供了一个轻快好用的Web图形界面和众多附加功能</h3>
    <p align="center">
      <p>
        支持星火、千问众多模型  · 基于文件问答 · LLM本地部署 · 联网搜索 · Agent 助理 · 
      </p>
    </p>
  </p>

## 目录

* [概述](README.md#概述)
* [功能介绍](README.md#功能介绍)
    * [模型接入](README.md#模型接入)
    * [智能助手](README.md#自定义智能体)
    * [可切换的模型](README.md#可切换的模型)
    * [在线搜索](README.md#在线搜索)
    * [知识库](README.md#知识库)
* [快速上手](README.md#快速上手)
    * [源码安装部署/开发部署](README.md#源码安装部署开发部署)

## 概述
鉴于当前大多数大型语言模型主要依赖收费的token机制，给用户带来了使用上的不便。本项目应运而生，旨在构建一个免费且易于使用的大型模型系统，基于大模型技术，为用户打造专属的知识库与智能助手，让用户能够更加便捷、高效地获取信息与服务。

 项目图片:
![输入图片说明](img/6.png)
![输入图片说明](img/7.png)
![输入图片说明](img/1.png)
![输入图片说明](img/2.png)
![输入图片说明](img/3.png)
![输入图片说明](img/4.png)
![输入图片说明](img/5.png)
![输入图片说明](img/6.png)

## 功能介绍

### 模型接入
支持 [Groq](https://console.groq.com/playground)、[讯飞星火](https://xinghuo.xfyun.cn/)、[通义千问](https://www.aliyun.com/product/bailian)、[LMStudio](https://lmstudio.ai/)厂商大模型

Groq: 注册后可免费调用
讯飞星火:注册后可免费调用lite大模型
通义千问:首次注册送限定时序的调用token
LMStudio: 提供基于open ai 的接口，带GUI的本地模型调用

在页面上模型中方便快捷配置各种模型，不用修改源码
![输入图片说明](img/model.png.png)

### 自定义智能体
通过预制的prompt和上下文打造属于自己的智能助手
![输入图片说明](img/agent.png.png)

### 可切换的模型
在对话中，可随时切换各种大模型
![输入图片说明](img/chat.png)

### 在线搜索
提供基于网络搜索的工具，给LLM提供更准确的回答
![输入图片说明](img/websearch.png)

### 知识库
上传自己专属文档，打造自己的专有知识库

![输入图片说明](img/knowlege.png)

## 快速上手
### 源码安装部署/开发部署
#### 0. 拉取项目代码
                                              
如果您是想要使用源码启动的用户，请直接拉取 master 分支代码

```shell
git clone https://gitee.com/vfcm/hx_gpt.git
```
#### 1. 初始化开发环境

##### 1.1 安装node.js环境
‌下载Node.js安装包‌：首先，访问[Node.js官网](https:
odejs.org/zh-cn/download/)选择适合您操作系统的版本进行下载。对于Windows系统，通常选择64位的安装包。‌

##### 1.2 安装python环境
python.version >= 3.11.9
安装Python环境：首先，访问[Python官网](https://www.python.org/downloads/)选择适合您操作系统的版本进行下载。

##### 1.3 安装mysql数据库
mysql.version >= 8.0.0
安装mysql数据库：首先，访问[mysql官网](https://dev.mysql.com/downloads/mysql/)选择适合您操作系统的版本进行下载。

```
使用docker启动:

docker run -it --network mysql-network --rm mysql mysql -hsome-mysql -uexample-user -p
```

##### 1.4 安装redis-stack向量数据库
redis-stack.version >= 6.2.6-v17

```
使用docker启动:

$ docker run  -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```

#### 1.5 安装向量模型
方式一：进入[魔塔社区](https://www.modelscope.cn/home),搜索BAAI/bge-large-zh,然后下载模型文件到本地

```
使用命令行工具下载模型

modelscope download --model 'BAAI/bge-large-zh' --local_dir
'E://bge'
```
方式二：、使用阿里云盘下载模型

链接: https://pan.baidu.com/s/17fV4DHjTqQ5JADE31_EVeg?pwd=6b3i 提取码: 6b3i

下载完成后解压目录到本地
进入BAAI\bge-large-zh的目录中，并记录当前绝对路径

如：E:\plugIn\models\huggingface\sentence-transformers\BAAI\bge-large-zh

#### 2. 启动方式

##### 2.1 前后端分离启动

##### 2.1.1 启动前端项目
进入主项目根目录，打开命令行工具执行以下命令：
````
// 安装依赖包
npm install

// 调试方式启动
npm run dev
````
##### 2.1.1 启动后端项目
进入/server目录下，打开命令行工具执行以下命令：

1、安装虚拟环境，使用venv、conda或者其他包
2、执行pip install -r requirements.txt
3、打开chat_server\admin\settings.py,找到DATABASES，修改mysql数据库配置
```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "ai_agent",
        "USER": "root",  # 数据库用户名
        "PASSWORD": "123456",  # 数据库密码
        "HOST": "localhost",  # 数据库主机地址
        "PORT": "3306",  # 数据库端口号
    }
}
```    

4、执行python .\chat_server\manage.py  runserver 启动项目

5、打开浏览器访问 http://127.0.0.1:3000

6、点击模型,选择项目配置
配置大模型key和向量的模型路径

![输入图片说明](img/setting.png)


##### 2.2 后端一体化启动
##### 2.2.1 打包前端项目
进入主项目根目录，打开命令行工具执行以下命令：
````
// 安装依赖包
npm install

// 前端打包
npm run build
````
打包目录在当前目录的web文件夹中

##### 2.2.2 启动后端项目
1、2、3步骤跟[前后端分离-启动后端项目](README.md#####启动后端项目)一致
4、将前端打包文件复制到server\chat_server\web\目录下

5、执行python .\chat_server\manage.py  runserver 启动项目
6、打开浏览器访问 http://127.0.0.1:8000
6、点击模型,选择项目配置
7、配置大模型key和向量的模型路径

