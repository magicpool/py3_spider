import requests
from lxml import etree
import time
from retrying import retry
import xlwt


class CpcLeader:
    def __init__(self):
        self.headers = {
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/62.0.3202.94 Safari/537.36"
        }

    def get_province_urllist(self):
        pro_start_url = "http://ldzl.people.com.cn/dfzlk/front/personProvince{}.htm"
        print("*"*100)
        pro_url_list = []
        page_nums = (1,18,35,219,351,465,580,650,792,810,926,1028,1150,1245,1357,1515,1692,
                    1809,1946,2089,2213,2240,2279,2482,2580,2726,2807,2925,3026,3078,3106,
                    3220,3221)
        for num in page_nums:
            pro_url_list.append(pro_start_url.format(num))
        return pro_url_list

    @retry(stop_max_attempt_number=5)
    def parse_province_urllist(self,pro_url):
        response = requests.get(url=pro_url,headers=self.headers,timeout=5)
        assert response.status_code == 200
        pro_html = response.content
        # print(pro_html)
        return pro_html


    def parse_province_content(self,pro_html):
        le_start_url = "http://ldzl.people.com.cn/dfzlk/front/{}"
        all_leader_url = []
        pro_content =etree.HTML(pro_html)
        leader_url_list = pro_content.xpath("//div[@class='fr p2j_sheng_right title_2j']/p/a/@href|"
                                            "//div[@class='ld2 new_ld']/ol[@class='fl']/li/em/a/@href|"
                                            "//div[@class='ld2 new_ld']/ol[@class='fl']/li/i/a/@href")
        print("正在获取领导人信息")
        for leurl in leader_url_list:
            all_leader_url.append(le_start_url.format(leurl))

        leader_list = []

        for leader_url in all_leader_url:
            leader = {}
            leader_response = requests.get(url=leader_url,headers=self.headers,timeout=5)
            # assert leader_response.status_code == 200
            leader_content =leader_response.content
            leader_html = etree.HTML(leader_content)
            leader['title'] = leader_html.xpath("//div[@class='fl p2j_text_center title_2j']//li//dd/span/text()")[0] \
                if len(leader_html.xpath("//div[@class='fl p2j_text_center title_2j']//li//dd/span/text()")) > 0 else None
            # print(leader['title'])
            leader['name'] = leader_html.xpath("//div[@class='fl p2j_text_center title_2j']//li//dd//em/text()")[0] \
                if len(leader_html.xpath("//div[@class='fl p2j_text_center title_2j']//li//dd//em/text()")) > 0 else None
            # print(leader['name'])
            leader['gender'] = leader_html.xpath("//div[@class='fl p2j_text_center title_2j']//li//dd/p/text()[1]")[0] \
                if len(leader_html.xpath("//div[@class='fl p2j_text_center title_2j']//li//dd/p/text()[1]")) > 0 else None
            # print(leader['gender'])
            leader['birth'] = leader_html.xpath("//div[@class='fl p2j_text_center title_2j']//li//dd/p/text()[3]")[0] \
                if len(leader_html.xpath("//div[@class='fl p2j_text_center title_2j']//li//dd/p/text()[3]")) > 0 else None
            # print(leader['birth'])
            leader['address'] = leader_html.xpath("//div[@class='fl p2j_text_center title_2j']//li//dd/p/text()[5]")[0] \
                if len(leader_html.xpath("//div[@class='fl p2j_text_center title_2j']//li//dd/p/text()[5]")) > 0 else None
            # print(leader['address'])
            leader['degree'] = leader_html.xpath("//div[@class='fl p2j_text_center title_2j']//li//dd/p/text()[7]")[0] \
                if len(leader_html.xpath("//div[@class='fl p2j_text_center title_2j']//li//dd/p/text()[7]")) > 0 else None
            # print(leader['degree'])
            leader['profile'] = leader_html.xpath("//div[@class='p2j_text']/p/text()")\
                if len(leader_html.xpath("//div[@class='p2j_text']/p/text()")) > 0 else None

            leader_list.append(leader)
        return leader_list

    def save_leader_content(self,leader_list):
        print(leader_list)
        for people in leader_list:
            self.ws.write(self.file_num,0,people["name"])
            self.ws.write(self.file_num,1,people["title"])
            self.ws.write(self.file_num,2,people["gender"])
            self.ws.write(self.file_num,3,people["birth"])
            self.ws.write(self.file_num,4,people["address"])
            self.ws.write(self.file_num,5,people["degree"])
            self.ws.write(self.file_num,6,people["profile"])
            self.file_num = self.file_num + 1
        # with open("领导人简历.csv", "a", encoding="utf-8") as f:
        #     for temp in leader_list:
        #         f.write(json.dumps(temp,ensure_ascii=False))
        #         f.write('\n')

    def run(self):
        # 1. 构建省级url_list
        print(">>>>>>>>>>>>构建省份链接<<<<<<<<<<<<<")
        pro_url_list = self.get_province_urllist()
        self.wb = xlwt.Workbook()
        self.file_num = 0
        self.ws = self.wb.add_sheet('leader', cell_overwrite_ok=True)

        for pro_url in pro_url_list:
            print("正在解析:%s" % pro_url)
            pro_html_content = self.parse_province_urllist(pro_url) # 2-3. 发送请求，获取各省政要url_list,获取各省政要内容
            time.sleep(3)
            leader_list = self.parse_province_content(pro_html_content)  #3. 发送请求，获取各省政要内容
            self.save_leader_content(leader_list) #5. 保存内容

        self.wb.save("123.xls")


if __name__ == '__main__':
    cpc = CpcLeader()
    cpc.run()