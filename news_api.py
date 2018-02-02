import csv
import time
from newsapi import NewsApiClient
from prettytable import PrettyTable

newsapi = NewsApiClient(api_key='YourOwnApiKey')
page = 1


def get_media():
    sources = newsapi.get_sources()
    x = PrettyTable(["媒体名称", "语言"])
    x.align["id"] = "l"
    x.padding_width = 1
    print('请稍后，正在查找媒体机构........')
    time.sleep(1)
    print("共找到%d家媒体机构"% len(sources['sources']))
    for temp in sources['sources']:
        x.add_row([temp['id'],temp['language']])
    print(x)
    


def search_everyting():
    i = 1
    headers = ['name', 'author', 'title', 'url', 'urlToImage', 'publishedAt', 'description']
    with open('{}_records.csv'.format(query), 'w',newline='',encoding='utf-8') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        while i <= total_number:
            all_articles = newsapi.get_everything(q=query,sources= source,domains=None,from_parameter=from_date,to=end_date,language=lange,sort_by='relevancy',page=i,page_size=100)
            for article in all_articles['articles']:
                print(article)
                f_csv.writerow([article['source']['name'],
                                article['author'],
                                article['title'],
                                article['url'],
                                article['urlToImage'],
                                article['publishedAt'],
                                article['description']],)
            # print(all_articles)
            i += 1


if __name__ == '__main__':
    get_media()
    success = True
    while success is True:
        query = input('请输入查询关键词')
        source = input("请输入信息源：")
        # input date formatted as YYYY-MM-DD
        from_date = input("请输入起始日期")
        end_date = input("请输入截止日期")
        lange = input("请输入语言代码")
    
        all_articles = newsapi.get_everything(q=query,sources= source,domains=None,from_parameter=from_date,to=end_date,language=lange,sort_by='relevancy',page=1,page_size=100)
        total_number = all_articles['totalResults']//100 + 1
        search_everyting()
        s = input("执行完毕，是否退出？Q退出程序，C继续执行")
        if s.lower() == 'q':
            success = False
        else:
            success = True