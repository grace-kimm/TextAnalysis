# assign08_김은혜.py

import re

import requests
from bs4 import BeautifulSoup 

# 기사 가져오기
def get_article(url):
    # Obtain three types of information about a news article
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(r.text, 'lxml')
    
    news_contents = soup.find('div', id= "articleBodyContents").text
    news_contents = news_contents.replace("// flash 오류를 우회하기 위한 함수 추가", "")
    news_contents = news_contents.replace("function _flash_removeCallback() {}", "")
    news_contents = news_contents.replace("silverpaper@news1.kr", "")
    news_contents = re.sub(r'▶.*','', news_contents)
    news_contents = news_contents.lstrip()
    news_contents = news_contents.rstrip()
    
    return news_contents
    
url = 'https://news.naver.com/main/read.nhn?oid=421&sid1=100&aid=0003646082&mid=shm&mode=LSD&nh=20181018225255'
content = get_article(url)

def get_sentences(text): # 문장 단위로 쪼개 줌
    sentences = re.split(r'[\.\?\!]\s*', text) # '.','?,'!'가 나오면 문장의 끝이라고 가정하고 해당 문자가 나오면 쪼개줌.
    return sentences

# 문장 단위로 content를 쪼개기
final_sentences = get_sentences(content)


# 불필요한 조사, 기호 제거
filtered_sentences = [re.sub(r'[^\s\d\w]','',sent) for sent in final_sentences]
filtered_sentences = [re.sub(r'[은는이가과을를의고에]','',sent) for sent in final_sentences]

# 붙어있는 단어 띄어쓰기
filtered_sentences[0] = filtered_sentences[0].replace('영국독일태국', '영국, 독일, 태국')
filtered_sentences[0] = filtered_sentences[0].replace('정상회담대북제재', '정상회담 대북 제재')
filtered_sentences[0] = filtered_sentences[0].replace('가속화문재인', '가속화 문재인')
filtered_sentences[3] = filtered_sentences[3].replace('방북訪北의사', '방북 의사')
filtered_sentences[-2] = filtered_sentences[-2].replace('비상임이사국2020년까지으로', '비상임이사국 2020년까지 으로')

import nltk

# 단어에 tagging
tagged_words = [nltk.pos_tag(nltk.word_tokenize(sent)) for sent in filtered_sentences]

# Lemmatization
final_words = []
wlem = nltk.WordNetLemmatizer()
for sent in tagged_words:
    noun_sent = []
    for word, pos in sent:
         if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'): # 명사인 단어에 대해서 lemmatizaion
            noun_sent.append(wlem.lemmatize(word))
    final_words.append(noun_sent)

total_nouns = []
for words in final_words:
    total_nouns.extend(words)

# 불용어 제거를 위한 별도의 사전 구축
# count 했을 때 빈도수가 높지만 본문 주요 내용과 관련이 없는 '있다', '데', '문', '것으로' 단어 제거
stopwords = ['있다', '데', '문', '것으로']


# 불용어 제거하기
for word in total_nouns :
    if word in stopwords :
        while word in total_nouns : total_nouns.remove(word)

# 고유한 명사 : 불용어 제거한 버전으로 업데이트
unique_nouns = set(total_nouns)

# 명사 별로 빈도수를 세기
from collections import Counter
c = Counter(total_nouns) # input type should be a list of words (or tokens)

# 상위 10개 단어 추출
NUM_WORDS = 10
top_words = c.most_common(NUM_WORDS)

# 빈도수 제외하고 단어만 담은 리스트 만들기
only_words = []
for first in top_words :
    only_words.append(first[0])

import networkx as nx
import itertools
import matplotlib.pyplot as plt
import time

# 그래프 폰트 지정
import matplotlib.font_manager as fm
from matplotlib import rc
font_name = fm.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

g = nx.Graph()
# 노드 추가
g.add_nodes_from(only_words)
# 관계 추가
for pair in list(itertools.combinations(list(only_words), 2)): 
    if pair[0] == pair[1]:
        continue
    for sent in final_words:
        if pair[0] in sent and pair[1] in sent:
            if pair in list(g.edges()) or (pair[1],pair[0]) in list(g.edges()): 
                g[pair[0]][pair[1]]['weight'] += 1 # tie가 있으면 weight만 추가
            else:
                g.add_edge(pair[0], pair[1], weight=1 )

# 그래프 그리기
pos = nx.shell_layout(g)
nx.degree_centrality(g)

nx.draw_shell(g)
nx.draw_networkx_labels(g, pos, font_family=font_name, font_size=16, font_color = 'black', font_weight='bold')
plt.show()

# gephi를 꺼야 나머지가 실행 됩니다.

# 연결중심도
degree_centrality = nx.degree_centrality(g)
max_degree_value = max(degree_centrality.values())
max_degree_keys = [k for k in degree_centrality if degree_centrality[k] == max_degree_value]
separator = ', '
max_degree_string = separator.join(max_degree_keys)
print('연결중심도는 노드 ' + max_degree_string + '이 가장 높습니다.')


# 매개중심도
betweenness_centrality = nx.betweenness_centrality(g)
max_betweenness_value = max(betweenness_centrality.values())
max_betweenness_keys = [k for k in betweenness_centrality if betweenness_centrality[k] == max_betweenness_value]
separator = ', '
max_betweenness_string = separator.join(max_betweenness_keys)
print('매개중심도는 노드 ' + max_betweenness_string + '이 가장 높습니다.')

# 근접중심도
closeness_centrality = nx.closeness_centrality(g)
max_closeness_value = max(closeness_centrality.values())
max_closeness_keys = [k for k in closeness_centrality if closeness_centrality[k] == max_closeness_value]
separator = ', '
max_closeness_string = separator.join(max_closeness_keys)
print('근접중심도는 노드 ' + max_closeness_string + '이 가장 높습니다.')


# 연결된 단어 보여주기
edges = g.edges()

num = 1
for word in only_words :
    word_list = []
    num +1
    for i, j in edges :
        if i== word :
            word_list.append(j)
        elif j == word :
            word_list.append(i)
    if word in ['평화프로세스', '완화', '프란치스코', '대북제재', '한반도']:
        print('단어 ' + word + '는 ' + str(len(word_list)) + '개의 단어와 연결되어 있습니다.')
    else :
        print('단어 ' + word + '은 ' + str(len(word_list)) + '개의 단어와 연결되어 있습니다.')
    print(word_list)
        