# coding: utf-8
# @File: dataset.py
# @Author: HE D.H.
# @Email: victor-he@qq.com
# @Time: 2021/12/09 11:01:32
# @Description:

import numpy as np
from tqdm import tqdm
from torch.utils.data import Dataset

from torch.utils.data import Dataset
import numpy as np
from tqdm import tqdm
import multiprocessing


# 自定义CNewsDataset类，用于加载和处理新闻分类数据集
class CNewsDataset(Dataset):
    def __init__(self, filename, tokenizer):
        # 数据集初始化
        # 定义类别标签
        self.labels = ['体育', '娱乐', '家居', '房产', '教育', '时尚', '时政', '游戏', '科技', '财经']
        # 将类别标签转换为对应的索引
        self.labels_id = list(range(len(self.labels)))
        # 存储tokenizer（分词器），用于对文本进行处理
        self.tokenizer = tokenizer
        # 定义输入ID、token类型ID、注意力掩码和标签ID的存储列表
        self.input_ids = []
        self.token_type_ids = []
        self.attention_mask = []
        self.label_id = []
        # 加载数据并进行预处理
        self.load_data(filename)

    def load_data(self, filename):
        # # 加载数据
        # print('loading data from:', filename)
        # with open(filename, 'r', encoding='utf-8') as rf:
        #     lines = rf.readlines()  # 读取文件中的所有行，每一行表示一条数据
        lines = filename

        # tqdm 用于显示进度条，方便了解数据加载进度
        for line in tqdm(lines, ncols=100):
            # 假设数据的每一行格式为 "标签\t文本"
            label, text = line.strip().split('\t')
            # 根据标签名称找到标签对应的索引
            label_id = self.labels.index(label)
            # 使用分词器将文本转换为模型可接受的格式
            # add_special_tokens=True: 添加特殊的起始和结束标记
            # padding='max_length': 将输入填充到指定的max_length
            # truncation=True: 如果文本超过指定长度，则进行截断
            # max_length=512: 设定输入的最大长度为512
            token = self.tokenizer(text, add_special_tokens=True, padding='max_length', truncation=True, max_length=512)
            # 将分词后的结果存储到对应的列表中，转换为numpy数组方便后续使用
            self.input_ids.append(np.array(token['input_ids']))
            self.token_type_ids.append(np.array(token['token_type_ids']))
            self.attention_mask.append(np.array(token['attention_mask']))
            # 存储对应的标签索引
            self.label_id.append(label_id)

    def __getitem__(self, index):
        # 定义如何通过索引获取数据，这里返回的是模型的所有输入（input_ids, token_type_ids, attention_mask）以及对应的标签
        return self.input_ids[index], self.token_type_ids[index], self.attention_mask[index], self.label_id[index]

    def __len__(self):
        # 返回数据集的长度，即总共有多少条数据
        return len(self.input_ids)


from torch.utils.data import Dataset
import os
import numpy as np
from tqdm import tqdm


# # 自定义WeiboDataset类，用于加载和处理微博数据集
# class WeiboDataset(Dataset):
#     def __init__(self, data_dir, tokenizer):
#         # 数据集初始化
#         self.tokenizer = tokenizer
#         # 定义输入ID、token类型ID、注意力掩码的存储列表
#         self.input_ids = []
#         self.token_type_ids = []
#         self.attention_mask = []
#         # 加载数据并进行预处理
#         self.load_data(data_dir)
#
#     def load_data(self, data_dir):
#         # 加载数据
#         print('loading data from directory:', data_dir)
#         # 获取目录下所有.txt文件
#         files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.txt')]
#
#         # 使用多进程并行处理文件加载和预处理
#         with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
#             results = list(tqdm(pool.imap(self.process_file, files), total=len(files), ncols=100))
#
#         # 合并所有结果
#         for input_ids, token_type_ids, attention_mask in results:
#             self.input_ids.extend(input_ids)
#             self.token_type_ids.extend(token_type_ids)
#             self.attention_mask.extend(attention_mask)
#
#     def process_file(self, file):
#         input_ids = []
#         token_type_ids = []
#         attention_mask = []
#         with open(file, 'r', encoding='utf-8') as rf:
#             lines = rf.readlines()  # 读取文件中的所有行，每一行表示一条数据
#
#         for line in lines:
#             text = line.strip()
#             # 使用分词器将文本转换为模型可接受的格式
#             # add_special_tokens=True: 添加特殊的起始和结束标记
#             # padding='max_length': 将输入填充到指定的max_length
#             # truncation=True: 如果文本超过指定长度，则进行截断
#             # max_length=512: 设定输入的最大长度为512
#             token = self.tokenizer(text, add_special_tokens=True, padding='max_length', truncation=True, max_length=512)
#             # 将分词后的结果存储到对应的列表中，转换为numpy数组方便后续使用
#             input_ids.append(np.array(token['input_ids']))
#             token_type_ids.append(np.array(token['token_type_ids']))
#             attention_mask.append(np.array(token['attention_mask']))
#
#         return input_ids, token_type_ids, attention_mask
#
#     def __getitem__(self, index):
#         # 定义如何通过索引获取数据，这里返回的是模型的所有输入（input_ids, token_type_ids, attention_mask）
#         return self.input_ids[index], self.token_type_ids[index], self.attention_mask[index]
#
#     def __len__(self):
#         # 返回数据集的长度，即总共有多少条数据
#         return len(self.input_ids)


from torch.utils.data import Dataset
import numpy as np
from tqdm import tqdm


# 自定义WeiboDataset类，用于加载和处理微博数据集
class WeiboDataset(Dataset):
    def __init__(self, file_path, tokenizer):
        # 数据集初始化
        self.tokenizer = tokenizer
        # 定义输入ID、token类型ID、注意力掩码的存储列表
        self.input_ids = []
        self.token_type_ids = []
        self.attention_mask = []
        self.texts = []  # 用于存储原始文本
        # 加载数据并进行预处理
        self.load_data(file_path)

    def load_data(self, file_path):
        # 加载数据
        # print('loading data from file:', file_path)
        # with open(file_path, 'r', encoding='utf-8') as rf:
        #     lines = rf.readlines()  # 读取文件中的所有行，每一行表示一条数据
        lines = file_path
        for line in tqdm(lines, ncols=100):
            text = line.strip()
            self.texts.append(text)  # 存储原始文本
            # 使用分词器将文本转换为模型可接受的格式
            # add_special_tokens=True: 添加特殊的起始和结束标记
            # padding='max_length': 将输入填充到指定的max_length
            # truncation=True: 如果文本超过指定长度，则进行截断
            # max_length=512: 设定输入的最大长度为512
            token = self.tokenizer(text, add_special_tokens=True, padding='max_length', truncation=True, max_length=512)
            # 将分词后的结果存储到对应的列表中，转换为numpy数组方便后续使用
            self.input_ids.append(np.array(token['input_ids']))
            self.token_type_ids.append(np.array(token['token_type_ids']))
            self.attention_mask.append(np.array(token['attention_mask']))

    def __getitem__(self, index):
        # 定义如何通过索引获取数据，这里返回的是模型的所有输入（input_ids, token_type_ids, attention_mask）和原始文本
        return self.input_ids[index], self.token_type_ids[index], self.attention_mask[index], self.texts[index]

    def __len__(self):
        # 返回数据集的长度，即总共有多少条数据
        return len(self.input_ids)
