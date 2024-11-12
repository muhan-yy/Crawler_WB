# Crawler_WB: 微博爬虫脚本

## 项目介绍

本项目的目的是根据用于输入的信息（搜索关键词、起止时间限制）爬取博文多模态信息（文本、图片、视频）
Crawler_WB的功能如下：

- 多模态数据爬取（文本、图片、视频）
- 文本数据简单预处理（时间文本格式化、特殊符号筛减等）
- 冗余视频过滤（只保留画质最高的视频）
- 日志保存（爬取进度日志、报错日志等）

## 相关文件说明
### './code'文件夹

存放项目相关脚本、日志信息

#### py脚本文件说明
- 'getFromWeibo.py': Crawler_WB的主要执行脚本
- 'DataClean.py': 文本数据预处理脚本

#### text文件说明
- 'complete.txt': 存放爬取进度日志，每行信息包括：关键词、开始日期、截止日期、开始时间、截止时间、页数。在该txt文件中，我们给出了部分示例。
- 'imageError.txt': 当根据id获取对应图片时出现报错信息，则记录下该图片id，每行表示：当前id对应的所有图片的保存路径。在该txt文件中，我们给出了部分示例。

### './data'文件夹

存放爬取到的多模态数据（文本、图片、视频）

- './images': 存放图片数据，所有图片将根据其对应的博文id单独存放，存放的文件夹名为博文id
- './text': 存放当前时间范围内的所有博文的相关文本信息，所有信息存储在一个json文件中，json文件名为当前时间范围，例如：202406130-6.json表示存放2024年6月13号0点至6点内所有的博文的文本信息。
- './videos': 存放视频数据，所有视频将根据其对应的博文id单独存放，存放的文件夹名为博文id，每个视频的文件名为该视频的画质信息。