#-*- encoding: utf-8 -*-

import hashlib

import requests
from bs4 import BeautifulSoup

base_url = 'http://www.yhcgzf.gov.cn/gzdt_9204/yybb/'
headers = {'user-agent': 'Mozilla/5.0'}

def handler():
    response = requests.get(base_url, headers=headers)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, "html.parser")
    before_ele = soup.select("input#classlist1_classid_0")[0]
    table = before_ele.find_next_sibling('table')
    links = table.select('a')

    hrefs = []
    for a in links:
        hrefs.append(a.attrs['href'][2:]) # u'./201609/t20160905_509522.html'--> '201609/t20160905_509522.html'

    hrefs.sort(reverse=True)

    images = []
    for href in hrefs[:5]:
        page_url = base_url + href #http://www.yhcgzf.gov.cn/gzdt_9204/yybb/201609/t20160905_509520.html
        base_page_url = page_url.rsplit('/', 1)[0] # http://www.yhcgzf.gov.cn/gzdt_9204/yybb/201609
        response = requests.get(page_url, headers=headers)
        html_doc = response.text
        soup = BeautifulSoup(html_doc, "html.parser")

        author = soup.select("#author")[0]
        table = author.find_parent('table')
        img = table.select('img')[0]
        src = img.attrs['src'][2:] # ./W020160905351972077626.jpg --> W020160905351972077626.jpg
        img_url = base_page_url + '/' + src
        images.append(img_url)

    images.sort(reverse=True)
    m = hashlib.md5()
    m.update(''.join(images))
    etag = m.hexdigest()

    return {'images': images, 'etag': etag}
