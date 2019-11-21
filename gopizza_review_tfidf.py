#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
pizza_df = pd.read_csv('/Users/angieryu2202/Desktop/전체피자요기요리뷰.tsv', sep= '\t')
대치본점_df = pizza_df.loc[pizza_df['location'] == '대치본점']
평촌학원가점_df = pizza_df.loc[pizza_df['location'] == '평촌학원가점']
홍성점_df = pizza_df.loc[pizza_df['location'] == '홍성점']
진주경상대점_df = pizza_df.loc[pizza_df['location'] == '진주경상대점']
홍대상수점_df = pizza_df.loc[pizza_df['location'] == '홍대상수점']
부산동아대점_df = pizza_df.loc[pizza_df['location'] == '부산동아대점']
숭실대점_df = pizza_df.loc[pizza_df['location'] == '숭실대점']
일산라페스타점_df = pizza_df.loc[pizza_df['location'] == '일산라페스타점']
화성병점점_df = pizza_df.loc[pizza_df['location'] == '화성병정점']
인천구월nc점_df = pizza_df.loc[pizza_df['location'] == '인천구월nc점']
일산후곡점_df = pizza_df.loc[pizza_df['location'] == '일산후곡점']
노량진점_df = pizza_df.loc[pizza_df['location'] == '노량진점']
수지구청점_df = pizza_df.loc[pizza_df['location'] == '수지구청점']
상현역점_df = pizza_df.loc[pizza_df['location'] == '상현역점']
성남수진역점_df = pizza_df.loc[pizza_df['location'] == '성남수진역점']
수원행궁동점_df = pizza_df.loc[pizza_df['location'] == '수원행궁동점']
부산광복점_df = pizza_df.loc[pizza_df['location'] == '부산광복점']
고양어린이박물관점_df = pizza_df.loc[pizza_df['location'] == '고양어린이박물관점']
마이크임펙트스튜디오점_df = pizza_df.loc[pizza_df['location'] == '마이크임펙트스튜디오점']


# In[2]:


def text_punc_num_remover (df_col_value, df_col_name):
    import string
    from string import digits
    translator = str.maketrans('', '', string.punctuation)
    punc_removed_column = []
    for line in df_col_value:
        punc_removed_column.append(line.translate(translator))
    #print(punc_removed_column)
    remove_digits = str.maketrans('', '', digits)
    globals()[str(df_col_name)+"_punc_num_removed"] = []
    for item in punc_removed_column:
        globals()[str(df_col_name)+"_punc_num_removed"].append(item.translate(remove_digits))
    print("punc_num_removed")

remove_words = ['\n', '|', '🖒', '~', ',' , '!', '?', '^', '@', '>', '<', 'ㅡ', '😀', ';', '.', '❤️', '👍', '💕', '♡', '❤', '😠', '🤒', '😡', '🤣','🤩','🤗', 'ㅋ', 'ㅎ', 'ㅅ','ㅂ', 'ㅠ', 'ㅜ', '🍕', '💓', '🧡', '💛', '💚', '💙', '💜', '❣️', '💓', '💖', '💗', '💞']
def spec_charac_remover(remove_words, df_col_name, punc_num_removed_text):
    globals()[str(df_col_name) + "_preprocessed"] = []
    for i in punc_num_removed_text:
        temp = []
        for k in i.split(" "):
            if not any(i for i in remove_words if i in k):
                temp.append(k)
        globals()[str(df_col_name) + "_preprocessed"].append(" ".join(temp))
    print("spec_charac_removed")

def noun_tokenizer(df_col_name, preprocessed_df):
    from konlpy.tag import Komoran
    komoran = Komoran()
    globals()["noun_"+str(df_col_name)] = []
    i=0
    for words in preprocessed_df:
        i += 1
        globals()["noun_" + str(df_col_name)].append(komoran.nouns(words))
        print('row ' + str(i) + ' finished')
    print("noun_tokenized")


# In[3]:


def text_preprocessor(location):
    text_punc_num_remover(globals()[str(location)+"_df"]['content'], str(location))
    spec_charac_remover(remove_words, str(location), globals()[str(location)+"_punc_num_removed"])
    noun_tokenizer(str(location), globals()[str(location) + "_preprocessed"])
    globals()[str(location)+"_df"]['tokenized_abstract']=globals()["noun_"+str(location)]
    globals()[str(location)+"_df"].to_csv('/Users/angieryu2202/Desktop/'+str(location)+"_df.tsv", sep = '\t')


# In[4]:


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
    text_preprocessor(key)


# In[5]:


import pandas as pd
pizza_saved_tuple = []
for key in address_dict:
    globals()[str(key)+"_saved_df"] = pd.read_csv('/Users/angieryu2202/Desktop/'+str(key)+"_df.tsv", sep = '\t')
    pizza_saved_tuple.append(globals()[str(key)+"_saved_df"])
pizza_saved_df = pd.concat(pizza_saved_tuple)


# In[6]:


# 와ㅏ 진짜 드디어 만들었다ㅜㅜㅜㅜㅜ
def tfidf_scatter_plotter (abstracts, docu_year):
    import pandas as pd
    import matplotlib.font_manager as fm
    import matplotlib.pyplot as plt
    from matplotlib import rc
    from sklearn.manifold import TSNE
    from sklearn.feature_extraction.text import TfidfVectorizer
    for abstract in abstracts:
        abstract = ' ' + abstract.replace("',","").replace("['","").replace("']","").replace("'","")
    tfidf = TfidfVectorizer(max_features = 100, max_df=0.95, min_df=0)
    #generate tf-idf term-abstracts matrix
    globals()["tfidf_matrix_"+str(docu_year)] = tfidf.fit_transform(abstracts)#size D x V
    
    #tf-idf features
    globals()["tfidf_features_"+str(docu_year)] = tfidf.get_feature_names()
    for tfidf_dict_word in globals()["tfidf_features_"+str(docu_year)]:
        tfidf_dict_word.replace("'","")
    globals()["data_array_"+str(docu_year)] = globals()["tfidf_matrix_"+str(docu_year)].toarray()
    data = pd.DataFrame(globals()["data_array_"+str(docu_year)], columns=globals()["tfidf_features_"+str(docu_year)])
    print(data.shape)
    # TF-IDF를 사용하여 단어의 중요도를 산출하였고, 선택된 100개의 단어를 t-SNE로 시각화 하였다. t-SNE는 고차원(100차원)상에 존재하는 데이터의 유사성들을 KL-divergence가 최소화되도록 저차원(2차원)으로 임베딩시키는 방법이다.
    tsne = TSNE(n_components=2, n_iter=10000, verbose=1)
    print(globals()["data_array_"+str(docu_year)].shape)
    print(globals()["data_array_"+str(docu_year)].T.shape)
    Z = tsne.fit_transform(globals()["data_array_"+str(docu_year)].T)
    print(Z[0:5])
    print('Top words: ',len(Z))


# In[7]:


def tfidf_table_maker(tfidf_matrix, feature_names, data_array, docu_year):
    import pandas as pd
    import operator
    indices = zip(*tfidf_matrix.nonzero())
    globals()["tfidf_dict_"+str(docu_year)] = {}
    for row,column in indices:
        globals()["tfidf_dict_"+str(docu_year)][feature_names[column]] = data_array[row, column]
    globals()["tfidf_dict_"+str(docu_year)] = sorted(globals()["tfidf_dict_"+str(docu_year)].items(), key=lambda x: (-x[1], x[0]))
    globals()["tfidf_dict_df_"+str(docu_year)] = pd.DataFrame(globals()["tfidf_dict_"+str(docu_year)], columns=['keywords','tfidf_score'])
    print(globals()["tfidf_dict_df_"+str(docu_year)].head(30))


# In[8]:


def tfidf_rank_bar_plotter (tfidf_df, tfidf_score, keywords, docu_year):
    import matplotlib.pyplot as plt
    from matplotlib import rc
    import numpy as np
    rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams["font.size"] = 12
    plt.rcParams["figure.figsize"] = (20,15)
    plt.ylabel('Keyword',rotation=90)
    plt.xlabel('TF-IDF Score')
    tfidf_df = tfidf_df.sort_values(by = str(tfidf_score), ascending=True)
    y_pos = np.arange(len(tfidf_df[-30:].keywords))
    # Create horizontal bars
    plt.barh(y_pos, tfidf_df[-30:].tfidf_score, color='#86bf91')
    # Create names on the y-axis
    plt.yticks(y_pos, tfidf_df[-30:].keywords)
    plt.title('Pizza '+docu_year+' TF-IDF Score Rank')
    plt.savefig('/Users/angieryu2202/Desktop/'+docu_year+'_tfidf_rank_barplot.png', bbox_inches='tight')


# In[9]:


for key in address_dict:
    try:
        globals()[str(key)+"_nouns"] = globals()[str(key)+"_saved_df"]['tokenized_abstract']
        tfidf_scatter_plotter(globals()[str(key)+"_nouns"], str(key))
        tfidf_table_maker(globals()["tfidf_matrix_"+str(key)], globals()["tfidf_features_"+str(key)], globals()["data_array_"+str(key)], str(key))
        tfidf_rank_bar_plotter(globals()["tfidf_dict_df_"+str(key)], 'tfidf_score', 'keywords', str(key))
    except:
        pass


# In[ ]:




