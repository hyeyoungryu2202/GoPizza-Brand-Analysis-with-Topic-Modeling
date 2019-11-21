#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import gensim
from gensim import corpora

# libraries for visualization
import pyLDAvis
import pyLDAvis.gensim


# In[2]:


address_dict = {"대치본점" : "서울 강남구 삼성로 301",
                "평촌학원가점" : "경기 안양시 동안구 평촌대로 131",
                "홍성점" : "충남 홍성군 홍성읍 아문길29번길 67", 
                "진주경상대점":"경상남도 진주시 가좌동 868-33",
                "홍대상수점":"서울 마포구 독막로19길 32",
                "부산동아대점":"부산 서구 구덕로 220",
                "숭실대점":"서울 동작구 상도로 362-1",
                "일산라페스타점": "경기 고양시 일산동구 중앙로1275번길 38-5",
                "화성병점점": "경기 화성시 효행로 1060",
                "인천구월nc점": "인천 남동구 인하로 485 뉴코아아울렛",
                "일산후곡점": "경기 고양시 일산서구 일산로 547",
                "노량진점": "서울 동작구 노량진로16길 22-1",
                "수지구청점": "경기 용인시 수지구 풍덕천로 135",
                "상현역점": "경기 용인시 수지구 광교중앙로 305",
                "성남수진역점": "경기 성남시 중원구 원터로 116",
                "수원행궁동점": "경기 수원시 팔달구 정조로892번길 4",
                "부산광복점": "부산 중구 광복로97번안길 8",
                "고양어린이박물관점": "경기 고양시 덕양구 화중로 26",
                "마이크임펙트스튜디오점": "서울 강남구 역삼로 180"}

for key in address_dict:
    try:
        globals()[str(key)+"_saved_df"] = pd.read_csv('/Users/angieryu2202/Desktop/'+str(key)+'_df.tsv', sep='\t')
        globals()[str(key)+'_data_words']=[]
        for words in globals()[str(key)+"_saved_df"]['tokenized_abstract']:
            words = words.replace('[','').replace(']','').replace("'",'').replace(',','')
            globals()[str(key)+'_data_words'].append(words.strip().split())
        dictionary = corpora.Dictionary(globals()[str(key)+'_data_words'])
        globals()[str(key)+"_doc_term_matrix"] = [dictionary.doc2bow(rev) for rev in globals()[str(key)+'_data_words']]
        # Creating the object for LDA model using gensim library
        LDA = gensim.models.ldamodel.LdaModel
        # Build LDA model
        globals()[str(key)+"_lda_model"] = LDA(corpus=globals()[str(key)+"_doc_term_matrix"], id2word=dictionary, num_topics=10, random_state=100, chunksize=1000, passes=50)
        print(globals()[str(key)+"_lda_model"].print_topics())
    except:
        pass


# In[10]:


for key in address_dict:
    # Visualize the topics
    pyLDAvis.enable_notebook()
    globals()[str(key)+"_vis"] = pyLDAvis.gensim.prepare(globals()[str(key)+"_lda_model"], globals()[str(key)+"_doc_term_matrix"] , dictionary, sort = True)
    globals()[str(key)+"_vis"]


# In[ ]:




