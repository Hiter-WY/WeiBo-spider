from openai import OpenAI
from utils import return_userinfo
text = []
data = return_userinfo("周杰伦",1)
cleaned_texts = [entry['cleaned_text'] for entry in data]
client = OpenAI(
    api_key="sk-6GKmdaNAI7dczeXksnMufGYfMibfB7p4ee3HwUZZC6Lt5llT",  # 在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
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
print(completion.choices[0].message.content)
