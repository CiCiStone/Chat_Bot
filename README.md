# Chat_Bot
一个基于大模型LLM的API的极简网页设计。包含选择模型，创造对话，多轮对话，历史记录等功能。
1.运行结果如图所示
![image](https://github.com/CiCiStone/Chat_Bot/assets/174783580/c449c730-c85b-4a1f-a603-3ea919057df0)
2.环境配置
2.1 key的申请
本项目直接调用阿里云的大模型，使用SDK，API进行调用，所以配环境之前还需要创建阿里云账户，创建API-KEY并记录在key.txt文件中。
具体可根据产品手册创建账号，申请key，耗时大约5-10分钟
产品手册链接：（https://help.aliyun.com/zh/model-studio/getting-started/alibaba-cloud-model-studio-quick-start）
![image](https://github.com/CiCiStone/Chat_Bot/assets/174783580/1c0ef82e-4a53-493c-82db-c2cd40e87f89)
2.2环境配置
本项目只使用了flask等包，已经制作了requirements.txt，只需要在terminal输入pip install -r requirements.txt然后等待依赖安装完成。
3.运行项目
本项目只需要运行app.py文件，然后在[127.0.0.1：5000](http://127.0.0.1:5000/)打开即可。
