import random

import requests
import re
import os
from threading import Thread
import time
import logging

class ZhihuSpider():
    def __init__(self):
        self.headers = {
            "Host": "www.zhihu.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv;58.0) Gecko/20100101 Firefox/58.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"    #      这里自己看看令牌
        }
        self.num_id = '20300634'  #这里写你的那个问题的id
        self.base_url = 'https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20&sort_by=default'.format(self.num_id)
        self.image_list = set()
        self.count = 1
        self.base_dir = os.getcwd() + r'\img\{}'.format(self.num_id)

    def get_imgs(self,base_url):
        time.sleep(random.uniform(1,2))
        ret = requests.get(base_url, headers=self.headers)
        img_json = ret.json()
        print(img_json)
        totals = img_json['paging']['totals']
        is_end = img_json['paging']['is_end']
        next_ = img_json['paging']['next']
        data = img_json['data']
        for item in data:
            content = item['content']
            imgs = re.findall(r'img.*?src="https://(.*?)"', content, re.DOTALL)
            self.image_list.update(imgs)
        if is_end == False:
            print('开始下一页评论')
            print(next_)
            self.get_imgs(next_)
        else:
            print('爬完图片了~~~~~~~~~~~~')


    def download_images(self,img):
        name = img[18:-4]
        suffix = img[-4:]
        ret = requests.get('https://' + img)
        os.chdir(self.base_dir)
        print('共有照片{}，这是第 {} 张， 正在下载:{}'.format(len(self.image_list), self.count,img))
        with open(name + suffix, 'wb') as f:
            f.write(ret.content)
        self.count += 1

    def run(self):

        if not os.path.exists(self.base_dir):
            os.mkdir(self.base_dir, 0o755)
        self.get_imgs(self.base_url)
        for i in self.image_list:
           self.download_images(i)

        print('###########################下载结束#############################')


zhuhu = ZhihuSpider()
zhuhu.run()
