# author:MagicPool

import mediacloud
import time
import datetime
import csv

mc = mediacloud.api.MediaCloud('xxxxxxx')
id_media = ['58722749', '57078150', '34412118', '34412232', '9272347', '38379799', '34412476']

q = input('请输入查询关键词（布尔格式）：')
start_date = input("输入开始日期：（例如：2018-08-01）")
end_date = input("输入截止日期：")
s_date = datetime.datetime.strptime(start_date,'%Y-%m-%d')
e_date = datetime.datetime.strptime(end_date,'%Y-%m-%d')
print("本程序共有7大数据集:\n"
      "1.美国主流新闻媒体\n"
      "2.美国数字媒体\n"
      "3.印度媒体\n"
      "4.俄罗斯媒体\n"
      "5.全球媒体\n"
      "6.法国媒体\n"
      "7.英国媒体\n")
source_usr = int(input("请输入相应数字编号:"))

us_mainstream_media = 'tags_id_media:{}'.format(id_media[0])
us_digital_news = 'tags_id_media:{}'.format(id_media[1])
india_news = 'tags_id_media:{}'.format(id_media[2])
russia_news = 'tags_id_media:{}'.format(id_media[3])
global_news = 'tags_id_media:{}'.format(id_media[4])
france_news = 'tags_id_media:{}'.format(id_media[5])
uk_news = 'tags_id_media:{}'.format(id_media[6])

source_list = [us_mainstream_media,us_digital_news,india_news,russia_news,global_news,france_news,uk_news]
res = mc.storyCount(q + ' AND  ' + source_list[source_usr-1],solr_filter=mc.publish_date_query(s_date,e_date))
num = res['count']
print("共找到文章{}篇".format(num))

def get_posts():
    fetch_size = 100
    stories = []
    last_processed_stories_id = 0
    # articles = []
    page_num = num // fetch_size + 1
    i = 1

    while i <= page_num:
        if num == 0:
            break
        print("正在获取第{}页".format(i))
        fetched_stories = mc.storyList(q + ' AND ' + source_list[source_usr-1],solr_filter=mc.publish_date_query(s_date,e_date),
                                       last_processed_stories_id=last_processed_stories_id, rows= fetch_size)

        stories.extend(fetched_stories)
        print("已获取{}篇,共{}篇,已完成{:.0%}".format(len(stories),num,len(stories)/num))
        if len(fetched_stories) < fetch_size:
            break
        last_processed_stories_id = stories[-1]['processed_stories_id']
        print("已添加ID：{}".format(last_processed_stories_id))
        time.sleep(1)
        i += 1

    return stories


def save_csv(stories):
    headers = ['media_name', 'publish_date', 'title', 'url']
    with open("records.csv", 'w', newline='',encoding='utf-8')as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        for story in stories:
            f_csv.writerow([story['media_name'],story['publish_date'],story['title'],story['url']])

        print("done!")


if __name__ == '__main__':
    stories = get_posts()
    save_csv(stories)