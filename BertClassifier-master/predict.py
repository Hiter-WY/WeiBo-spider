import time
import os

import torch
from model import BertClassifier
from transformers import BertTokenizer, BertConfig
from dataset import WeiboDataset
from torch.utils.data import DataLoader


class Bert():
    def __init__(self,
                 device="cuda",
                 batch=4,
                 bert_classifier_path="/Users/wangyu/大四实践/项目/BertClassifier-master/",
                 model_path="models/best_model.pkl",
                 config_path="pretrained-models/bert-base-chinese/config.json",
                 tokenizer_path="pretrained-models/bert-base-chinese/"):
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        self.batch = batch

        self.labels = [
            "体育",
            "娱乐",
            "家居",
            "房产",
            "教育",
            "时尚",
            "时政",
            "游戏",
            "科技",
            "财经",
        ]
        self.model_path = os.path.join(bert_classifier_path, model_path)
        self.config_path = os.path.join(bert_classifier_path, config_path)
        self.tokenizer_path = os.path.join(bert_classifier_path, tokenizer_path)

        self.bert_config = BertConfig.from_pretrained(self.config_path)

        # 定义模型
        self.model = BertClassifier(self.bert_config, len(self.labels)).to(self.device)

        # 加载训练好的模型
        self.model.load_state_dict(
            torch.load(self.model_path, map_location=torch.device(self.device), weights_only=False)
        )
        self.model.eval()

        self.tokenizer = BertTokenizer.from_pretrained(self.tokenizer_path)

    def classify_text(self, text):
        # 输入文本的处理
        token = self.tokenizer(
            text,
            add_special_tokens=True,
            padding="max_length",
            truncation=True,
            max_length=512,
        )
        input_ids = token["input_ids"]
        attention_mask = token["attention_mask"]
        token_type_ids = token["token_type_ids"]

        input_ids = torch.tensor([input_ids], dtype=torch.long).to(self.device)
        attention_mask = torch.tensor([attention_mask], dtype=torch.long).to(self.device)
        token_type_ids = torch.tensor([token_type_ids], dtype=torch.long).to(self.device)

        # 进行预测
        predicted = self.model(
            input_ids,
            attention_mask,
            token_type_ids,
        )
        pred_label = torch.argmax(predicted, dim=1)

        return self.labels[pred_label]

    def classify_text_batch(self, data_path):
        start_time = time.time()
        weibo_dataset = WeiboDataset(data_path, self.tokenizer)
        dataloader = DataLoader(weibo_dataset, batch_size=self.batch)
        pred_labels_list = []
        texts_list = []

        end_time = time.time()
        print(f"load dataset time: {end_time - start_time:.2f} seconds")

        print("start inference...")
        start_time = time.time()
        with torch.no_grad():
            for input_ids, token_type_ids, attention_mask, texts in dataloader:
                output = self.model(
                    input_ids=input_ids.to(self.device),
                    attention_mask=attention_mask.to(self.device),
                    token_type_ids=token_type_ids.to(self.device),
                )
                predictions = torch.argmax(output, dim=1)
                pred_labels_list.extend(predictions.cpu().numpy())  # 追加预测标签到列表
                texts_list.extend(texts)  # 追加原始文本到列表

        end_time = time.time()
        print(f"inference time: {end_time - start_time:.2f} seconds")
        print("finished!")

        # 返回文本与对应的预测标签
        # return list(zip(texts_list, [self.labels[i] for i in pred_labels_list]))
        return [self.labels[i] for i in pred_labels_list]

# 使用模式调用函数
if __name__ == "__main__":
    # print("动态类别分类")
    # while True:
    #     text = input("Input: ")
    #     label = classify_text(text)
    #     print("Label:", label)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    batch = 4
    model = Bert(device, batch)

    labels = model.classify_text_batch('./dataset/weibo/zhoujielun.txt')
    # labels = model.classify_text('./dataset/weibo/zhoujielun.txt')
    print("Labels:", labels)
