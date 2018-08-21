# -*- coding:utf-8 -*-
import sys
import io
import csv
import time
import json
import random
import hashlib
import requests
import newsapi
from prettytable import PrettyTable

newsApi = newsapi.NewsApiClient(api_key='xxxxx')
pagesize = 100

appKey = 'xxxxxx'
secretKey = 'xxxxxx'


def inofs():
    print("""
###################################################################
------------------------说明---------------------------------------
ForeignNewsSearch是一个基于开源项目NewsAPI.org编写的命令行工具，授权条款
为MIT License。因接口调用次数有限，每日下载文章数理论值约为10万篇，请酌情
使用。如有疑问请联系作者或访问https://newsapi.org.
------------------------说明---------------------------------------
###################################################################
""")
    pargram_fuc()

def pargram_fuc():
    print("""
*******************************************************************
                    程序功能菜单                            
                1.查看本程序查询的媒体列表                  
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
    sources = newsApi.get_sources(category=None, language=None, country=None)
    x = PrettyTable(["媒体名称", "语言", "国家"])
    x.align["id"] = "l"
    x.padding_width = 1
    print("------↓↓↓↓共找到%d家媒体机构↓↓↓↓-----" % len(sources['sources']))
    time.sleep(1)
    for temp in sources['sources']:
        x.add_row([temp['id'], temp['language'], temp['country']])
    print(x)
    usr_q = input("执行完毕，是否退出？Q键退出程序，其他键再次执行查询。")
    if usr_q.lower() == "q":
        sys.exit()
    else:
        pargram_fuc()

def get_headlines(params):
    top_headlines = newsApi.get_top_headlines(q=params[0],
                                              sources=params[1],
                                              language=params[2],
                                              country=params[3],
                                              category=params[4])
    print('请稍后，正在查找........')
    if top_headlines['totalResults'] != 0:
        h = PrettyTable(["媒体名称", "标题（英）", "标题（中）","链接"])
        h.align["id"] = "l"
        h.padding_width = 1
        print("------↓↓↓↓共找到{}条报道↓↓↓↓-----".format(top_headlines['totalResults']))
        print("正在写入TXT")
        with open('headlines.txt', 'a+') as f:
            f.write('\n'+ time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+'\n')
            for article in top_headlines['articles']:
                print("标题(英)：{}".format(article['title']))
                a = article['title'].encode('latin-1','ignore')
                b = a.decode('latin-1','ignore')
                tt_zh = trans(b)
                print("标题（中）{}".format(tt_zh))
                if tt_zh is not None:
                    time.sleep(2)
                    f.write("---"*40+'\n')
                    f.write(article['source']['name']+'\n')
                    f.write(article['title']+'\n')
                    f.write(tt_zh+'\n')
                    f.write(article['url'] + '\n')
                    f.write("---"*40+'\n'+'\n')
                    h.add_row([article['source']['name'], article['title'],tt_zh, article['url']])
                else:
                    print("翻译有误")
            f.write("***"*40)
            print("写入完毕")
        pargram_fuc()
    else:
        print("没有找到相关报道")
        pargram_fuc()


def search_everyting(params_e):
    i = 1
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    all_results = newsApi.get_everything(q=params_e[0],
                                          sources=params_e[3],
                                          domains=params_e[5],
                                          from_parameter=params_e[1],
                                          to=params_e[2],
                                          language=params_e[4],
                                          sort_by='relevancy',
                                          page=i,
                                          page_size=100)
    total_number = all_results['totalResults']
    print("**************共找到{}条报道**************".format(total_number))

    total_page = total_number // 100 + 1
    headers = ['name', 'author', 'title', 'url', 'urlToImage', 'publishedAt', 'description']
    with open('{}_records.csv'.format(params_e[0]), 'w', newline='', encoding='utf-8') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        while i <= total_page:
            all_articles = newsApi.get_everything(q=params_e[0],
                                        sources=params_e[3],
                                        domains=params_e[5],
                                        from_parameter=params_e[1],
                                        to=params_e[2],
                                        language=params_e[4],
                                        sort_by='relevancy',
                                        page=i,
                                        page_size=100)
            # print("正在获取第{}页，已完成{:.2%}.......".format(i,i/total_page))
            for article in all_articles['articles']:
                # print(str(article).translate(non_bmp_map))
                f_csv.writerow([article['source']['name'],
                                article['author'],
                                article['title'],
                                article['url'],
                                article['urlToImage'],
                                article['publishedAt'],
                                article['description']], )
            time.sleep(0.01)
            i += 1
            recv_per=int(100*i/total_page)
            progress(recv_per,width=30)
        else:
            s = input("执行完毕，结果已保存至当前目录，是否退出？Q键退出程序，其他键再次执行查询。")
            if s.lower() == 'q':
                sys.exit()
            else:
                pargram_fuc()

def progress(percent,width=50):
    '''进度打印功能'''
    if percent >= 100:
        percent=100
  
    show_str=('[%%-%ds]' %width) %(int(width * percent/100)*"#") #字符串拼接的嵌套使用
    print('\r%s %d%%' %(show_str,percent),end='')            

def trans(query):
    pid = "625615497ff2a09ae7ce5fcde77e4069"
    q = query
    salt = random.randint(1,65536)
    key = "54868db52061ae5b5eadd3034ccc9630"

    sign_raw = pid+q+str(salt)+key
    sign = hashlib.md5(sign_raw.encode('utf-8')).hexdigest()
    url = "http://fanyi.sogou.com:80/reventondc/api/sogouTranslate"
    payload = "from=en&to=zh-CHS&pid={0}&q={1}&sign={2}&salt={3}".format(pid,q,sign,salt)
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json"
        }
    response = requests.request("POST", url=url, data=payload, headers=headers)
    record = json.loads(response.text)
    if record['errorCode'] != "0":
        return None
    else:
        text = record['translation']
        return text


if __name__ == '__main__':
    inofs()
    pargram_fuc()

