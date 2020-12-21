# assign09_김은혜

from os import listdir
from os.path import isfile, join

mypath = './docs/' #화일들이 있는 디렉토리를 정의합니다.
listdir(mypath)  #mypath에 있는 화일들을 보여줍니다.
files = listdir('./docs/')  #읽어드린 file 이름이 리스트형태로 files에 저장됩니다.

import numpy as np
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

#4개 파일 내용을 리스트로 읽어드리기 위해 total_docs를 empty list로 정의하고,
#for loop을 실행시켜 15개 파일의 내용을 차례로 추가합니다.
total_docs = [] 
for file in onlyfiles:
    file_path = mypath+file
    with open(file_path, 'r', encoding='utf8') as f:
        content = f.read()
    total_docs.append(content)  

import my_preprocessing 
#불용어를 정의하고, 불용어 사전 생성합니다.
stopwords = ['be', 'today', 'yesterday', 'new', 'york', 'time']

#total_docs을 전처리하면서 불용어도 제거함. 그러므로 doc_nouns에는 total_docs에서 사용된 명사들만 저장되어 있을 것임.
docs_nouns = [my_preprocessing.En_preprocessing(doc, stopwords) for doc in total_docs]

DOCS_NUM=len(docs_nouns) #document의 숫자입니다.

# corpus, 즉 4개 문서에서 사용된 모든 명사단어를 저장하기 위해 empty 리스트를 만듬.
# 모든 명사 단어들 합침.
total_docs_nouns = [] 
for words in docs_nouns:
    total_docs_nouns.extend(words)
	
len(total_docs_nouns) #494: 4개의 문서에서 사용된 전체 명사 단어수 

#sklearn.feature_extraction.text.CountVectorizer는 텍스트 문서 모음을 토큰 수가 원소인 matrix로 변환합니다.
from sklearn.feature_extraction.text import CountVectorizer # frequency based DTM

#class sklearn.feature_extraction.text.TfidfVectorizer는 원시 문서 컬렉션을 TF-IDF 단어(feature) 매트릭스로 변환합니다.
from sklearn.feature_extraction.text import TfidfVectorizer # tf-idf based DTM

# returns a frequency-based DTM: 
def tf_extractor(corpus): 
    vectorizer = CountVectorizer(min_df=1, ngram_range=(1,1))
    features = vectorizer.fit_transform(corpus) # transform texts to a frequency matrix
    return vectorizer, features    

# returns a tf-idf based DTM
def tfidf_extractor(corpus):
    vectorizer = TfidfVectorizer(min_df=1, ngram_range=(1,1))
    features = vectorizer.fit_transform(corpus)
    return vectorizer, features
	
#15개 문서 각각에 대해, 각 문서의 명사 단어로 된 리스트를 만듬.
# 불필요한 단어들을 제거하고 난후 DTM로 변환하기 위해 다시 list of strings의 형태로 변환
documents_filtered = []
for doc in docs_nouns:
    document_filtered =''
    for word in doc:
        document_filtered = document_filtered+' '+word
    documents_filtered.append(document_filtered) # list of docs, 각 doc은 단어들로 구성이 된 string data

vectorizer_tfidf, DTM_tfidf = tfidf_extractor(documents_filtered) # 문서들을 TFIDF 기반 DTM으로(matrix) 변환
print(DTM_tfidf.toarray())

DTM_TFIDF = np.array(DTM_tfidf.todense())
DTM_TFIDF.shape
print(DTM_TFIDF)

vectorizer_tf, DTM_tf = tf_extractor(documents_filtered) # 문서들을 TF 기반 DTM으로 (matrix) 변환
print(DTM_tf.toarray())

DTM_TF = np.array(DTM_tf.todense()) #dense array (즉, 0을 포함한 array)로 변환후 다시 numpy array로 변환
DTM_TF.shape                        # row는 문서의 수, column은 최종적으로 사용된 단어의 수
print(DTM_TF)

#TF: Term Frequency. 특정 단어가 문서에서 얼마나 자주 등장하는지 나타내는 값.
#이 값이 클수록, 즉 단어가 반복적으로 사용될 수록 문서에서 그 단어가 중요함.
d1d1_tf = np.linalg.norm(DTM_TF[0]-DTM_TF[1])
d1d2_tf = np.linalg.norm(DTM_TF[0]-DTM_TF[2])
d1d3_tf = np.linalg.norm(DTM_TF[0]-DTM_TF[3])
print(d1d1_tf, d1d2_tf, d1d3_tf)
#문서간 거리가 가까울수록 유사하다고 말할 수 있으므로 한 군집에 속할 확률이 높다.

#TF-IDF: IDF는 Inverse of DF이므로 DF를 정의하면 IDF는 이해가 가능합니다.
#DF는 Document Frequency의 약자로 단어가 문서군 내에서 자주 사용되는 경우, 그 단어가 흔하게 등장한다는 의미입니ㅣ다.
#TF-IDF값은 TF와 IDF 값의 곱셈으로 계산되는데, TF값과 IDF값이 클때 커집니다.
#즉, TF 값이 크다는 것은 단어 t가 해당문서에서 많이 사용되고, IDF 크다는 것은 단어 t가 사용된 문서가 적다는 것을 의미합니다.
#즉, TF-IDF 값은 하나의 단어 t가 해당 문서에서 얼마나 고유하게 사용되었느냐를 나타냅니다.
d1d1_tfidf = np.linalg.norm(DTM_TFIDF[0]-DTM_TFIDF[1])
d1d2_tfidf = np.linalg.norm(DTM_TFIDF[0]-DTM_TFIDF[2])
d1d3_tfidf = np.linalg.norm(DTM_TFIDF[0]-DTM_TFIDF[3])
print(d1d1_tfidf, d1d2_tfidf, d1d3_tfidf) 

#Term Frequency 기반 코사인 유사도
d1d2_cos_tf = np.dot(DTM_TF[0],DTM_TF[1])/(np.linalg.norm(DTM_TF[0])*np.linalg.norm(DTM_TF[1]))
d1d4_cos_tf = np.dot(DTM_TF[0],DTM_TF[2])/(np.linalg.norm(DTM_TF[0])*np.linalg.norm(DTM_TF[2]))
d1d6_cos_tf = np.dot(DTM_TF[0],DTM_TF[3])/(np.linalg.norm(DTM_TF[0])*np.linalg.norm(DTM_TF[3]))
print(d1d2_cos_tf, d1d4_cos_tf, d1d6_cos_tf)

#TF-IDF기반 코사인 유사도를 갖고도 수행
d1d2_cos_tfidf = np.dot(DTM_TFIDF[0],DTM_TFIDF[1])/(np.linalg.norm(DTM_TFIDF[0])*np.linalg.norm(DTM_TFIDF[1]))
d1d4_cos_tfidf = np.dot(DTM_TFIDF[0],DTM_TFIDF[2])/(np.linalg.norm(DTM_TFIDF[0])*np.linalg.norm(DTM_TFIDF[2]))
d1d6_cos_tfidf = np.dot(DTM_TFIDF[0],DTM_TFIDF[3])/(np.linalg.norm(DTM_TFIDF[0])*np.linalg.norm(DTM_TFIDF[3]))
print(d1d2_cos_tfidf, d1d4_cos_tfidf, d1d6_cos_tfidf)
#코싸인 유사도는 동일한 방향 이면 1, 다른 방향이면 -1, 수직이면 0. --> Doc1과 Doc2가 제일 유사함

# 유클리디안거리 : doc1과 doc2가 제일 가까움
dis1_eucli = np.linalg.norm(DTM_TFIDF[0]-DTM_TFIDF[1])
dis2_eucli = np.linalg.norm(DTM_TFIDF[0]-DTM_TFIDF[2])
dis3_eucli = np.linalg.norm(DTM_TFIDF[0]-DTM_TFIDF[3])

print(dis1_eucli, dis2_eucli, dis3_eucli)

# 유클리디안 거리가 가깝고, 코사인 유사도가 높은 문서 1과 문서 2가 제일 유사하다.