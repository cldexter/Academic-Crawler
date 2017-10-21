# 定义所有数据格式

-----
## 数据库格式如下：

### 项目（project）：
- 项目名称(project)：字符串
- 项目描述（description）：项目描述，字符串
- 项目检索式（sstr)：用于检索项目的字符串，列表
- 项目生成日期（ctime）：项目生成的时间，时间
- 项目状态（status）：项目现在是否还运行，0=不运行，1=运行

### 搜索条目（sstr）
- 项目名称（project）：字符串
- 搜索条目（sstr）：搜索字符串，字符串
- 搜索条目生成时间（ctime）：时间
- 搜索条目类型（type）：可以是关键词key_word, 也可以是expression两种
- 任务循环类型（loop）：生成任务周期，实际定义了。0=不循环，1=指定循环小时，2=自动安排循环：根据产率，多久能抓至少一个来计算；默认选1
- 任务循环间隔（frequency）：如果是制定循环，任务运行间隔，每多少小时运行一次，单位为小时，浮点数；默认24小时

### pmid（pmid）
- 项目名称（project）
- 搜索检索式（sstr）
- 采集时间（ctime）
- 任务名称（task）
- pmid值（pmid）


### 论文记录（content）：论文记录
- 项目名称（project）：与运行项目名保持一致，字符串
- 搜索检索式（sstr）：搜索使用的关键词或者检索式，字符串
- 采集时间（ctime）：运行时间，如先抓sum再抓abstract，抓到abstract后更新
- 记录状态（status）：统一便于调取。1=第一轮抓取pmid，2=已补充完整，3-10保留（自然语言处理），11=已输出，12=已阅读，13=已完整评价，14-20保留（人工智能），整数
- 来源（source）：文章来源于何处，pubmed = “pm”，字符串
- pmid（pmid）： pmid，整数

- 标题（title）：文章标题，字符串
- 作者（author）：为简化统一用单数，列表
- 期刊（journal）：名称必须是在线搜索返回的标准名称（直接抓下来的不算），字符串
- 期刊正式名称（ojournal）：通过搜索返回的名字，字符串
- 影响因子（if）：通过在线搜索获取，浮点数
- 期刊分区（jzone）：期刊中科院分区，整数
- 年份（issue）：只记录年份，不考虑出版时间，整数
- 摘要（abstract）：即abstract，字符串
- 关键词（keyword）：关键词，列表
- 机构名（institue)：机构名，列表
- 第一机构排名（irank）：第一个机构的世界排名（尚未找到靠谱材料）
- 机构国家（country）：机构国家，列表
- 全文链接（flink）：全文链接，列表

- 文章有用性评分(usability)：本论文是不是自己想要的？是否可用？是否需要更多类似的？整数 1-5
- 与项目相关性评分(relativeness)：对本论文“是否是设置检索式时说想要的”进行评分，整数 1-5
- 文章质量评分(quality)：对本论文质量是否高进行总体评分，需要看全文，整数 1-5
- 标注（highlight）：在论文中用鼠标高亮的语句或关键词，字符串列表
- 笔记（comment）：自己写的笔记


### 日志（log）：
- 任务名称（task）：该项目下哪个任务，可以留空
- 日志生成时间（ctime）：消息生成时间
- 日志类型（logtype）：日志类型，字符串
- 日志信息（loginfo）：日志内容，字符串
    

### 任务（task）：
- 任务针对项目名称（project）：需要运行的项目
- 任务针对的sstr：字符串
- 任务名称（task）：即时间戳
- 任务生成时间（ctime）：ctime
- 任务运行状态（status）：0=未运行，1=已运行（含失败）
- 抓取论文条目（itemnum）：本次任务指定最多抓取量，整数；逻辑判断得出
- 抓取论文最大时间（mrhours）：最多运行多久，小时数，浮点数；默认8小时
- 是否提前终止：（endwith）：任务如何提前结束，整数。 0=不提前终止（运行到最大条目、所有条目或最多时间终止）1=自动提前终止


### 杂志(journal):
- 杂志全名（journal）：杂志全名
- 杂志影响因子(if)：杂志影响因子
- 杂志分区（jzone）：中科院分区


### 作者（author）:
- 英文名（name）：作者全名，以姓，逗号，名的方法，如 Chen，Long
- 英文名缩写（sname）：发表时的缩写 L Chen
- 机构（institute)：作者第一单位
----
## 其它变量格式

### 代理（proxy）：
- 生成时间（ctime）[0]
- 代理地址（proxy）[1]
- 最大使用量（max_used）[2]
- 最多失败次数（max_tried）[3]
- 最多连续失败次数（max_c_tried）[4]
- 

### 代理抛弃逻辑
- 大于最大使用量抛弃
- 


### 信息（message）:
- 

### message_type: 信息类型
- info(5) = 普通信息，最基本运行情况，
- sum(4) = 总结信息，运行一段时间的总结
- notice(3) = 提醒信息，在容错范围内，如“浏览器又重启了”
- error(2) = 错误信息，出现的小错误，导致某一步失败，比如某篇具体文章存取失败 
- important(1) = 重要信息，致命错误，导致程序不能进行

### stats_infotype: 统计信息类型
- succ = 成功
- fail = 失败
- skip = 跳过
- proc = 处理

### alert_type: 弹出信息类型
- notice = 提醒
- warning = 警告信息

### display_protocol：显示（包括屏幕或者网页）
- 0 = 不显示任何信息
- 1 = 只显示重要信息
- 2 = 显示错误信息、提醒信息及总结信息
- 9 = 显示所有信息

### log_protocol: 记录日志
- 0 = 不记录任何信息
- 1 = 只记录重要信息
- 2 = 记录重要信息、提醒信息及总结信息
- 9 = 记录所有信息

### 记录语句说明
- 抓取记录成功显示 "retrieved record: 23456789; total retrieved: 1000" info
    - log "retrieve record: 23456789"
- 抓取记录跳过显示 "skipped record: 23456789; total skipped: 300" info
    - log "skip record: 23456789" 
- 抓取记录失败重试显示 "retrying record: 23456789; 2 tries left" notice
    - log "retry record: 23456789"
- 抓取记录最终失败显示 "retrieve record failed: 23456789" error
    - log "fail record: 23456789"
- 抓取sp成功显示（direct） "loaded: NO.2 sum page (requests); total page loaded: 100" info
    - log "load sum page: NO.1 (requests)"
- 抓取sp成功显示（phantomjs） "loaded: NO.2 sum page (phantomJS); total page loaded: 100" info
    - log "load sum page: NO.2 (phantomjs)"
- 抓取sp失败重试显示 "load retrying: NO.2 sum page (requests); 2 tries left" notice
    - log "retry sum page: NO.2 (phantomjs)"
- 抓取sp最终失败显示 "load failed: NO.2 sum page (phantomJS)" error
    - log "fail sum page: NO.2 (phantomjs)"
- 液面数字更改 "max sum page changed: 23" notice
    - log "max sum page changed: 23"

### 任务生成逻辑
- 任务生成的工作24小时运行一次，每个词条对应一个任务，两个任务之间间隔5分钟
- 任务生成频率以sstr第二次开始的7日平均产率计算：确保一天至少1个，最多不超过7日
- 生成的任务中：
    - 抓取数量以sstr为单位，sstr第一次运行5000，第二次开始20
    - 最大抓取时间以sstr为单位，sstr第1次运行8小时，2次开始5分钟
    - 是否提前终止以project为单位，项目有1个sstr不提前终止，2个开始自动提前终止


### 任务自动提前终止逻辑：遇到如下情况，任务自行结束
- 连续40个pmid已存在
    
