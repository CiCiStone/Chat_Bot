import random
from http import HTTPStatus
from dashscope import Generation  # 建议dashscope SDK 的版本 >= 1.14.0
import dashscope
import os
import json


def get_message(role="user", content=""):
    """创建一个包含角色和内容的消息字典。

    Args:
        role (str): 消息的角色，如"user"或"system"。默认为"user"。
        content (str): 消息的内容。默认为空字符串。

    Returns:
        dict: 包含角色和内容的消息字典。
    """
    message = {'role': role, 'content': content}
    return message

class Channel_manager():
    def __init__(self, path="./record/channels.json"):
        self.channels = []
        self.json_f = self.get_json_data(status="r")
        self.__init_channels(self.json_f)
        self.max_id = 1
        if len(self.channels):
            self.max_id = self.channels[-1].ID

    def get_json_data(self, path="./record/channels.json", status="r"):
        json_f = json.load(open(path, status, encoding='utf-8'))
        return json_f

    def __init_channels(self, json_f):
        for channel in json_f:
            temp = Channel(messages=channel["messages"], channel_name=channel["channel_name"], id=channel["id"])
            self.channels.append(temp)

    def create_channel(self):
        self.channels.append(Channel(id=self.max_id + 1))
        self.max_id += 1


class Channel():
    def __init__(self, messages=[], channel_name="", id=1):
        self.ID = id
        self.history = []
        for message in messages:
            self.history.append(self.modify_message(message))
        self.name = channel_name
        self.size = len(self.history)

    def modify_message(self, message: dict):
        if "role" in message.keys() and "content" in message.keys():
            return get_message(message["role"], message["content"])
        else:
            raise ValueError(f"data is not enough to create a message: {message}")

    def get_history(self):
        return self.history

    def insert_history(self, message):
        self.history.append(self.modify_message(message))
        self.size += 1

    def modify_last_message(self, content):
        self.history[-1]["content"] = content