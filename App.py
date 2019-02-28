from flask import Flask,jsonify,request
import random
import pandas as pd
import json
import numpy as np
from scipy.stats import pearsonr
##########global variable##########
session=[]#存储uerid判断新老用户
Mlist=[]#存储movie id 防止重复评论
commit=[]#存储用户评分，判断是否够10个
df = pd.DataFrame(pd.read_csv('E:\document\movieId.csv', header=0))
app = Flask(__name__)
####some function without route####
def genRandom():#生成随机数，防止重复
    df = pd.DataFrame(pd.read_csv('E:\document\movieId.csv', header=0))
    # print(df.head(n=5))
    col = df.iloc[:, 1].values
    index = int(random.sample(list(col), 1)[0])
    if index in Mlist:
        genRandom()
    else:
        Mlist.append(index)
        return index
def getItem(id):#返回随机数对应的电影id的一行数据
    url = "https://movielens.org/movies/"+str(id)
    df = pd.DataFrame(pd.read_csv('E:\document\movies.csv', header=0))
    l = list(df['movieId'])
    if id in l:
        f = l.index(id)
        item = df[f:f + 1]
        jsonString = item.to_json(orient='records')
        js = json.loads(jsonString)[0]
        js.pop('genres')
        js['url']=url
        return str(js)

############推荐系统价值百万的核心算法###############
def movie():#不需要输入，输出一个数组电影的序号
    movieId =df['movieId'].tolist()#取出movieId一列
    midBook = list(set(movieId))#做成码本1235
    midBook = sorted(midBook)
    return midBook

def user():#不需要输入，输出一个数组用户id的序号
    userId = df['userId'].tolist()  # 取出userId一列
    uidBook = list(set(userId))  # 做成码本
    uidBook = sorted(uidBook)
    return uidBook

def vectorize(user):#需要输入，输入一个用户的id，从csv中取出该id的所有movie和rating，按照电影码本返回一个向量，等待循环调用
    dic = {}
    vec = []
    userDf = df[df['userId'].isin([user])]
    umovieId = userDf['movieId'].tolist()
    urating = userDf['rating'].tolist()
    length = len(userDf['movieId'])
    for i in range(length):
        dic[umovieId[i]]=urating[i]
    for i in range(len(movieId)):
        if movieId[i] in umovieId:
            j = umovieId.index(movieId[i])
            vec.append(urating[j])
        else:
            vec.append(0)
    return vec

def matrix_():#返回完整各个用户的评分矩阵，调用上一个函数产生向量，整合向量，返回一个二维数组
    m=[]
    m_0 = uservec()
    m.append(m_0)
    for user in userId:
        vec = vectorize(user)
        m.append(vec)
    return m

def similarity(u1, u2):#课间计算相似度的算法，等待调用
    r, _ = pearsonr(_matrix[u1], _matrix[u2])
    return r

def bestNeighbor():#返回一个字典，键为userid，值为对应的user和0的相似度，是相似度最高的10个人的集合
    l = []
    top = []
    topId = {}
    for i in range(len(_matrix)):
        if i != 0:
            l.append(similarity(0,i))
    orderL = sorted(l,reverse=True)
    for i in range(10):
        top.append(orderL[i])
    for i in top:
        id = l.index(i)
        topId[id]=i
    return topId

def final(): #返回一个二维数组，最终用来做推荐的10人评分矩阵
    bestM = []#一会要给他初始化一个用户喜欢
    m = uservec()
    bestM.append(m)
    for i in topId:
        bestM.append(_matrix[i])
    return bestM

def preForSingleItem(item): #返回单一电影的预测值，数字,等待调用
    m = final()
    fz = 0
    fm = 0
    r_mean_0 = np.mean([r for r in m[0] if r > 0])
    for u in range(len(m)):
        r_mean = np.mean([r for r in m[u] if r > 0])
        sim = similarity(u, 0)
        fm = fm + sim
        fz = fz + sim * (_matrix[u][item] - r_mean)
    pred = r_mean_0+(fz/fm)
    return pred

def preTop():#返回所有电影按照预测值排序的数组，数组里放的是movieid
    m = final()
    order = []
    topOrder = []
    idSet=[]
    for i in range(len(m[0])):
        pred = preForSingleItem(i)
        order.append(pred)
    topOrder = sorted(order,reverse=True)
    for i in topOrder:
        id = order.index(i)
        idSet.append(id)
    return idSet
def uservec():
    dic = {}
    vec = []
    ml = []
    rl = []
    for i in range(10):
        mo = commit[i]['movie_id']
        mark = int(commit[i]['rating'][-1:])
        ml.append(mo)
        rl.append(mark)
    for i in range(len(ml)):
        dic[ml[i]] = rl[i]
    for i in range(len(movieId)):
        if movieId[i] in ml:
            j = ml.index(movieId[i])
            vec.append(rl[j])
        else:
            vec.append(0)
    return vec
# def test():
#     l=[]
#     for i in range(1235):
#        l.append(0)
#     l[0]=1
#     l[22]=2
#     l[245]=5
#     l[360]=3
#     l[467]=4
#     l[603]=3
#     l[733]=5
#     l[850]=2
#     l[965]=1
#     l[1135]=4
#     return l
def finalM():
    favor = []
    dic = {}
    movi = []
    t = preTop()
    reply={}
    for i in range(n):
        favor.append(t[i])
    for i in favor:
        js = eval(getItem(i))
        dic = {"title":js['title'],"url":js["url"]}
        movi.append(dic)
    reply["movies"]=movi
    return reply


####################返回新老用户####################
@app.route('/register',methods=['POST'])
def register():
    chat_id = request.form.get('chat_id')
    if chat_id in session:
        res = {"exists": 1}
        return str(res)
    else:
        session.append(chat_id)
        res = {"exists": 0}
        return str(res)
####################返回json字符串包含电影信息和链接###################
@app.route('/get_unrated_movie',methods=['POST'])
def get_unrated_movie():
    chat_id = request.form.get('chat_id')
    index = genRandom()
    res = getItem(index)
    return res
####################添加用户rating到数组返回状态####################
@app.route('/get_unrated_movie/status',methods=['POST'])
def status():
    values = request.form.get('values')
    js = eval(values)
    if js['chat_id']!="" and js['movie_id']!="" and js['rating']!="":
        commit.append(js)
        res = str({"status": "success"})
        print(commit)
        return res
    else:
        res = str({"status": "failed"})
        return res

@app.route('/recommend',methods=['POST'])
def recommend():
    values = request.form.get('values')
    js = eval(values)
    global n
    n = js['top_n']
    global userId
    global topId
    global _matrix
    global movieId
    global m
    global t
    movieId = movie()  # 电影码本
    userId = user()  # 用户码本
    _matrix = matrix_()  # 评分矩阵
    topId = bestNeighbor()  # 10人相似度字典
    m = final()
    t = preTop()
    back = finalM()
    return str(back)

@app.route('/',methods=['POST'])
def loadCommmands():
   return 'mo'


if __name__ == '__main__':
    app.run(debug=True)
