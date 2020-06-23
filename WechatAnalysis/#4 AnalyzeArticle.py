# -*- coding: utf-8 -*-
# @File       : #4 AnalyzeArticle.py
# @Author     : Yuchen Chai
# @Date       : 2020-06-20 14:52
# @Description:
import jieba
import pandas as pd
from WechatAnalysis.NLP_Tool import preprocess as pp
from WechatAnalysis.NLP_Tool import tool
from sklearn.cluster import KMeans

with open("data_article.txt",encoding="utf8") as f:
    mArticles = f.readlines()
    mArticles = list(set(mArticles))
    mArticles = [s.strip() for s in mArticles]
    pass
with open("NLP_Tool/stopwords.txt",encoding="utf8") as f:
    mStopwords = f.readlines()
    mStopwords = [s.strip() for s in mStopwords]

# 读入用户个性化词库
jieba.load_userdict("data_userdict.txt")

# 分词
mArticles_splitted = pp.split_words(mArticles)

# 去除停用词
mArticles_deleteStop = pp.del_stop_split_words(mArticles_splitted,pp.add_words(mStopwords))

mCorpus = []
for item in mArticles_deleteStop:
    temp = ""
    for sub in item:
        temp = temp + sub + " "
        pass
    temp.strip()
    mCorpus.append(temp)
    pass

# 将文本转为词频矩阵
mVector = tool.get_word_frequency_matrix(mCorpus)

# 获得权值矩阵
mMatrix = tool.get_word_tfidf_matrix(mVector)

# 聚类
mCluster = KMeans(n_clusters=50)
mCluster_result = mCluster.fit_predict(mMatrix)

df = pd.DataFrame({"Category":list(mCluster_result),"Text":mCorpus})
df.to_csv("result_article.csv")