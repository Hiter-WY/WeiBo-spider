from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import *
import sys
import os

import torch

bert_classifier_path = os.path.abspath('../BertClassifier-master')
sys.path.append(bert_classifier_path)

from predict import Bert

device = "cuda" if torch.cuda.is_available() else "cpu"
batch = 4
bert_classifier_path = "/Users/wangyu/大四实践/项目/BertClassifier-master/"
model_path = "models/best_model.pkl"
model = Bert(device, batch, bert_classifier_path=bert_classifier_path, model_path=model_path)

app = Flask(__name__)
CORS(app)  # 允许跨域请求


# 定义路由，接收关键词并返回用户信息
@app.route('/api/userinfo', methods=['POST'])
def get_user_info():
    try:
        data = request.get_json()
        keyword = data.get('keyword')
        if not keyword:
            return jsonify({'error': 'Keyword is required'}), 400

        # 调用 return_userinfo 函数获取数据
        user_info = return_userinfo(keyword)
        return jsonify({'status': 'success', 'data': user_info})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# 定义路由，接收关键词并返回微博内容信息
@app.route('/api/keywordsinfo', methods=['POST'])
def get_keywords_info():
    try:
        data = request.get_json()
        keyword = data.get('keyword')
        if not keyword:
            return jsonify({'error': 'Keyword is required'}), 400

        # 调用 return_keywords_info 函数获取数据
        keywords_info = return_keywords_info(keyword)
        return jsonify({'status': 'success', 'data': keywords_info})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# 定义路由，接收用户名并返回微博内容分类
@app.route('/api/classifyuserinfo', methods=['POST'])
def classify_user_info():
    try:
        data = request.get_json()
        username = data.get('username')
        if not username:
            return jsonify({'error': 'Username is required'}), 400

        # 调用 classify_userinfo 函数获取数据
        classified_info = classify_userinfo(username, model)
        return jsonify({'status': 'success', 'data': classified_info})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/classfiy', methods=['POST'])
def classify_single_api():
    try:
        data = request.get_json()
        # print(data)
        text = data.get('text')
        # print(text)
        res = classify_single(text, model)
        print(res)
        return jsonify({'status': 'success', 'data': res})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/retransmission', methods=['POST'])
def retransmission_info_api():
    try:
        data = request.get_json()
        mid_list = data.get("mid")
        mid = mid_list[0]
        # print(mid)
        if not mid:
            return jsonify({'error': 'Keyword is required'}), 400
        retransmission_info = get_retransmission(mid)
        # print(retransmission_info)
        return jsonify({'status': 'success', 'data': retransmission_info})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/userportrait', methods=['POST'])
def user_portrait_api():
    try:
        data = request.get_json()
        keyword = data.get('keyword')
        if not keyword:
            return jsonify({'error': 'Keyword is required'}), 400
        user_portrait_info = user_portrait(keyword)
        return jsonify({'status': 'success', 'data': user_portrait_info})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    # device = "cuda" if torch.cuda.is_available() else "cpu"
    # batch = 4
    # bert_classifier_path = "/Users/wangyu/大四实践/项目/BertClassifier-master/"
    # model_path = "models/best_model.pkl"
    # model = Bert(device, batch, bert_classifier_path=bert_classifier_path, model_path=model_path)

    app.run(debug=True)
