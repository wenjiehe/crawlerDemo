import builtwith
import whois
from urllib import robotparser
import ssl
import requests
import re

ssl._create_default_https_context = ssl._create_unverified_context

#识别网站所用技术的工具
zhulang = builtwith.parse('http://book.zhulang.com')
print(zhulang)

#查询网站所有者的工具
owner = whois.whois('book.zhulang.com')
print(owner)

#解析robots.txt
parser = robotparser.RobotFileParser()
parser.set_url('http://book.zhulang.com/robots.txt')
parser.read()
print(parser)

def html_content(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        for charset in ('utf-8', ):
            try:
                content = resp.content.decode(charset)
                # print(content)
                res = r'</style>.*?<p>(.*?)<p>.*?<cite>'
                textList = re.findall(res, content)
                print(textList)

            except UnicodeDecodeError:
                pass

def main():
    """开始爬取数据"""
    print('开始爬取数据')
    new_urls = 'http://book.zhulang.com/571724/'
    resp = requests.get(new_urls)
    if resp.status_code == 200:
        for charset in ('utf-8', ):
            try:
                content = resp.content.decode(charset)
                linkList = re.findall('target="_blank".*?href="(.*?)".*?title=".*?"', content)
                titleList = re.findall('<a.*?target="_blank".*?href=".*?".*?title=".*?">(.*?)</a>', content)
                titleList = [x.replace('<span style="color:red">[vip]</span>', '') for x in titleList]
                titleList = [x.strip() for x in titleList]
                print(linkList)
                print(titleList)
                url = linkList[0]
                html_content(url)
            except UnicodeDecodeError:
                pass

if __name__ == '__main__':
    main()
