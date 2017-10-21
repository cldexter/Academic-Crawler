#  项目说明

该项目目标：
- 采用爬虫、自然语言处理、机器学习的办法，快速获取某领域关键论文（PubMed，ScienceDirect）
- 使用自动化脚本，追踪领域关键论文相关变化和趋势
- 采用人工智能分析 + 人工打分的办法，自动判断某篇论文“可用性”
------
1. 建立爬虫环境

`project.py  web.py  pmid_crawler.py detail_crawler.py  task.py  message.py`

* [x] 项目定时启动、终止
 * [x] 根据运行统计数据自动计算运行参数
* [x] 采用selenium + phantomjs方案解决js加载问题
 * [x] 页面解析采用lxml xpath、正则表达式，加快速度
* [x] 建立代理IP池，防止访问限制：自动抓取IP，储存，更新
* [x] 采用反反爬虫机制：换user agent，运行机制（夜间访问，随机间隔）
 * [x] 建立多线程爬虫
* [ ] 采用flask搭建可视化界面，通过网页对任务运行监控
* [ ] 采用云部署的mongoDB，实现任何地点的访问与同步
* [ ] 对运行情况做统计分析
* [ ] 对关键词产量进行统计分析并自动生成最优检索式
* [ ] 根据运行统计、关键词统计等信息，自动优化运行参数 

-----
2. 自动抓取PubMed上相关文献信息

`spider_pm.py journal.py institute.py`

* [x] 使用单线程phantomjs快速抓取pmid：每页200个，快速翻页
* [x] 使用多线程requests抓取：题目、期刊、年份、作者、机构、摘要、关键词、全文链接
* [x] 自动补齐：期刊影响因子、杂志分区信息；储存查询过的期刊信息
* [x] 自动提取：国家、大学、医院、校园、机构名称；储存查询过的机构信息
* [ ] 模糊查询，对机构名进行辨识，统计，归类同一机构
* [ ] 自动补齐：该机构在该领域排名：根据发表论文数量，分区占比等
* [ ] 部分关键论文查找引用率
-----
3. 通过模型生成自动文摘
* [ ] 根据信息和简单的模型计算论文的重要性（不含人工智能或机器学习）：作者（机构）、期刊（影响因子）、引用
* [ ] 根据关键词、摘要、期刊等判断文章类型：机制？医院数据收集？方法类？ 
* [ ] 高亮关键词，手动加入行业关键词

-----
5. 建立数据可视化界面

`data_wash.py`

* [x] 清理抓取的信息：去除所有标签；清除特殊字符或者非英文字母；合并段落，规范化数据结构
* [ ] 搜索关键词突出：包含本项目所涉及所有关键词；自定义关键词突出：自定义添加关注词，机构中国家、机构名突出
* [ ] 根据自然语言处理词频分析，自动添加高频关键词
* [ ] 根据需要使用jinja2生成MD，HTML静态文件
* [ ] 使用flask建立动态输出：索引页、阅读页面、鼠标控制自动标记（已读、未读、加星）
* [ ] 使用jquery将页面勾选的关键词及笔记返回到数据库
* [ ] 将阅读状况返回数据库：花了多少秒钟阅读？是不是真的阅读了
* [ ] 通过网页对项目、条目内容进行增删修改
-----
7. 使用自然语言处理对文章进行聚类分析
* [x] 文本清洗：停用词，词格，分词，大小写
* [x] 词频统计与向量分析
* [ ] 多文章聚类分析，找到代表性论文
 * [ ] 关键信息提取、自动文摘
-----
8. 深度学习模型建立：根据人工打分监督训练
* [ ] 人工搭建文本、期刊资质、团队资质、作者资质等与人工打分之间联系的模型
* [ ] 根据人工评分重新计算文章分数，重新排序
* [ ] 根据人工智能排出最重要的国家、机构、期刊等信息
-----
9. 阅读后人工评分、更新
* [ ] 人工多维度评论文章：主题相关度、文章质量、文章有用性、研究类型
* [ ] 人工选择论文分类
* [ ] 对重排的文章进行打分
* [ ] 手动添加关键词
-----  
10. 根据建立的模型，提供每篇文章有用性的可能性
