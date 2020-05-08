# Redbook-Spider

  小红书笔记爬虫
 
  该爬虫仅供学习使用
  
# 文件介绍
  Setting.py : 爬虫设置文件
  
  Main.py : 爬虫主程序

# 其他

  通过Fiddler抓包pc端小程序拿到API地址：
  
  http://www.xiaohongshu.com/fe_api/burdock/weixin/v2/search/notes?keyword=%E6%9D%AD%E5%B7%9E%E4%BA%B2%E5%AD%90&sortBy=hot_desc&page={}&pageSize=20&needGifCover=true&sid=session.1575338664880906512653
  
  有session限制，使用爬虫前需自行替换请求头和session
  
  这次更新了可以自行输入关键词进行爬取，目前支持爬取笔记标题、内容、图片和视频链接
  
