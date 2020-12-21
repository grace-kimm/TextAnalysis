import pickle

# 자료를 new_dict에 넣기
with open('./total_sections_morphs.p', 'rb') as f :
    new_data = pickle.load(f)
print(len(new_data.values())) # 7837개 기사

# 데이터 파악 단계
import pandas as pd
df =pd.DataFrame.from_dict(new_data, orient='index')

# 명사 추출 단계
import nltk
import re
# 명사만 포함 & 중복 제거한 딕셔너리 만들기
df_noun = {}
        
for i in range(7837) :
    NN_words = []
    for word, pos in df['content'][i] :
        if 'Noun' in pos :
            NN_words.append(word)
    df_noun[i] = NN_words

# 불용어 리스트에 있으면 불용어 제거
with open('stop_words.txt', 'r', encoding='UTF-8') as f:
    stopwords_list = f.read().splitlines()

for i in range(7837) :
    for word in df_noun[i]:
        if word in stopwords_list:
            while word in df_noun[i]: df_noun[i].remove(word)


# 빈도수 기준으로 불용어 제거

from collections import defaultdict

term_fre_dict = defaultdict(int)
doc_fre_dict = defaultdict(int)

for key in df_noun:
    for word in df_noun[key]:
        term_fre_dict[word] += 1
    for word in set(df_noun[key]):
        doc_fre_dict[word] += 1

max_doc_frequency = 1000
min_doc_frequency = 3
max_term_frequency = 7000
min_term_frequency = 5

doc_frequency_filtered = {k:v for k, v in doc_fre_dict.items() if ((v>=min_doc_frequency) and (v <= max_doc_frequency))}
term_frequency_filtered = {k:v for k, v in term_fre_dict.items() if ((v>=min_term_frequency) and (v <= max_term_frequency))}
both_satisfied = {k:v for k, v in term_frequency_filtered.items() if k in doc_frequency_filtered}

print(both_satisfied) # 조건 만족하는 단어 확인

for i in range(7837) :
    for word in df_noun[i]:
        if word not in both_satisfied :
            while word in df_noun[i]: df_noun[i].remove(word)


# 역토큰화 (토큰화 작업을 역으로 되돌림)
detokenized_doc = []
for i in range(len(df_noun)):
    t = ' '.join(df_noun[i])
    detokenized_doc.append(t)

print(detokenized_doc[1]) # 정보 확인

# Vectorization. TF-IDF Vectorizer 이용
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(smooth_idf=True)
X = vectorizer.fit_transform(detokenized_doc)

print(X.shape) # TF-IDF 행렬의 크기 확인

# Topic Modeling
import gensim
from gensim import corpora
dictionary = corpora.Dictionary(df_noun.values())

corpus = [dictionary.doc2bow(text) for text in df_noun.values()]
print(corpus[1]) # 수행된 결과에서 두번째 뉴스 출력

len(dictionary) # dictionary 규모 확인

NUM_TOPICS = 32
NUM_TOPIC_WORDS = 15

ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
topics = ldamodel.print_topics(num_words=NUM_TOPIC_WORDS)

# 토픽 별 분포 확인
for topic in topics:
    print(topic)

# 토픽 별 단어와 분포를 txt 파일로 저장
with open("total_results_test.txt", "w") as f:
    for i in range(NUM_TOPICS) :
        f.write('Topic ' + str(i) + '\n단어\t분포\n------------------------\n')
        for j in range(15) :
            f.write(dictionary[ldamodel.get_topic_terms(i, 15)[j][0]] + '\t' + str(ldamodel.get_topic_terms(i, 15)[j][1]) + '\n')
        f.write('\n')