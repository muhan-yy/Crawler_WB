import os
import re
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
import nltk
from nltk.corpus import stopwords
#import jieba
import datetime

class DataClean():
    def __init__(self, divTime, startTime, endTime):
        self.time = divTime
        self.startTime = startTime
        self.endTime = endTime
    def clean_space(self, oriText):
        '''
        清除空格
        :return: 没有空格的文本
        '''
        #print("处理前的文本：" + self)
        content = oriText.replace(' ','')
        return content

    def clean_character(self, oriText):
        '''
        清除表情符号与空格
        :return: 只有数字、汉字、英文、常规句子符号的文本，且不符合要求的内容被替换成空字符
        '''
        pattern = re.compile("[^\u4e00-\u9fa5^,^.^!^a-z^A-Z^0-9]")  # 只保留中英文、数字和符号，去掉其他东西
        line = re.sub(pattern,'',oriText)
        content = ''.join(line.split())
        return content

    def clean_time(self):
        '''
        对时间进行格式化，处理一下三种类型
        47秒前
        57分钟前
        今天08:45
        06月30日 15:36
        2020年06月29日 22:51
        :return: 2021-7-1 8:24  类型的时间数据
        '''
        now = datetime.datetime.now()
        ymd = now.strftime('%Y-%m-%d')

        if self.time[-2:] == '秒前':
            self.time = now - datetime.timedelta(seconds=int(self.time[:-2]))
            return self.time.strftime('%Y-%m-%d %H:%M')
        elif self.time[-3:] == '分钟前':
            self.time = now - datetime.timedelta(minutes=int(self.time[:-3]))
            return self.time.strftime('%Y-%m-%d %H:%M')
        elif self.time[0:2] == '今天':
            self.time = str(ymd) + ' ' + self.time[2:]
            return self.time
        elif self.time[2] == '月':
            pattern = re.match('(\d+)月(\d+)日 (\d+):(\d+)', self.time)
            self_mou = pattern.group(1)
            self_d = pattern.group(2)
            self_h = pattern.group(3)
            self_min = pattern.group(4)
            self_year = datetime.datetime.now().year
            infoTime = str(str(self_year) + '-' + self_mou + '-' + self_d)
            infoTime = datetime.datetime.strptime(str(infoTime), "%Y-%m-%d")
            if infoTime >= self.startTime and infoTime <= self.endTime:
                return '{}-{}-{} {}:{}'.format(str(self_year),self_mou,self_d,self_h,self_min)
            else:
                return 'None'
        elif self.time[4] == '年':
            pattern = re.match('(\d+)年(\d+)月(\d+)日 (\d+):(\d+)',self.time)
            self_year = pattern.group(1)
            self_mou = pattern.group(2)
            self_d = pattern.group(3)
            self_hour = pattern.group(4)
            #infoTime = str(str(self_year) + self_mou + self_d + self_hour)
            #infoTime = datetime.datetime.strptime(str(infoTime), "%Y%m%d%h")
            if str(self_year) == '2024':
                return '{}-{}-{}-{}'.format(str(self_year), self_mou, self_d, self_hour)
            else:
                return 'None'

            '''
            if infoTime >= startTime and infoTime <= endTime:
                return '{}-{}-{}'.format(str(self_year), self_mou, self_d)
            else:
                return 'None'
            '''











