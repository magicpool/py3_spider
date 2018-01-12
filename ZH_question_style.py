#coding='utf-8'
import requests
import json
import re
import time
import datetime
import os
import xlwt
from retrying import retry

@retry(stop_max_attempt_number=3)
def get_content(url):
# 提交请求，相应请求
    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
                'Referer': 'https://www.zhihu.com/question/64824598',
                'X-UDID': 'AJACNu3zzwyPTlNV8CxTJQxTX-9h93DWqAg=',
                'authorization': 'Bearer 2|1:0|10:1515595727|4:z_c0|92:Mi4xYlpTc0JBQUFBQUFBa0FJMjdmUFBEQ1lBQUFCZ0FsVk56M1ZEV3dDQmFURU5idURsVllsdDg5dDZSOGZiZFJkd3pR|598437f1da15cc53bd75a5816b5388d84013290d367b20e1bfebb0d52413adc7',
                'Cookie': '_zap=9a96d0cb-2e41-45e1-bccf-3e7f051c704b; d_c0="AJACNu3zzwyPTlNV8CxTJQxTX-9h93DWqAg=|1512893908"; aliyungf_tc=AQAAAMJM9zbXMA8AAjbpZ8OIdOCqvyLG; q_c1=66cb2aff22b44e0a8c81e6ae880f574a|1515595721000|1512621057000; capsion_ticket="2|1:0|10:1515595725|14:capsion_ticket|44:MDAxYmI3OGM5MDQxNGRkZDlkNDhhZDgwZmM0YzIxY2Q=|74eea373a06424520642827f551f43d69dec3e4137fc1b08a57e505aa11b5400"; z_c0="2|1:0|10:1515595727|4:z_c0|92:Mi4xYlpTc0JBQUFBQUFBa0FJMjdmUFBEQ1lBQUFCZ0FsVk56M1ZEV3dDQmFURU5idURsVllsdDg5dDZSOGZiZFJkd3pR|598437f1da15cc53bd75a5816b5388d84013290d367b20e1bfebb0d52413adc7"; __utma=51854390.37961403.1515595736.1515595736.1515595736.1; __utmb=51854390.0.10.1515595736; __utmc=51854390; __utmz=51854390.1515595736.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100--|2=registration_date=20170411=1^3=entry_date=20170411=1; _xsrf=9d00a62f-00be-4027-a139-8bb8e10579ca'

           }
    req_session = requests.session()
    try:
        print("@@@@@@@")
        response = req_session.get(url, headers=headers, verify=False)
        print(response.status_code)
        print("提示:除最后一批，单次爬取20条数")
        content = json.loads(response.text)
        return content
    except:
        print("提示：数据爬取失败，请排查异常情况。。。。。。")


def run(req_url):
# 流程
#     pass
    # 1、接收用户收入url，
    # 2、进行请求，获取content
    file_num = 0
    url = req_url
    print(url)
    print('***********')
    wb = xlwt.Workbook()
    ws = wb.add_sheet('ZhihuSpider', cell_overwrite_ok=True)
    while True:
        content = get_content(url)
        # 3、处理content，返回数据和url，下一页的url进行返回，重新调用数据处理(打印回答量)
        paging_info = get_url(content)
        # print("提示：该问题共有%s条回答" %paging_info['totals'])
        data_text_list = get_data(content)
        #3.5取得字体格式
        styleDkBlue, styleRsRed, styleBlue = site_style()
        # 4进行数据保存
        file_num = save_data(data_text_list, file_num, ws, styleDkBlue, styleRsRed, styleBlue)
        print("提示：已爬取%s条" %file_num)
        # 5、判断是否有下一页，如果有，继续发出请求
        if paging_info['is_end'] == False :
            url = paging_info['next']
            print(url)
        else:
            # wb.save('E:\\'+data_text_list[0]["question_title"]+'.xlsx')
            ws.write(file_num+5, 0, "说明:超长（字符数量>32767）内容，超长部分放入“更多内容...”中", styleRsRed)
            wb.save(data_text_list[0]["question_title"]+'.xls')
            print(">>>>>>>")
            print("提示：标题“%s”" %data_text_list[0]["question_title"])
            print("提示：该问题 %s 条回答,爬取 %%s 条" %paging_info['totals'] %file_num)
            print("提示：------数据采集完毕!保存至同名文件!--------------------------------------------------------------")
            break
    wb.save(data_text_list[0]["question_title"] + '.xls')

@retry(stop_max_attempt_number=3)
def get_url(content):
#获取下一页信息
    # print('$'*10)
    print(content)
    # time.sleep(2)
    paging_dic = content['paging']
    paging_item = {}
    # 是否最后一页
    paging_item['is_end'] = paging_dic['is_end']
    # 回答量
    paging_item['totals'] = paging_dic['totals']
    paging_item['previous'] = paging_dic['previous']
    # 下一页地址
    paging_item['next'] = paging_dic['next']
    return paging_item
def get_data(content):
#处理数据，得到项目信息
    data_list = content['data']
    # print(data_list)
    data_text_list = []
    for data in data_list:
        # print(data)
        item = {}
        # 问题创建时间
        item['question_created_time'] = time_tran_stamp(data['question']['created'])
        # 问题更新时间
        # item['question_updated_time'] = data['question']['updated_time']
        item['question_updated_time'] = time_tran_stamp(data['question']['updated_time'])
        # 点赞数
        item['voteup_count'] = data['voteup_count']
        # 用户名
        item['author_name'] = data['author']['name']
        # 性别,男-1，女0，未知1
        item['author_gender'] = data['author']['gender']
        if item['author_gender'] == -1:
            item['author_gender'] = '男'
        elif item['author_gender'] == 0:
            item['author_gender'] = '女'
        else:
            item['author_gender'] = '未知'
        # 是否广告者
        item['author_is_advertiser'] = data['author']['is_advertiser']
        if item['author_is_advertiser'] == False:
            item['author_is_advertiser'] = '否'
        else:
            item['author_is_advertiser'] = '是'
        # 简单介绍
        item['author_headline']  = data['author']['headline']
        #用户主页
        url_user = data['author']['url']
        if url_user =='http://www.zhihu.com/api/v4/people/0':
            item['author_url'] ='空'
        else :
            item['author_url'] = re.sub(r'/api/v4', "", url_user)
        # 问题
        item['question_title'] = data['question']['title']
        # 回复时间
        item['question_created_time'] = time_tran_stamp(data['created_time'])
        # 回答内容
        # item['answer_content'] = data['content']
        # item['answer_content'] = re.sub(r'<.*>', '', data['content'])
        item['answer_content_all'] = re.sub(r'<[^>]+>', '', data['content'])
        if len(item['answer_content_all']) > 32767:
            # 如果字符数量超过单元格最大容量，则放在'answer_content_exlen'
            item['answer_content'] = item['answer_content_all'][0:32767]
            item['answer_content_exlen'] = item['answer_content_all'][32767:]
            print("@@@@@@@@@@@@")
        else:
            item['answer_content'] = item['answer_content_all']
            item['answer_content_exlen'] = "无"
        # 评论数
        item['comment_count'] = data['comment_count']
        # 问题链接
        url_question = data['question']['url']
        item['question_url'] = re.sub(r'/api/v4', "", url_question)
        data_text_list.append(item)
    return data_text_list
def save_data(data_text_list, file_num, ws, styleDkBlue, styleRsRed, styleBlue):
#文件保存
    for data in data_text_list:
        print(data)
        if file_num == 0 and os.path.exists(data['question_title']+".xls") == True:
            print("删除保存目录下的同名文件《%s.xls》,并重新执行本程序" %data['question_title'])
            exit()
        else:
            if file_num == 0:
                # 打印标题
                ws.write(0, 0, "标题：", styleDkBlue)
                ws.write(0, 1, data['question_title'], styleDkBlue)
                ws.write(1, 0, "创建时间：", styleDkBlue)
                ws.write(1, 1, data['question_created_time'], styleDkBlue)
                ws.write(2, 0, "更新时间：", styleDkBlue)
                ws.write(2, 1, data['question_updated_time'], styleDkBlue)
                ws.write(3, 0, "问题链接：", styleDkBlue)
                ws.write(3, 1, data['question_url'], styleDkBlue)
                ws.write(4, 0, "序号", styleBlue)
                ws.write(4, 1, "内容", styleBlue)
                ws.write(4, 2, "点赞", styleBlue)
                ws.write(4, 3, "评论", styleBlue)
                ws.write(4, 4, "回复时间", styleBlue)
                ws.write(4, 5, "用户名", styleBlue)
                ws.write(4, 6, "性别", styleBlue)
                ws.write(4, 7, "广告者?", styleBlue)
                ws.write(4, 8, "介绍", styleBlue)
                ws.write(4, 9, "用户主页", styleBlue)
                ws.write(4, 10, "更多内容...", styleBlue)
                ws.write(5, 0, file_num + 1, styleBlue)
                ws.write(5, 1, data['answer_content'], styleBlue)
                ws.write(5, 2, data['voteup_count'], styleBlue)
                ws.write(5, 3, data['comment_count'], styleBlue)
                ws.write(5, 4, data['question_created_time'], styleBlue)
                ws.write(5, 5, data['author_name'], styleBlue)
                ws.write(5, 6, data['author_gender'], styleBlue)
                ws.write(5, 7, data['author_is_advertiser'], styleBlue)
                ws.write(5, 8, data['author_headline'], styleBlue)
                ws.write(5, 9, data['author_url'], styleBlue)
                ws.write(5, 10, data['answer_content_exlen'], styleBlue)
                file_num = file_num + 1
            else:
                # ws.write(file_num+1, 0,)
                # with open (data['question_title']+".csv", 'a') as f:
                    # f.write(json.dumps(data),)
                    # f.write("\n")
                answer_num = file_num+5
                ws.write(answer_num, 0, file_num+1, styleBlue )
                ws.write(answer_num, 1, data['answer_content'], styleBlue)
                ws.write(answer_num, 2, data['voteup_count'], styleBlue)
                ws.write(answer_num, 3, data['comment_count'], styleBlue)
                ws.write(answer_num, 4, data['question_created_time'], styleBlue)
                ws.write(answer_num, 5, data['author_name'], styleBlue)
                ws.write(answer_num, 6, data['author_gender'], styleBlue)
                ws.write(answer_num, 7, data['author_is_advertiser'], styleBlue)
                ws.write(answer_num, 8, data['author_headline'], styleBlue)
                ws.write(answer_num, 9, data['author_url'], styleBlue)
                ws.write(answer_num, 10, data['answer_content_exlen'], styleBlue)
                file_num = file_num + 1
    return file_num
def time_tran_stamp(time_date):
#时间戳处理
    time_tran_ing = time.localtime(time_date)
    return time.strftime('%Y-%m-%d %H:%M:%S', time_tran_ing)
def site_style():
    # 字体样式
    # 深蓝色
    fontDkBlue = xlwt.Font()
    fontDkBlue.name = u'幼圆'
    fontDkBlue.colour_index = 8
    # 枚红色
    fontRsRed = xlwt.Font()
    fontRsRed.name = u'幼圆'
    fontRsRed.colour_index = 25
    # 浅蓝色
    fontBlue = xlwt.Font()
    fontBlue.name = u'幼圆'
    fontBlue.colour_index = 18
    # 边框样式
    borderBlue = xlwt.Borders()
    borderBlue.left = 1
    borderBlue.rigth = 1
    borderBlue.top = 1
    borderBlue.bottom = 1
    borderBlue.left_colour = 0x36
    borderBlue.right_colour = 0x36
    borderBlue.top_colour = 0x36
    borderBlue.bottom_colour = 0x36

    # styleDkBlue深蓝色字体、无边框
    styleDkBlue = xlwt.XFStyle()
    styleDkBlue.font = fontDkBlue
    # styleRsRed梅红色字体、无边框
    styleRsRed = xlwt.XFStyle()
    styleRsRed.font = fontRsRed
    # styleBlue蓝色字体、蓝色边框
    styleBlue = xlwt.XFStyle()
    styleBlue.font = fontBlue
    styleBlue.borders = borderBlue
    return styleDkBlue, styleRsRed, styleBlue
if __name__ == '__main__':
    #给"url_input"输入知乎问答地址(注意格式)
    # url_input = 'https://www.zhihu.com/question/68546899'
    url_input = 'https://www.zhihu.com/question/265406739'
    url_id = re.findall(r'\d*$', url_input)[0]
    # req_url = 'http://www.zhihu.com/api/v4/questions/'+url_id+'/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=0'
    req_url = 'https://www.zhihu.com/api/v4/questions/'+url_id+'/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20&sort_by=default'
    # req_url = "http://www.zhihu.com/api/v4/questions/64824598/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=3&limit=20&sort_by=default"
    run(req_url)

