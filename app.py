from flask import Flask, request, jsonify, render_template
import random
from http import HTTPStatus
from Chat_SQ.Channel_manager import get_message
from dashscope import Generation  # 建议dashscope SDK 的版本 >= 1.14.0
import dashscope
import os
import json
dashscope.api_key = open("./key.txt", 'r', encoding='utf-8').readline()

app = Flask(__name__)

# 加载历史对话
if os.path.exists('conversations.json'):
    with open('conversations.json', 'r', encoding='utf-8') as f:
        conversations_data = json.load(f)
else:
    conversations_data = {"dialogs": {}, "current_dialog_id": None}

# 定义可选择的模型列表
available_models = ["qwen-max", "qwen-long", "qwen-max-longcontext"]

# 初始化全局变量
current_model = 'qwen-max'

def process_message(message, model, history=[]):
    # 自定义的处理函数，返回处理结果
    message = get_message(content=message)
    history.append(message)
    print("messages: ", history)
    response = Generation.call(model=model,
                               messages=history,
                               # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
                               seed=random.randint(1, 10000),
                               # 将输出设置为"message"格式
                               result_format='message')

    if response.status_code == HTTPStatus.OK:
        return response.output["choices"][0]["message"]["content"]
    else:
        print('Request id: %s, Status code: %s, Detail: %s' % (
            response.request_id,
            response.status_code,
            response.detail if response.detail else ''))
        return "Error: 请求失败"


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', dialogs=conversations_data["dialogs"], current_dialog_id=conversations_data["current_dialog_id"], models=available_models, current_model=current_model)


@app.route('/send_message', methods=['POST'])
def send_message():
    global current_model
    data = request.form
    message = data.get('message')
    current_dialog_id = conversations_data["current_dialog_id"]

    if not current_dialog_id:
        return jsonify({'error': '请选择或创建一个对话。'})

    if current_dialog_id not in conversations_data["dialogs"]:
        conversations_data["dialogs"][current_dialog_id] = {"name": f"对话{current_dialog_id}", "conversations": []}

    dialog = conversations_data["dialogs"][current_dialog_id]
    history = dialog["conversations"]
    response = process_message(message, current_model, history)
    dialog["conversations"].append({"role": "user", "content": message})
    dialog["conversations"].append({"role": "bot", "content": response})

    with open('conversations.json', 'w', encoding='utf-8') as f:
        json.dump(conversations_data, f, ensure_ascii=False, indent=4)

    return jsonify({'message': message, 'response': response})


@app.route('/create_dialog', methods=['POST'])
def create_dialog():
    new_id = str(random.randint(10000, 99999))
    conversations_data["dialogs"][new_id] = {"name": f"对话{new_id}", "conversations": []}
    conversations_data["current_dialog_id"] = new_id

    with open('conversations.json', 'w', encoding='utf-8') as f:
        json.dump(conversations_data, f, ensure_ascii=False, indent=4)

    return jsonify({"dialogs": conversations_data["dialogs"], "current_dialog_id": new_id})


@app.route('/select_dialog', methods=['POST'])
def select_dialog():
    data = request.form
    dialog_id = data.get('dialog_id')
    if dialog_id in conversations_data["dialogs"]:
        conversations_data["current_dialog_id"] = dialog_id

        with open('conversations.json', 'w', encoding='utf-8') as f:
            json.dump(conversations_data, f, ensure_ascii=False, indent=4)

        return jsonify({"current_dialog_id": dialog_id, "conversations": conversations_data["dialogs"][dialog_id]["conversations"]})
    else:
        return jsonify({'error': '对话ID不存在。'})


@app.route('/delete_dialog', methods=['POST'])
def delete_dialog():
    data = request.form
    dialog_id = data.get('dialog_id')

    if dialog_id in conversations_data["dialogs"]:
        del conversations_data["dialogs"][dialog_id]

        if conversations_data["current_dialog_id"] == dialog_id:
            conversations_data["current_dialog_id"] = None

        with open('conversations.json', 'w', encoding='utf-8') as f:
            json.dump(conversations_data, f, ensure_ascii=False, indent=4)

        return jsonify({"dialogs": conversations_data["dialogs"], "current_dialog_id": conversations_data["current_dialog_id"]})
    else:
        return jsonify({'error': '对话ID不存在。'})


@app.route('/rename_dialog', methods=['POST'])
def rename_dialog():
    data = request.form
    dialog_id = data.get('dialog_id')
    new_name = data.get('new_name')

    if dialog_id in conversations_data["dialogs"]:
        conversations_data["dialogs"][dialog_id]["name"] = new_name

        with open('conversations.json', 'w', encoding='utf-8') as f:
            json.dump(conversations_data, f, ensure_ascii=False, indent=4)

        return jsonify({"dialogs": conversations_data["dialogs"], "current_dialog_id": conversations_data["current_dialog_id"]})
    else:
        return jsonify({'error': '对话ID不存在。'})


@app.route('/select_model', methods=['POST'])
def select_model():
    global current_model
    data = request.form
    model = data.get('model')
    if model in available_models:
        current_model = model
        return jsonify({'success': True, 'current_model': current_model})
    else:
        return jsonify({'error': '模型不存在。'})


if __name__ == '__main__':
    app.run(debug=True)
