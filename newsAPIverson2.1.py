import sys
import csv
import time
from newsapi import NewsApiClient
from prettytable import PrettyTable

newsapi = NewsApiClient(api_key='xxxxxxx')
pagesize = 100



def inofs():
    print("""
###################################################################
---------------------重要说明---------------------------------------
foreignNewsSearch是一个基于开源项目NewsAPI.org、使用python编写的命令行工具，
授权条款为MIT License。因免费套餐接口调用次数有限，每日下载文章数理论值约为10
万篇，请酌情使用。如有疑问请联系作者或访问https://newsapi.org.
---------------------重要说明---------------------------------------
###################################################################
""")
    authen = input("同意请输入Y，不同意输入N:")
    if authen.lower() == "y":
        pargram_fuc()
    elif authen.lower() == "n":
        sys.exit()
    else:
        print("输入有误，程序将退出")
        sys.exit()


def pargram_fuc():
    print("""
*******************************************************************
                    程序功能菜单                            
                1.获取本程序查询的媒体列表                  
                2.查询今日境外头条新闻                      
                3.自定义查询境外媒体报道                    
                4.退出程序                                
*******************************************************************
""")
    fuc = input("请输入想要使用的功能编号：")
    if fuc == "1":
        get_media()
    elif fuc == "2":
        query_headline = input("请输入查询关键词：")
        sources = input("请输入查询信息源："),
        language = input("请输入查询语言："),
        country = input("请输入查询国家："),
        category = input("请输入查询类别：")
        params = [query_headline, sources, language, country, category]
        get_headlines(params)
    elif fuc == "3":
        query_headline_e = input("请输入查询关键词：")
        from_date = input("请输入起始日期（YYYY-MM-DD格式）：")
        end_date = input("请输入截止日期（YYYY-MM-DD格式）：")
        sources_e = input("请输入查询信息源："),
        language_e = input("请输入查询语言："),
        domains_e = input("请输入查询域名：")
        params_e = [query_headline_e, from_date, end_date, sources_e, language_e, domains_e]
        search_everyting(params_e)
    elif fuc == '4':
        sys.exit()
    else:
        print("输入有误,程序退出")



def get_media():
    print('请稍后，正在查找媒体机构........')
    sources = newsapi.get_sources(category=None, language=None, country=None)
    x = PrettyTable(["媒体名称", "语言", "国家"])
    x.align["id"] = "l"
    x.padding_width = 1
    print("------↓↓↓↓共找到%d家媒体机构↓↓↓↓-----" % len(sources['sources']))
    time.sleep(1.5)
    for temp in sources['sources']:
        x.add_row([temp['id'], temp['language'], temp['country']])
    print(x)
    usr_q = input("执行完毕，是否退出？Q键退出程序，其他键再次执行查询。")
    if usr_q.lower() == "q":
        exit()
    else:
        pargram_fuc()

def get_headlines(params):
    top_headlines = newsapi.get_top_headlines(q=params[0],
                                              sources=params[1],
                                              language=params[2],
                                              country=params[3],
                                              category=params[4])
    print('请稍后，正在查找........')
    if top_headlines['totalResults'] != 0:
        h = PrettyTable(["媒体名称", "标题"])
        h.align["id"] = "l"
        h.padding_width = 1
        print("------↓↓↓↓共找到{}条报道↓↓↓↓-----".format(top_headlines['totalResults']))
        time.sleep(1.5)
        for article in top_headlines['articles']:
            h.add_row([article['source']['name'], article['title']])
        print(h)
        pargram_fuc()
    else:
        print("没有找到相关报道")
        pargram_fuc()


def search_everyting(params_e):
    i = 1
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    all_articles = newsapi.get_everything(q=params_e[0],
                                          sources=params_e[3],
                                          domains=params_e[5],
                                          from_parameter=params_e[1],
                                          to=params_e[2],
                                          language=params_e[4],
                                          sort_by='relevancy',
                                          page=i,
                                          page_size=100)
    total_number = all_articles['totalResults']
    total_page = total_number // 100 + 1
    headers = ['name', 'author', 'title', 'url', 'urlToImage', 'publishedAt', 'description']
    with open('{}_records.csv'.format(params_e[0]), 'w', newline='', encoding='utf-8') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        while i <= total_page:
            print("正在获取第{}页.......".format(i))
            for article in all_articles['articles']:
                print(str(article).translate(non_bmp_map))
                f_csv.writerow([article['source']['name'],
                                article['author'],
                                article['title'],
                                article['url'],
                                article['urlToImage'],
                                article['publishedAt'],
                                article['description']], )
            # print(all_articles)
            i += 1
        else:
            s = input("执行完毕，结果以保存至当前目录，是否退出？Q键退出程序，其他键再次执行查询。")
            if s.lower() == 'q':
                exit()
            else:
                pargram_fuc()


if __name__ == '__main__':
    inofs()
    pargram_fuc()

    
