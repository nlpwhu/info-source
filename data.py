#!/usr/bin/python3
#-*-coding:utf-8 -*-

REGION = [{"region":"0", "regionname":"国内"},
          {"region":"11","regionname":"北京市"},
          {"region":"12","regionname":"天津市"},
          {"region":"13","regionname":"河北省"},
          {"region":"14","regionname":"山西省"},
          {"region":"15","regionname":"内蒙古"},
          {"region":"21","regionname":"辽宁省"},
          {"region":"22","regionname":"吉林省"},
          {"region":"23","regionname":"黑龙江省"},
          {"region":"31","regionname":"上海市"},
          {"region":"32","regionname":"江苏省"},
          {"region":"33","regionname":"浙江省"},
          {"region":"34","regionname":"安徽省"},
          {"region":"35","regionname":"福建省"},
          {"region":"36","regionname":"江西省"},
          {"region":"37","regionname":"山东省"},
          {"region":"41","regionname":"河南省"},
          {"region":"42","regionname":"湖北省"},
          {"region":"43","regionname":"湖南省"},
          {"region":"44","regionname":"广东省"},
          {"region":"45","regionname":"广西省"},
          {"region":"46","regionname":"海南省"},
          {"region":"50","regionname":"重庆市"},
          {"region":"51","regionname":"四川省"},
          {"region":"52","regionname":"贵州省"},
          {"region":"53","regionname":"云南省"},
          {"region":"54","regionname":"西藏"},
          {"region":"61","regionname":"陕西省"},
          {"region":"62","regionname":"甘肃省"},
          {"region":"63","regionname":"青海省"},
          {"region":"64","regionname":"宁夏回族自治区"},
          {"region":"65","regionname":"新疆"},
          {"region":"97","regionname":"亚洲"},
          {"region":"98","regionname":"欧洲"},
          {"region":"99","regionname":"北美洲"}]

GROUP = [{"sourcegroup":1,"name":"汽车"},
         {"sourcegroup":-1,"name":"其他"}]

LEVEL = [{"level":1, "name":"境外英文"},  
         {"level":2, "name":"境外中文"},  
         {"level":3, "name":"国内中央"},  
         {"level":4, "name":"国内省级"},  
         {"level":5, "name":"国内地方"}]

TYPE = [
{"type":1 , "name":"新闻"},
{"type":2 , "name":"社区"},
{"type":3 , "name":"微博"},
{"type":4 , "name":"博客"},
{"type":5 , "name":"电子报刊"},
{"type":6 , "name":"Twitter"},
{"type":7 , "name":"微信"},
{"type":8 , "name":"学术"},
{"type":9 , "name":"视频"},
{"type":10, "name":" 问答"},
]

COLUMN = {
"要闻",
"新闻",
"理论",
"图片",
"国内",
"国际",
"专题",
"四平",
"高层",
"论坛",
"汽车",
"房产",
"体育",
"报道",
"教育",
"数码",
"农业",
"文娱",
"健康",
"酒店",
"旅游",
"心理",
"风采",
"时评",
"时政",
"论坛",
"视频",
"法制",
"房地产",
"财富",
"家居",
"城市",
"资讯",
"军事",
"台湾",
"评论",
"图片",
"视频",
"纪实",
"播客",
"军情",
"财经",
"股票",
"理财",
"娱乐",
"明星",
"电影",
"科技",
"数码",
"体育",
"NBA",
"汽车",
"车型",
"旅游",
"时尚",
"健康",
"亲子",
"历史",
"文化",
"读书",
"原创",
"教育",
"博报",
"论坛",
"公益",
"佛教",
"听书",
"房产",
"家居",
"城市",
"游戏",
"创新",
"出国",
"节目表",
"主持人",
"大学问",
"在人间",
"大事件",
"领秀圈",
"图说新闻",
"咋回事",
"人物",
"聚焦",
"热追踪",
"大参考",
"自由谈",
"观世变",
"年代访",
"纵议院",
"资讯首页",
"即时",
"大陆",
"国际",
"台湾",
"港澳",
"军事",
"社会",
"图片",
"评论",
"深度",
"历史",
"文化",
"专题",
"排行",
"专栏",
"新知",
"经济",
"政治",
"文化",
"社会",
"党建",
"科教",
"生态",
"国防",
"国际",
"纵横",
"图书",
"原创",
"论坛",
"看见",
"生活",
"文学",
"海外",
"社区",
"舆情",
"人大",
"政协",
"百姓",
"杂谈",
"摄影",
"映像",
"教育",
"金融",
"经济",
"万象",
"民生",
"民声",
"记者",
"政情",
}

EXCLUDE_COLUMN = {
'星座',
'娱乐',
'音乐',
'彩票',
'明星',
'游戏',
'开户',
'转户',
'提醒',
'邮箱',
'拍卖','下载',
'客服',
'更多',
'管理',
'声明',
'留言',
'关于',
'投稿',
'广告',
'联系',
'特卖',
'热辣',
'公交',
'报料',
'爆料',
'客户端',
'夫妻',
'婆媳',
'情感',
'感情',
'热恋',
'咨询',
'微信',
'申请',
'两性',
'导购',
'促销',
'婚',
'银行',
'查询',
'帮助',
'APP',
'试用',
'WAP','招聘',
'隐私',
'网站地图',
'时尚',
'用户',
'宝典','下载',
'首页',
'售',
'二手',
'投诉',
'恋爱','充值','婚恋',
'整形',

}

CAR = {
'学车',
'汽车',
'4s',
'4S',
'车市','购车','用车','新车',
'车友',
}