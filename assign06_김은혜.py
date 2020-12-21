# -*- coding: utf-8 -*-
# assign06_김은혜.py

import re
import requests
from bs4 import BeautifulSoup 

# article의 publisher, title, content 가져오기
def get_article(url):
    # Obtain three types of information about a news article
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    publisher = soup.find('meta', attrs={'property':'og:site_name'}).get('content')
    news_title = soup.title.text
    news_contents = soup.find_all ('p')
    content_text = ''
    for content in news_contents:
        content_text = content_text +' '+ content.text
    return news_title, publisher, content_text

# url을 입력해서 get_article 함수로 해당 url의 title, content, publisher 가져오기
url = 'https://www.yna.co.kr/view/AKR20181008116600055'
title, publisher, content = get_article(url)

# 문장 부호 등 제거하기
filtered_content = content.replace('.', '').replace(',','').replace("'","").replace('·', ' ').replace('=','').replace('"','')
filtered_content = re.sub(r'[^\.\?\!\w\d\s]','',content)

# okt 불러오기
from konlpy.tag import Okt
okt = Okt()

# 형태소(단어) 중에 명사만 뽑아내기
nouns_words = okt.nouns(filtered_content)

# 불용어 등록하기
stopwords = ['연합뉴스', '서울', '기자', '정경재', '김도훈', '저작권자', '무단', '전재', '재배포', '금지', '송고']

# 중복 되는 단어 제거하기
unique_noun_words = set(nouns_words)

# 단어 중에 불용어가 있으면 제거하기
for word in unique_noun_words :
    if word in stopwords :
        while word in nouns_words : nouns_words.remove(word)

# 불용어가 제거된 최종 명사 리스트
print('#1. 불용어가 제거된 최종 명사 리스트')
print(nouns_words)
# 불용어가 제거된 최종 명사 개수
print('#2. 불용어가 제거된 최종 명사 개수')
print(len(nouns_words))