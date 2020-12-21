# -*- coding: utf-8 -*-
# assign05_김은혜.py
import requests
import re
from bs4 import BeautifulSoup


def get_article(url):
    # html text 가져오기
    html = requests.get(url,
                        headers={'User-Agent': 'Mozilla/5.0'}).text
    soup = BeautifulSoup(html, 'html.parser')

    # title 가져오기
    title0 = soup.select('title')
    title = title0[0].text

    # publisher 가져오기
    publisher0 = soup.select('h4 > em')
    publisher = publisher0[0].text

    # content 가져오기
    content0 = soup.select('#articleBodyContents')
    content = content0[0].text.strip()

    # title, publisher, content 반환
    return title, publisher, content


# news_title, news_publisher, news_content에 return 값 각각 넣기
news_title, news_publisher, news_content = get_article(
    'http://news.naver.com/main/ranking/read.nhn?rankingType=popular_day&oid=001&aid=0010083362&date=20180514&type=1&rankingSectionId=100&rankingSeq=4')

# news_title, news_publisher, news_content 값 출력하기
print('news_title: ' + news_title + '\nnews_publisher: ' +
      news_publisher + '\nnews_content: ' + news_content)

# news_content 값은 txt 파일에 저장하기
with open('naver_news.txt', 'w') as f:
    f.write(news_content)
