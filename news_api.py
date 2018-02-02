import json
import csv
import time
from newsapi import NewsApiClient
from prettytable import PrettyTable

newsapi = NewsApiClient(api_key='e022a900d2b241ce8ebea3a5f363e652')
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
    with open('stocks.csv', 'w',newline='',encoding='utf-8') as f:
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
        query = '19th party congress'
        source = input("请输入信息源：")
        # input date formatted as YYYY-MM-DD
        from_date = '2018-01-01'
        end_date = '2018-01-30'
        lange = 'en'
    
        all_articles = newsapi.get_everything(q=query,sources= source,domains=None,from_parameter=from_date,to=end_date,language=lange,sort_by='relevancy',page=1,page_size=100)
        total_number = all_articles['totalResults']//100 + 1
        search_everyting()
        s = input("执行完毕，是否退出？Q退出程序，C继续执行")
        if s.lower() == 'q':
            success = False
        else:
            success = True