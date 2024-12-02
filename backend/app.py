from flask import Flask, json, request, jsonify
from flask_cors import CORS
from utils import *
import sys
import os
import pymysql
from datetime import datetime, timedelta

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


def create_connection():
    try:
        connection = pymysql.connect(
            host='127.0.0.1',
            user='wangyu',
            password='123',
            database='project',
            port=3306
        )
        print("Connection to MySQL DB successful")
        return connection
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return None


# 初始化数据库连接
db_connection = create_connection()

if db_connection is None:
    print("Failed to connect to the database. Exiting.")
    sys.exit(1)  # 退出程序，因为没有数据库连接


# 定义路由，接收关键词并返回用户信息
@app.route('/api/userinfo', methods=['POST'])
def get_user_info():
    try:
        data = request.get_json()
        keyword = data.get('keyword')
        if not keyword:
            return jsonify({'error': 'Keyword is required'}), 400
        user_info = get_user_ids(keyword)
        id = next(iter(user_info))
        cursor = db_connection.cursor()
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, id)  # 使用元组传递参数
        # 获取查询结果
        result = cursor.fetchone()
        if result:
            current_time = datetime.now()
            time_difference = abs(current_time - result[4])
            # print(time_difference)
            thirty_minutes = timedelta(minutes=30)
            if time_difference <= thirty_minutes:
                print("The time difference is within 30 minutes.")
                query = "SELECT * FROM blogs WHERE id = %s"
                cursor.execute(query, id)
                results = cursor.fetchall()
                # 初始化 user_info 列表
                user_info = []
                for result in results:
                    user_info.append({"created_time": result[2], "cleaned_text": result[3], "mid": result[0]})
                return jsonify({'status': 'success', 'data': user_info})
            else:
                print("The time difference exceeds 30 minutes.")
                query = "UPDATE users SET updatatime = %s, userportrait_state = 1 WHERE id = %s"
                data = (datetime.now(), id)
                cursor.execute(query, data)
                db_connection.commit()  # 提交事务
                print("Updata updatatime to ", datetime.now())
                # 调用 return_userinfo 函数获取数据
                user_info = return_userinfo(keyword)
                for result in user_info:
                    mid = result['mid']
                    query = "SELECT * FROM blogs WHERE mid = %s"
                    cursor.execute(query, mid)
                    result = cursor.fetchone()
                    if result:
                        print("Old")
                    else:
                        created_time = result['created_time']
                        cleaned_text = result['cleaned_text']
                        query = "INSERT INTO blogs (mid,id,created_time, cleaned_text) VALUES (%s, %s, %s,%s)"
                        data = (mid, id, created_time, cleaned_text)
                        try:
                            cursor.execute(query, data)
                            db_connection.commit()  # 提交事务
                            print("New")
                        except pymysql.Error as e:
                            print(f"Error: {e}")
                return jsonify({'status': 'success', 'data': user_info})
        else:
            screen_name = user_info[id]['screen_name']
            followers_count = user_info[id]['followers_count']
            profile_url = user_info[id]['profile_url']
            current_time = datetime.now()
            query = "INSERT INTO users (id,screen_name,followers_count,profile_url,updatatime) VALUES (%s, %s, %s,%s,%s)"
            data = (id, screen_name, followers_count, profile_url, current_time)
            try:
                cursor.execute(query, data)
                db_connection.commit()  # 提交事务
                print("User info saved successfully")
            except pymysql.Error as e:
                print(f"Error: {e}")
            user_info = return_userinfo(keyword)
            for result in user_info:
                created_time = result['created_time']
                cleaned_text = result['cleaned_text']
                mid = result['mid']
                query = "INSERT INTO blogs (mid,id,created_time, cleaned_text) VALUES (%s, %s, %s,%s)"
                data = (mid, id, created_time, cleaned_text)
                try:
                    cursor.execute(query, data)
                    db_connection.commit()  # 提交事务
                    # print("Blog info saved successfully")
                except pymysql.Error as e:
                    print(f"Error: {e}")
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
        for result in keywords_info:
            screen_name = result['screen_name']
            cleaned_text = result['cleaned_text']
            cursor = db_connection.cursor()
            query = "INSERT INTO keywordsinfo (keyword, screen_name, cleaned_text) VALUES (%s, %s, %s)"
            data = (keyword, screen_name, cleaned_text)

            try:
                cursor.execute(query, data)
                db_connection.commit()  # 提交事务
                print("Keywords info saved successfully")
            except pymysql.Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
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
        cursor = db_connection.cursor()
        query = "SELECT * FROM blogs WHERE mid = %s"
        cursor.execute(query, mid)
        result = cursor.fetchone()
        if result[4]:
            current_time = datetime.now()
            time_difference = abs(current_time - result[4])
            thirty_minutes = timedelta(minutes=30)
            if time_difference >= thirty_minutes:
                print("The time difference is within 30 minutes.")
                query = "SELECT * FROM retransmission WHERE mid = %s"
                cursor.execute(query, mid)
                results = cursor.fetchall()
                retransmission_info = []
                for a in results:
                    user_info_dict = json.loads(a[1])
                    user_info = {
                        'screen_name': user_info_dict.get('screen_name'),
                        'description': user_info_dict.get('description'),
                        'profile_url': user_info_dict.get('profile_url'),
                        'id': user_info_dict.get('id')
                    }
                    retransmission_info.append({"mid": a[0], "userinfo": user_info})
                print(retransmission_info)
                return jsonify({'status': 'success', 'data': retransmission_info})
            else:
                print("The time difference exceeds 30 minutes.")
                query = "UPDATE blogs SET updatatime  = %s WHERE mid=%s"
                data = (datetime.now(), mid)
                cursor.execute(query, data)
                db_connection.commit()  # 提交事务
                print("Updata updatatime to ", datetime.now())
                retransmission_info = get_retransmission(mid)
                for result in retransmission_info:

                    id = result['userinfo']['id']
                    profile_url = result['userinfo']['profile_url']
                    description = result['userinfo']['description']
                    screen_name = result['userinfo']['screen_name']
                    # print(id)
                    # print(screen_name)
                    query = "SELECT * FROM retransmission WHERE JSON_EXTRACT(userinfo, '$.id') = %s AND JSON_EXTRACT(userinfo, '$.description') = %s AND JSON_EXTRACT(userinfo, '$.profile_url') = %s AND JSON_EXTRACT(userinfo, '$.screen_name') = %s"
                    data = (id, description, profile_url, screen_name)
                    cursor.execute(query, data)
                    result1 = cursor.fetchone()
                    if result1:
                        print("Old")
                    else:
                        query = "INSERT INTO retransmission (mid,userinfo) VALUES (%s, JSON_OBJECT('id', %s, 'profile_url',%s,'description', %s,'screen_name', %s))"
                        data = (mid, id, profile_url, description, screen_name)
                        try:
                            cursor.execute(query, data)
                            db_connection.commit()  # 提交事务
                            print("New")
                        except pymysql.Error as e:
                            print(f"Error: {e}")
                return jsonify({'status': 'success', 'data': retransmission_info})
        else:
            query = "UPDATE blogs SET updatatime = %s WHERE mid=%s"
            data = (datetime.now(), mid)
            cursor.execute(query, data)
            db_connection.commit()  # 提交事务
            print("Updata updatatime to ", datetime.now())
            retransmission_info = get_retransmission(mid)
            # print(retransmission_info)
            for result in retransmission_info:
                screen_name = result['userinfo']['screen_name']
                description = result['userinfo']['description']
                profile_url = result['userinfo']['profile_url']
                id = result['userinfo']['id']
                # print(user_info)
                # print(mid)
                query = "INSERT INTO retransmission (mid,userinfo) VALUES (%s, JSON_OBJECT('id', %s, 'profile_url',%s,'description', %s,'screen_name', %s))"
                data = (mid, id, profile_url, description, screen_name)
                try:
                    cursor.execute(query, data)
                    db_connection.commit()  # 提交事务
                    print("Retransmission info saved successfully")
                except pymysql.Error as e:
                    print(f"Error: {e}")
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
        user_info = get_user_ids(keyword)
        id = next(iter(user_info))
        cursor = db_connection.cursor()
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, id)
        result = cursor.fetchone()
        if result[5]:
            if result[6] == 1:
                user_portrait_info = user_portrait(keyword)
                query = "UPDATE users SET userportrait = %s, userportrait_state = 0 WHERE id = %s"
                # 压缩
                compressed_data = compress_text(user_portrait_info)
                data = (compressed_data, id)
                cursor.execute(query, data)
                db_connection.commit()  # 提交事务
                print("Userportrait info updatad successfully")

                return jsonify({'status': 'success', 'data': user_portrait_info})
            elif result[6] == 0:
                query = "SELECT * FROM users WHERE id = %s"
                cursor.execute(query, id)
                result = cursor.fetchone()
                user_portrait_info = result[5]
                # 解压
                decompress_data = decompress_text(user_portrait_info)
                return jsonify({'status': 'success', 'data': decompress_data})
        else:
            user_portrait_info = user_portrait(keyword)
            query = "UPDATE users SET userportrait = %s, userportrait_state = 0 WHERE id = %s"
            # 压缩
            compressed_data = compress_text(user_portrait_info)
            data = (compressed_data, id)
            cursor.execute(query, data)
            db_connection.commit()  # 提交事务
            print("Userportrait info saved successfully")

            return jsonify({'status': 'success', 'data': user_portrait_info})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
@app.route('/api/databasenumber', methods=['POST'])
def databasenumber_api():
    try:
        query = "SELECT COUNT(*) FROM blogs"
        cursor = db_connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        # return result[0]
        return jsonify({'status': 'success', 'data': result[0]})
    except:
        return -1

if __name__ == '__main__':
    # device = "cuda" if torch.cuda.is_available() else "cpu"
    # batch = 4
    # bert_classifier_path = "/Users/wangyu/大四实践/项目/BertClassifier-master/"
    # model_path = "models/best_model.pkl"
    # model = Bert(device, batch, bert_classifier_path=bert_classifier_path, model_path=model_path)

    app.run(debug=True)
