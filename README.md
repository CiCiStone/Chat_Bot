# Chat_Bot
一个基于大模型LLM的API的极简网页设计。包含选择模型，创造对话，多轮对话，历史记录等功能。

1.运行结果如图所示

![image](https://github.com/CiCiStone/Chat_Bot/assets/174783580/c449c730-c85b-4a1f-a603-3ea919057df0)

2.环境配置

2.1 key的申请

本项目直接调用阿里云的大模型，使用SDK，API进行调用，所以配环境之前还需要创建阿里云账户，创建API-KEY并记录在key.txt文件中。
具体可根据产品手册创建账号，申请key，耗时大约5-10分钟。
产品手册链接：（[https://help.aliyun.com/zh/model-studio/getting-started/alibaba-cloud-model-studio-quick-start](https://help.aliyun.com/zh/model-studio/getting-started/alibaba-cloud-model-studio-quick-start?spm=a2c4g.11186623.0.0.50e23568cOeMY5)）

![image](https://github.com/CiCiStone/Chat_Bot/assets/174783580/1c0ef82e-4a53-493c-82db-c2cd40e87f89)


2.2环境配置

本项目只使用了flask等包，已经制作了requirements.txt，只需要在terminal输入pip install -r requirements.txt然后等待依赖安装完成。

3.运行项目

3.1设置key

本文建议创建key.txt来管理key，在主目录下创建一个key.txt文件，然后将申请的key写在第一行即可。

当然，也可以直接在下面的代码内将key写死进变量

![image](https://github.com/CiCiStone/Chat_Bot/assets/174783580/62e3cf6c-d7c4-48a1-aecb-a83c16d1c506)


3.2运行

本项目只需要运行app.py文件，然后在[127.0.0.1：5000](http://127.0.0.1:5000/)打开即可。
