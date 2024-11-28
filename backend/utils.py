import requests
import time
import random
from urllib.parse import quote
from bs4 import BeautifulSoup
from datetime import datetime
from openai import OpenAI


# 返回用户的blog
def return_userinfo(keyword, max_pages=3):
    # 从输入的名字查找用户信息
    user_data = get_user_ids(keyword)
    a = 0
    results = []

    # 打印用户信息
    for user_id, info in user_data.items():

        # 设置请求微博内容的初始URL
        base_url = (f"https://m.weibo.cn/api/container/getIndex?t=0&luicode=10000011&lfid=100103type%3D1%26q%3D%E7%A7"
                    f"%8B%E5%AD%A3%E5%BC%80%E5%AD%A6&type=uid&value={user_id}&containerid=107603{user_id}")

        # 初始化 since_id 和页数计数器
        since_id = None
        page_count = 0

        while page_count < max_pages:
            # 构造请求URL（包含since_id时为下一页请求）
            current_url = base_url if since_id is None else f"{base_url}&since_id={since_id}"

            # 请求微博API
            res = requests.get(current_url)
            data = res.json()
            if res.status_code != 200 or 'data' not in data:
                print(f"Failed to retrieve data for page {page_count + 1}. Status code: {res.status_code}")
                break

            # 处理微博内容
            if "cards" in data["data"]:
                for card in data["data"]["cards"]:
                    # 处理 card_type 为 9 的卡片，通常是微博内容
                    if card.get("card_type") == 9 and "mblog" in card:
                        mblog = card["mblog"]
                        mid = mblog.get("mid", "")
                        # 获取微博文本内容
                        text = mblog.get("text", "")
                        created_time = mblog.get("created_at", "")

                        # 转换时间格式
                        try:
                            created_time = datetime.strptime(created_time, "%a %b %d %H:%M:%S %z %Y").strftime(
                                "%m/%d/%Y %H:%M:%S")
                        except ValueError:
                            pass

                        # 使用BeautifulSoup解析文本内容，去掉所有不包含“全文”关键字的链接
                        soup = BeautifulSoup(text, "html.parser")

                        cleaned_text = soup.get_text().strip()
                        if cleaned_text:
                            a = a + 1
                            results.append({"created_time": created_time, "cleaned_text": cleaned_text, "mid": mid})

            # 获取since_id，用于下一页的请求
            if "cardlistInfo" in data["data"] and "since_id" in data["data"]["cardlistInfo"]:
                since_id = data["data"]["cardlistInfo"]["since_id"]
            else:
                print("No more pages to fetch.")
                break

            # 增加页数计数器
            page_count += 1

            # 延时以避免请求过快
            time.sleep(random.uniform(1, 3))

    return results

# 根据关键字搜索
def return_keywords_info(keyword, max_pages=3):
    results = []
    encoded_string = quote(keyword)
    a = 0
    for page in range(1, max_pages + 1):
        # 构造请求 URL，添加 page 参数
        url = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{encoded_string}&page_type=searchall&page={page}"

        # 发送请求
        res = requests.get(url)

        # 解析返回数据
        if res.status_code == 200:
            data = res.json()
            if "data" in data and "cards" in data["data"]:
                for card in data["data"]["cards"]:
                    if "card_group" in card:
                        for item in card["card_group"]:
                            if "mblog" in item and "user" in item["mblog"]:
                                user = item["mblog"]["user"]
                                user_data = {
                                    "id": user.get("id"),
                                    "screen_name": user.get("screen_name"),
                                    "followers_count": user.get("followers_count"),
                                    "profile_url": user.get("profile_url"),
                                }

                                text = item["mblog"].get("text", "")

                                # 使用BeautifulSoup解析文本内容，去掉所有不包含"全文"关键字的链接
                                soup = BeautifulSoup(text, "html.parser")
                                for a_tag in soup.find_all("a"):
                                    if "全文" not in a_tag.get_text():
                                        a_tag.decompose()

                                cleaned_text = soup.get_text()
                                a = a + 1
                                results.append({"screen_name": user_data["screen_name"], "cleaned_text":cleaned_text})
                                # 输出处理后的数据
                                # print(f"User Data: {user_data}\nCleaned Text: {cleaned_text}\n")
        else:
            print(f"Failed to retrieve data from page {page}.")
    return results

# 获取用户的基本信息
def get_user_ids(original_string):
    output = {}

    # 对输入的关键词进行编码
    encoded_string = quote(original_string)

    # 构造请求 URL
    url = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{encoded_string}&page_type=searchall"

    # 发送请求
    res = requests.get(url)

    # 如果请求成功则解析数据
    if res.status_code == 200:
        data = res.json()

        # 提取 userinfo 键对应的值
        if 'data' in data and 'cards' in data['data']:
            cards = data['data']['cards']
            for card in cards:
                if 'card_group' in card:
                    for sub_card in card['card_group']:
                        if sub_card.get('user'):
                            user_info = sub_card['user']
                            user_id = user_info.get('id')
                            screen_name = user_info.get('screen_name')
                            followers_count = user_info.get('followers_count')
                            profile_url = user_info.get('profile_url')

                            # 将提取的信息存入输出字典
                            output[user_id] = {
                                'screen_name': screen_name,
                                'followers_count': followers_count,
                                'profile_url': profile_url
                            }

    else:
        print(f"Failed to get data. Status code: {res.status_code}")

    return output

# 返回用户blog对应的分类
def classify_userinfo(username, model):
    text_input = username
    infos = return_userinfo(text_input)
    output = {}
    for info in infos:
        clean_text = info.get("cleaned_text")
        created_time = info.get("created_time")
        if clean_text:
            classify_res = model.classify_text(clean_text)
            print(f"{created_time}: {clean_text} ------- {classify_res}")
            output[created_time] = {"clean_text": clean_text,
                                    "classify_text": classify_res}
    return output

def classify_single(text, model):
    return model.classify_text_batch(text)

def get_retransmission(mid):
    mid = mid
    # print(mid)
    retransmission_info = []
    for i in range(1, 5):
        url = f"https://m.weibo.cn/api/statuses/repostTimeline?id={mid}&page={i}"
        headers = {
            'Cookie': "choose your cookie"
        }
        res = requests.get(url=url, headers=headers)
        if res.status_code == 200:
            data = res.json()
            if data["ok"] == 1:
                users_data = data['data']['data']
                for user_data in users_data:
                    # 提取所需的信息
                    user_info = {
                        'screen_name': user_data['user']['screen_name'],
                        'description': user_data['user']['description'],
                        'profile_url': user_data['user']['profile_url'],
                        'id': user_data['user']['id']
                    }
                    retransmission_info.append({"mid": mid, "userinfo": user_info})
            else:
                print(f"Nothing in page{i}")
    # print(retransmission_info)
    return retransmission_info

def user_portrait(keyword):
    name = keyword
    data = return_userinfo(name, 3)
    cleaned_texts = [entry['cleaned_text'] for entry in data]
    client = OpenAI(
        api_key="your Kimi api",
        # 在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
        base_url="https://api.moonshot.cn/v1",
    )

    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system",
             "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
            {"role": "user", "content": f"请根据下面的用户的blog为其做一个用户画像：{cleaned_texts}"}
        ],
        temperature=0.3,
    )

    # 通过 API 我们获得了 Kimi 大模型给予我们的回复消息（role=assistant）
    return completion.choices[0].message.content


# if __name__ == "__main__":
    # keyword = input("Enter key: ")
    # # return_keywords_info(keyword)
    # # weibo_results = return_userinfo(keyword)
    # res = classify_userinfo(keyword)
    # print(res)
