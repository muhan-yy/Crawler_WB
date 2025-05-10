# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 09:33:19 2024

@author: muhansay
"""

import requests
from bs4 import BeautifulSoup
import time 
import jieba
import re
import os
import json
import random
import datetime
from DataClean import DataClean
from urllib.parse import urlencode
from pyquery import PyQuery as pq

 
global keywords, start, end, startH, endH, fileName, Cookies, reCountMax, keywords_succ, keywords_error
# 已完成的关键词
complete = [    
    ]
# 待爬取的关键词
keywords = ['防潮', '防范措施', '防寒', '防洪工程', '防水', '防锈', '防汛', 
        '防汛措施', '防汛措施落实', '防汛工作', '防汛抗洪', '防汛抢险', '防汛抢险工作', '防汛指挥', '防御',
        '防灾', '风暴', '风起云涌', '风霜雨雪', '高处',   '高温','高温洪水', '海','海洋', '河堤', '河流', 
        '洪', '洪峰', '洪涝', '洪流', '洪水', '洪灾', '哗哗', '哗啦', 
          '哗啦啦', '检修','紧急', '紧急救援', 
            '紧急情况处理', '紧急疏散', '紧急疏散预案', '紧急通知', '紧急应对', '紧急预警', '警报', '警戒', '救援',
            '抗洪救灾', '狂飙', '狂风暴雨', '来势汹汹', '涝', '雷暴', '雷厉风行', '雷霆万钧','雷雨','雷阵雨', '梅雨',
            '内涝', '溺水', '排涝', '气势汹汹', '气象变化',  '气象变化预警', '气象台', '气象预警', '强风',
            '抢险', '抢修', '秋雨', '如火如荼', '塞车', '山洪', '山洪暴发', '上涨', '涉水', '疏散', '水坝', '水库', 
            '水库泄洪', '水利', '水利工程', '水漫金山', '水位', '水文数据', '水源', '水灾', '水涨船高', '水资源保护', 
            '损害评估', '台风', '台风袭击', '太阳雨',  '天崩地裂',  '天灾',   '停产', '停电', '停工', '停课', '退票', 
            '晚点', '危机', '危险', '危险区域', '维修', '误点', '熄火', '险情通报', '小到中雨', '小至中雨', '泄洪', 
            '汹涌澎湃', '淹没', '淹水', '延误', '阴雨', '应对策略', '应急处理', '应急管理', '应急情况', '应急响应', 
            '应急响应机制', '应急预案','应急预案制定', '拥堵', '雨', '雨雪', '预案', '预测',  '预测模型', '预警', 
            '灾害', '灾情', '灾情处置', '灾情通报', '长途跋涉', '涨', '涨水', '中到大雨','中雨', 
            '暴风雨', '暴风骤雨','暴雨', '暴雨过程',  '暴雨过后','暴雨洪水袭击', '避险', '飚', '波涛汹涌', '沧海',
            '潺潺', '撤离', '春雨','大暴雨', '大风', '大风大浪', '大水', '大肆', '大修', '大洋','堤防', '多发地区', '泛滥成灾',   ]
keywords_succ = []
keywords_error = {}

# 发文时间段
start = '20240613'  # 开始 年月日
end = '20240613'    # 终止 年月日
startH = '0'        # 开始时间 0点
endH = '6'          # 终止时间 6点
fileName = start + startH + '-' + endH

# 获取cookie的测试链接：https://s.weibo.com/weibo?q=%E9%AB%98%E6%B8%A9&Refer=index&page=2&timescope=custom%3A2020-06-15-10%3A2020-06-15-12
# 存放用于爬取正文的 cookie
Cookies = [
    ]

reCountMax = len(Cookies)

# 获取cookie的测试链接：https://weibo.com/tv/show/1034:4515742994071586
# 存放用于爬取视频的 cookie
vedioCookies = [
    ]


def getImage(weiboId, imageDiv):
    '''
    # 根据博文id weiboId 获取当前博文中的图片
    params:
        weiboId: 博文id
    '''
    
    
    url = "https://m.weibo.cn/detail/"+str(weiboId)

    response = requests.get(url)
    # 使用正则表达式匹配包含 pic_ids 的部分
    pattern = re.compile(r'"pic_ids":\s*\[([^\]]*)\]')

    # 在响应文本中搜索匹配的内容
    match_test = pattern.search(response.text)
    # if len(match_test.group())
    if pattern.search(response.text) != None:
        match = match_test
    else:
        match_text = imageDiv.attr('action-data')
        pattern = re.compile(r'.+pic_ids=(.+)')
        match = pattern.search(match_text)
    
    # 判断当前博文中是否存在图片
    matchItem_length = len(match.group(1).split(','))
    print(matchItem_length)
    if match and matchItem_length>0:
        # 获取匹配的内容
        pic_ids_str = match.group(1)

        # 使用逗号分隔的值拆分为列表
        pic_ids_list = pic_ids_str.split(',')

        # 去除每个元素两侧的空格和引号
        pic_ids_list = [re.sub(r'\s|"', '', pic_id) for pic_id in pic_ids_list]

        # 创建保存图片的文件夹
        if not os.path.exists(os.path.join(".","data","images",str(weiboId))):
            os.makedirs(os.path.join(".","data","images",str(weiboId)))
        for data, ID in zip(pic_ids_list, list(range(len(pic_ids_list)))):
            if len(data) == 0:
                continue
            time.sleep(0.5)
            imageTypes = ['.jpg', '.png', '.jpeg']
            for imageType in imageTypes:
                img_url = f"https://wx3.sinaimg.cn/large/{data}{imageType}"
                # 发送请求获取图片数据
                response = requests.get(img_url)
                image = response.content
                if type(image) != bytes:
                    with open('./code/imageError.txt', 'a', encoding='GB18030') as f:
                        #print(weiboId)
                        f.write(str(weiboId) + '\t' + data + '\n')
                        continue
                imageSize = len(image)
                if imageSize < 100:
                    continue
                else:
                    # 构建保存路径
                    imageFilePath = os.path.join(".", "data", "images", str(weiboId), f"{str(ID)}.jpg")
                    # 保存图片
                    with open(imageFilePath, 'wb') as f:
                        f.write(image)
                    break

    else:
        #未找到包含图片ID的内容
        with open('./code/imageError.txt', 'a', encoding='GB18030') as f:
            f.write(str(weiboId) + '\n')

def keep_largest_video(folder_path):
    '''
    # 保留文件夹中画质最高的视频
    params:
        folder_path: str, 所要检查的文件夹路径
    '''

    # 遍历文件夹
    for root, dirs, files in os.walk(folder_path):
        # 子文件夹中的视频文件列表
        video_files = [f for f in files if f.endswith('.mp4') or f.endswith('.avi')]
        if not video_files:
            continue  # 如果子文件夹中没有视频文件，则继续下一个子文件夹

        # 找到子文件夹中内存大小最大的视频文件
        largest_video = max(video_files, key=lambda f: os.path.getsize(os.path.join(root, f)))

        # 删除子文件夹中除了内存大小最大的视频文件之外的其他视频文件
        for file in video_files:
            if file != largest_video:
                os.remove(os.path.join(root, file))

def getVideo(videoUrl, weiboId, cookie):
    '''
    # 根据视频网页url 获取各分辨率的视频，并根据博文id weiboId 存储
    params:
        videoUrl: str, 所要获取的视频的url
        weiboId: str, 所属的微博id
        cookie: str, 所需的cookie
    '''

    videoId = re.findall('https://weibo.com/tv/show/(\d*:\d*)?.*',videoUrl)[0]
    url = 'https://weibo.com/tv/api/component?page=/tv/show/{0}&data={1}'
    data_str = '{%22Component_Play_Playinfo%22:{%22oid%22:%22' + videoId + '%22}}'
    url = url.format(videoId, data_str)
    headers = {
        "cookie": cookie,
        "origin": "https://weibo.com",
        "page-referer": "/tv/show/1034:4515742994071586",
        "referer": "https://weibo.com/tv/show/1034:{}?mid={}".format(videoId, weiboId),
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }
    try:
        rsp = requests.post(url=url, headers=headers)
        dict2 = json.loads(rsp.text)
        urls_dict = dict2['data']['Component_Play_Playinfo']['urls']
    except:
        print("!"*10 + weiboId + "!"*10)
    
    if len(urls_dict) > 0:
        vedioParentFile = os.path.join('.', 'data', 'videos', weiboId)
        if not os.path.exists(vedioParentFile):
            os.makedirs(vedioParentFile)
        for key,value in urls_dict.items():
            # 遍历各分辨率的视频，获取其画质类型、url
            file_path = os.path.join(vedioParentFile, key + '.mp4')    
            vedio_url = "https:" + value # 当前画质的视频链接
            response = requests.get(vedio_url).content
            with open(file_path, 'wb') as file:
                file.write(response)
                
        # 只保留画质最高的视频
        # keep_largest_video(vedioParentFile)

def getPageInfo(keyword, page, startTime, endTime, header):
    '''
    # 根据搜索内容返回当前页的内容
    params:
        keyword: str, 搜素关键词
        page: int, 页码
        startTime: datetime, 开始时间
        endTime: datetime, 结束时间
        header: dict, 头信息
    '''
    startT = str(startTime).split(' ')[0] + '-' + startH
    endT = str(endTime).split(' ')[0] + '-' + endH
    params = {
        'q': keyword,
        'Refer': 'index',
        'page': str(page),
        'timescope': 'custom:' + startT + ':' + endT
    }
    url = 'https://s.weibo.com/weibo?' + urlencode(params)
    try:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            return response.text,url
    except requests.ConnectionError: 
        return None,url

def save2CSV(data):
    '''
    # 数据存储
    params:
        data: list, 所要存储的数据
    '''
    csvName = './data/text/' + fileName + '.csv'
    with open(csvName,'a+',encoding='GB18030') as csvfile:
        csvfile.write(str(data) + '\n')

def save2Json(dataDict):
    '''
    # 数据存储到指定json文件
    params:
        dataDict: dict, 所需存储的数据
    '''

    fileName = start + startH + '-' + endH
    jsonFile = './data/text/' + fileName + '.json'
    
    # 创建空json文件
    if not os.path.exists(jsonFile):
        with open(jsonFile, 'w', encoding='gb18030') as file:
            file.write('{}')
    
    with open(jsonFile, 'r', encoding='gb18030') as fr:
        dataOri = json.load(fr)
    dataOri[len(dataOri)] = dataDict
    with open(jsonFile, 'w', encoding='gb18030') as fw:
        json.dump(dataOri, fw, indent = 4, ensure_ascii=False)

def getPageNum(keyword, page, startTime, endTime, header, numOri):
    '''
    # 根据搜索内容获取总页数
    params:
        keyword: str, 搜索关键词
        page: int, 页码
        startTime: datetime, 开始时间
        endTime: datetime, 结束时间
        header: dict, 头信息
        numOri: int, 原始的页数
    '''

    time.sleep(0.8)  # 挂起进程一秒
    html,url = getPageInfo(keyword,page,startTime,endTime,header)

    try:
        doc = pq(html)
    except:
        print('!'*10 + '获取总页数有问题' + '!'*10)
        return 
    pagesDivs = doc("div[class='m-page']").items()
    for pagesDiv in pagesDivs:
        pagesUl = pagesDiv.find('ul')('.s-scroll')
        pagesLi = pagesUl.find('li')
        return len(pagesLi)

def getDiscuss(weiboId, page, cookie, max_id=0):
    '''
    # 根据博文id 获取评论内容
    params:
        weiboId：str, 博文id
        page：int, 当前评论页
        max_id：int, 标识最后一个讨论内容的编号，当为0时表示遍历了所有评论，默认为0
    '''
    
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": cookie,
        "Mweibo-Pwa":"1",
        #"Host": "s.weibo.com",
        "Referer": "https://m.weibo.cn/detail/" + str(weiboId),
        "Sec-Ch-Ua":'"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        "Sec-Ch-Ua-Mobile":"?0",
        "Sec-Ch-Ua-Platform":'"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    # 原始 评论内容 header备份
    # headers = {
    #     "Accept": "application/json, text/plain, */*",
    #     "Accept-Encoding": "gzip, deflate, br, zstd",
    #     "Accept-Language": "zh-CN,zh;q=0.9",
    #     "Connection": "keep-alive",
    #     "Content-Type": "application/x-www-form-urlencoded",
    #     "Cookie": cookie,
    #     "Mweibo-Pwa":"1",
    #     #"Host": "s.weibo.com",
    #     "Referer": "https://m.weibo.cn/detail/" + str(weiboId),
    #     "Sec-Ch-Ua":'"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    #     "Sec-Ch-Ua-Mobile":"?0",
    #     "Sec-Ch-Ua-Platform":'"Windows"',
    #     "Sec-Fetch-Dest": "empty",
    #     "Sec-Fetch-Mode": "cors",
    #     "Sec-Fetch-Site": "same-origin",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    #     "X-Requested-With": "XMLHttpRequest",
    # }
    
    if page == 1:
        url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'.format(weiboId,weiboId)
    else:
        if max_id != 0:
            url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0&max_id={}'.format(weiboId,
        	                                                                                        weiboId,
        	                                                                                        max_id)
    r = requests.get(url, headers = headers)
    
    discussInfo = []
    if r.status_code == 200:
        try:
            max_id = r.json()['data']['max_id'] # 用于遍历所有的评论内容
            discussItems = r.json()['data']['data']
            for discussItem in discussItems:
                dr = re.compile(r'<[^>]+>', re.S) # 过滤评论内容
                discussText = dr.sub('', discussItem['text']) # 评论内容
                discussLikeCount = discussItem['like_count'] # 评论点赞数
                
                # 评论者信息
                discussUserName = discussItem['user']['screen_name'] # 评论者姓名
                discussUserId = discussItem['user']['id'] # 评论者id
                discussUserIdFollowCount = discussItem['user']['follow_count']  # 评论者关注数
                discussUserIdFollowersCount = discussItem['user']['followers_count']  # 评论者粉丝数
                
                discussInfo.append([discussText, discussLikeCount, discussUserName, discussUserId,
                                    discussUserIdFollowCount, discussUserIdFollowersCount])
        except:
            max_id = 0
    
    return discussInfo, max_id

def dealError(keyword, page, fileName, startTime, endTime, header, reCount):
    '''
    # 处理爬虫报错，修改header信息，重新爬取
    params:
        keyword: str, 搜索关键词
        page: int, 页码
        fileName: str, 存储的文件名
        startTime: datetime, 开始时间
        endTime: datetime, 结束时间
        header: dict, 头信息
        reCount: int, 重试次数
    '''
    
    reCount += 1
    try:
        header = changeHeader(Cookies)
        getContent(keyword, page, fileName, startTime, endTime, header, reCount)
    except:
        print("!"*10 + "处理爬虫报错" + "!"*10)
        reCount += 1
        header = changeHeader(Cookies)
        time.sleep(0.6)
        if reCount < reCountMax:
            dealError(keyword, page, fileName, startTime, endTime, header, reCount)

def changeHeader(Cookies):
    '''
    # 修改header信息，并返回
    params:
        Cookies: list, 存储的cookies
    '''
    
    Cookie = Cookies[random.randint(0,len(Cookies)-1)]
    header = {
        "authority":"s.weibo.com",
        "method":"GET",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control":"max-age=0",
        "Cookie": Cookie,
        "Referer": "https://s.weibo.com/weibo?q=%E6%9A%B4%E9%9B%A8&Refer=index",
        "Sec-Ch-Ua":'', # 待填入
        "Sec-Ch-Ua-Mobile":"?0",
        "Sec-Ch-Ua-Platform":'"Linux"',
        "Sec-Fetch-Dest":"document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "",   # 待填入
    }

    return header

def getContent(keyword, page, fileName, startTime, endTime, header, reCount):
    '''
    # 爬取页面相关信息
    params:
        keyword: str, 搜索关键词
        page: int, 页码
        fileName: str, 存储的文件名
        startTime: datetime, 开始时间
        endTime: datetime, 结束时间
        header: dict, 搜索头
        reCount: int, 重试次数
    '''
      
    assert reCount < reCountMax
    
    print("-"*10 + "执行 getContent" + '-'*10)
    time.sleep(0.4)
    html, url = getPageInfo(keyword, page, startTime, endTime, header)
    
    try:
        doc = pq(html)
    except:
        print('!'*10 + "获取页面信息时报错--1" + '!'*10) # 正文 cookie 有问题 Cookies
        if reCount < reCountMax:
            dealError(keyword, page, fileName, startTime, endTime, header, reCount)
        else:
            with open('./code/urlError.txt', 'a', encoding='gb18030') as f:
                f.write(keyword + '\t' + str(startTime) + '\t' + str(endTime) + '\t' + str(page) + '\n')
            
    if doc.find('div.card-wrap'):
        divItems = list(map(pq, doc('div.card-wrap')[:-1]))
        
        for item in divItems:
            
            weiboId = item.attr('mid')
            if weiboId == None:
                weiboId = 'None'
            else:
                imageDiv = item('div.media.media-piclist') # 图片Div
                #videoDiv = doc('div.media.media-video-a') # 视频Div
                videoDiv = item('div.thumbnail') # 视频Div
            
                # 获取图片
                if len(imageDiv) > 0:
                    getImage(weiboId, imageDiv)

                # 获取视频
                if len(videoDiv) > 0:
                    videoCookie = vedioCookies[random.randint(0, len(vedioCookies)-1)]
                    #print('获取视频')
                    patternVideo = re.compile(r'address:\s.*fid=(.*)\',.*')
                    match = patternVideo.search(videoDiv.outer_html())
                    if match:
                        videoUrl = "https://weibo.com/tv/show/" + match.group(1)
                        getVideo(videoUrl, weiboId, videoCookie)
                
            # 存储某个博文的相关信息
            allInfo = {"author":'', "comment":'', "loc":'', "dateTime":'', "trans":0,
                       "discuss":0, "praise":0, "weiboId":'', "discussInfo":[], "transInfo":[]}
            
            # 昵称 author
            try:
                info = item('a.name')
                nickName = info.attr('nick-name')
                if nickName == ' ':
                    author = 'None'
                else:
                    author = nickName
            except:
                print('!' * 10 + '获取昵称报错' + '!'*10)
                author = 'None'

            # 用户定位信息 loc
            loc = ''
            locP = item("p[node-type='feed_list_content']")
            if len(locP) > 0:
                if locP.find('a').find('i.wbicon').text() == '2':
                    loc = locP.find('a').text().split('2')[-1]

            # 博文内容 comment
            commentP = item('p.txt:first')
            comment = commentP.text()
            if commentP.find('a') and commentP.find('a').find('i.wbicon').text() == '2':
                # 删除正文中的 定位信息
                comment = comment.replace(commentP.find('a').find('i.wbicon').parent().text(), '')
            comment_jieba = jieba.lcut_for_search(comment) 
           
            # 发文日期 dateTime
            try:
                dateTime = item('div.from')('a').eq(0).text()
                dc = DataClean(str(dateTime), startTime, endTime)
                dateTime = str(dc.clean_time())
            except:
                print('!'*10 + '发文日期报错' + '!'*10)
                dateTime = 'None'
            
            # 转发数trans  评论数discuss  点赞数praise
            forwards = item("div.card-act").find('li').items()
            for i, forward in enumerate(forwards):
                num = re.sub("\D", "", forward.text())
                if num == '':
                    num = 0
                else:
                    num = int(num)
                if i == 0:
                    trans = num  # 转发数
                elif i == 1:
                    discuss = num  # 评论数
                elif i == 2:
                    praise = num  # 点赞数
            allInfo['author'] = author
            allInfo['comment'] = comment
            allInfo['loc'] = loc
            allInfo['dateTime'] = dateTime
            allInfo['trans'] = trans
            allInfo['discuss'] = discuss
            allInfo['praise'] = praise
            allInfo['weiboId'] = weiboId
        
            # 评论内容
            if discuss > 0:
                _page = 1
                cookie = header['Cookie']
                
                discussInfo = [] # 存储所有讨论信息
                
                # 获取第page页的讨论信息，此时page为1
                discussInfo_page, max_id = getDiscuss(weiboId, _page, cookie, max_id=0)
                discussInfo += discussInfo_page
                # 判断是否需要获取讨论，即max_id是否为0
                while max_id != 0:
                    _page += 1
                    discussInfo_page, max_id = getDiscuss(weiboId, _page, cookie, max_id=max_id)
                    discussInfo += discussInfo_page
                discussInfo = list(map(list, set(map(tuple, discussInfo)))) # 去重
                allInfo['discussInfo'] = discussInfo
                
                
            # 转发的内容transComment 转发博文的id transWeiboId
            transDiv = item.find('div')('.card-comment')
            transComment = ''
            transWeiboId = ''
            
            if len(transDiv) > 0:
                transComment = transDiv('p.txt:last').text()
                imageDiv = transDiv("div.media.media-piclist")
                if len(imageDiv) > 0:
                    pattern = re.compile(r'.*mid=(.*)&pic_ids.*')
                    match = pattern.search(imageDiv.attr('action-data'))
                    if match:
                        transWeiboId = match.group(1)
                        getImage(transWeiboId)
            allInfo['transInfo'] = [transComment, transWeiboId]

            # 存储信息
            if str(dateTime.split('-')[0]) == "2024":
                save2Json(allInfo)   
                print('-'*10 + '存储成功' + '-'*10)
            else:
                with open('./code/url.txt', 'a+') as f:
                    f.write(url + '\n')
        with open('./code/complete.txt', 'a', encoding='gb18030') as fc:
            fc.write(keyword + '\t' + start + '\t' + end + '\t' + startH + '\t' + endH + '\t' + str(page) + '\n')
    else:
        print('!'*10 + "获取页面信息时报错--2" + '!'*10)
        if reCount < reCountMax:
            dealError(keyword, page, fileName, startTime, endTime, header, reCount)
        else:
            with open('./code/urlError.txt', 'a', encoding='gb18030') as f:
                f.write(keyword + '\t' + str(startTime) + '\t' + str(endTime) + '\t' + str(page) + '\n')
        
def getAllInfo(keyword, Cookies, reCount):
    '''
    # 在getContent函数基础上进行分装
    params:
        keyword: str, 搜索关键词
        Cookies：list, Cookie集
        reCount：int, 重试次数
    '''
    
    fileName = 'weibo' + start + '-' + end
    #num = 35  # 爬取页数

    startTime = datetime.datetime.strptime(str(start), "%Y%m%d")
    endTime = datetime.datetime.strptime(str(end), "%Y%m%d")

    header = {
        "authority":"s.weibo.com",
        "method":"GET",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control":"max-age=0",
        "Cookie": Cookies[random.randint(0,len(Cookies)-1)],
        "Referer": "https://s.weibo.com/weibo?q=%E6%9A%B4%E9%9B%A8&Refer=index",
        "Sec-Ch-Ua":'', # 待填入
        "Sec-Ch-Ua-Mobile":"?0",
        "Sec-Ch-Ua-Platform":'"Linux"',
        "Sec-Fetch-Dest":"document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "",    # 待填入
    }
    
    # 获取爬取页数，默认50页
    numDefault = 50 
    num = None
    try:
        num = getPageNum(keyword, 1, startTime, endTime, header, numOri=numDefault)
    except:
        print('!'*10 + 'getAllInfo中获取总页数报错' + '！'*10)
        for i in range(5):
            header = changeHeader(Cookies)
            num = getPageNum(keyword, 1, startTime, endTime, header, numOri=numDefault)
            if num != None:
                break
    if num == None:
        num = numDefault
        
    startT = str(startTime.year) + '-' + str(startTime.month) + '-' + str(startTime.day)
    endT = str(endTime.year) + '-' + str(endTime.month) + '-' + str(endTime.day)
    if str(num) != 'None':
        for page in range(0,num + 1):
            print('第',page,'页')
            try:
                time.sleep(0.4)
                getContent(keyword, page, fileName, startTime, endTime, header, reCount)
            except AttributeError:
                print("外部：捕获到AttributeError") # 视频 cookie有问题  vedioCookies
                header = changeHeader(Cookies)
                print('#' * 10, 'Header已更换', '#' * 10)
                time.sleep(1)
                reCount += 1
                if reCount < reCountMax:
                    dealError(keyword, page, fileName, startTime, endTime, header, reCount)
            except:
                print("外部：捕获到错误")
                header = changeHeader(Cookies)
                print('#' * 10, 'Header已更换', '#' * 10)
                time.sleep(1.2)
                reCount += 1
                if reCount < reCountMax:
                    dealError(keyword, page, fileName, startTime, endTime, header, reCount)
        
def main(keyword):
    time.sleep(0.6)
    reCount = 0
    getAllInfo(keyword, Cookies, reCount)
    
if __name__=="__main__":
    for keyword in keywords:
        main(keyword)
