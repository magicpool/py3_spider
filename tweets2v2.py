#!/usr/bin/python3
# __Author__  :    MagicSugar
# __Time__    :    2018/8/23 下午10:41
import sys
from twitterscraper import query
# import twitterscraper
import csv
import datetime

def menu():
    print("""
*******************************************************************
                    程序功能菜单                            
                1.获取制定推特账号推文                  
                2.搜索获取特定关键词推文                                         
                3.退出程序                                
*******************************************************************
""")


def get_record():
    list_of_tweets = query.query_tweets(query=q, limit=num, begindate=datetime.date(year_bg,month_bg,day_bg),
                                                 enddate=datetime.date(year_ed,month_ed,day_ed),
                                                 poolsize=20, lang=lang)
    return list_of_tweets


def get_user_tweets():
    user_tweets_list = query.query_tweets_from_user(user=q,limit=tweets_num)
    return user_tweets_list




def save(tweets):
    csv_header = ["user", "fullname", "tweet-id", "timestamp", "url", "likes", "replies", "retweets", "text", "html"]
    with open('{}_tweets.csv'.format(q), 'w', newline='', encoding='utf-8') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(csv_header)
        for tweet in tweets:
            # print(tweet)
            f_csv.writerow([tweet.user, tweet.fullname, tweet.id, tweet.timestamp, tweet.url, tweet.likes,
                            tweet.replies, tweet.retweets, tweet.text, tweet.html])


if __name__ == '__main__':
    menu()
    fuc_num = int(input("请输入功能编号："))
    if fuc_num == 1:
        q = input("请输入要查询的用户名：")
        tweets_num = int(input("请输入要获取的推文数量："))
        if tweets_num == -1:
            tweets_num = None
        user_records = get_user_tweets()
        save(user_records)

    elif fuc_num == 2:
        q = input("请输入查询关键词（布尔格式）：")
        # q = "贸易战"
        from_date = input("输入开始日期：")
        # from_date = "2018-07-01"
        until_date = input('輸入截止日期：')
        # until_date = "2018-08-20"
        from_date_list = from_date.split('-')
        until_date_list = until_date.split('-')
        year_bg = int(from_date_list[0])
        year_ed = int(until_date_list[0])
        month_bg = int(from_date_list[1])
        month_ed = int(until_date_list[1])
        day_bg = int(from_date_list[2])
        day_ed = int(until_date_list[2])
        lang = input("请输入推文的语言码（中文：zh，英文：en）：")
        num = int(input("请输入获取的推文数量（必须是20的倍数），如不限制请输入0："))
        if num == -1:
            num = None

        records = get_record()
        save(records)

    else:
        sys.exit()