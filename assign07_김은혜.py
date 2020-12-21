import re

import requests
from bs4 import BeautifulSoup 

def get_article(url):
    # Obtain three types of information about a news article
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(r.text, 'lxml')
    
    news_title = soup.title.text
    news_subtitle = soup.select('#articleBodyContents > b')[0].text
    news_contents = soup.find('div', id= "articleBodyContents").text
    
    # 내용에서 불필요한 부분 제외
    news_contents = news_contents.replace("가상통화 가격 떨어질 것이라는 전망과 더 오를 것이라는 예상 교차", "")
    news_contents = news_contents.replace("// flash 오류를 우회하기 위한 함수 추가", "")
    news_contents = news_contents.replace("function _flash_removeCallback() {}", "")
    news_contents = news_contents.strip()
    
    return news_title, news_subtitle, news_contents
    
url = 'https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=101&oid=277&aid=0004164498'
title, subtitle, content = get_article(url)
print(title, subtitle, content)

# title, subtitle, content 값을 txt 파일에 저장하기
with open('bitcoin_news.txt', 'w', encoding='utf8') as f:
    f.write(title)
    f.write(subtitle)
    f.write(content)

with open('bitcoin_news.txt', 'r', encoding='utf8') as f:
    content = f.read()

# 내용에서 불필요한 특수문자, 기호 등 제거
filtered_content = content.replace('.', '').replace(',','').replace("'","").replace('·', ' ').replace('=','').replace('"','')
filtered_content = re.sub(r'▶.*','', filtered_content)
filtered_content = re.sub(r'[^\.\?\!\w\d\s]','',filtered_content)
print (filtered_content)

from ckonlpy.tag import Twitter
twitter = Twitter()

# 가상통화, 아시아경제 등 미등록 단어를 사전에 추가로 등록
twitter.add_dictionary('가상통화', 'Noun')
twitter.add_dictionary('아시아경제', 'Noun')
twitter.add_dictionary('한동안', 'Noun')
twitter.add_dictionary('블리클리', 'Noun')
twitter.add_dictionary('공동창립자', 'Noun')
twitter.add_dictionary('부크바', 'Noun')

# 형태소 분석
twitter_morphs = twitter.pos(filtered_content)

# 명사만 추출하기
Noun_words = []
for word, pos in twitter_morphs:
    if pos == 'Noun':
        Noun_words.append(word)
print(Noun_words)

# 불용어 제거를 위한 별도의 사전 구축
# 본문과 상관 없는 아시아 경제, 기자 이름, 기자 단어 제거
# count 했을 때 빈도수가 높지만 본문 주요 내용과 관련이 없는 못, 것, 수, 까지 단어 제거
stopwords = ['아시아경제', '김철현', '기자', '못', '것', '수', '까지']

# unique 하게 명사 추려내기
unique_noun_words = set(Noun_words)

# 불용어 제거하기
for word in unique_noun_words :
    if word in stopwords :
        while word in Noun_words : Noun_words.remove(word)

# 명사 별로 빈도수를 세기
from collections import Counter
c = Counter(Noun_words) # input type should be a list of words (or tokens)
print(c)

# 상위 20개 단어 추출. 20개 까지는 빈도가 3번 이상이나, 그 이하는 빈도가 2 이하임
# 그리고 빈도가 2인 단어는 30개 이상으로 중요 단어를 추출하고자 하는 목적에 맞지 않고, 변별력이 떨어짐
k = 20
print(c.most_common(k)) # 빈도수 기준 상위 k개 단어 출력

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from os import path

FONT_PATH = 'C:\Windows\Fonts\HMFMMUEX.TTC' # For Korean characters

# word cloud 는 string 만 받으므로 string 형태로 만들어주기
noun_text = ''
for word in Noun_words:
    noun_text = noun_text +' '+word
    
# word cloud 만들기
wordcloud = WordCloud(font_path=FONT_PATH,
                      background_color="white",
                      max_font_size=60, relative_scaling=.5).generate(noun_text) 
# generate() 는 하나의 string value를 입력 받음
plt.figure()
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()