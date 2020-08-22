import os
import json
import gensim
import random
from os.path import isfile, isdir, join

# 需要被計算的分類
myTypes = ['animal', 'vehicle',  'food', 'fashion', 'dog', 'cat', 'car', 'motorcycle']

# 計算完網紅權重存放的位置
scorePath = "..\\data\\score"

# getUsersData.py儲存網紅貼文資料的json檔案，拿來計算分數
usersDataFile = "..\\data\\usersData.json"
with open(usersDataFile, 'r') as load_f:
    usersData = json.load(load_f)

# 訓練好的Word2Vec model的存放位置，該位置只能放Word2Vec Model，否則會拋出例外
modelPath = "..\\data\\model\\"

def getScore(model):
    
    new_dic = {}
    scoreFile = ("{}\\{}.json".format( scorePath, model ) )
    
    if not os.path.exists(scoreFile):
        with open(scoreFile,"w") as dump_f:
            new_dic['50'] = list()
            new_dic['100'] = list()
            new_dic['150'] = list()
            new_dic['200'] = list()
            new_dic['250'] = list()
            new_dic['300'] = list()
            json.dump(new_dic,dump_f)
    
    with open(scoreFile,'r') as load_f:
        load_dict = json.load(load_f)


    print('載入 {} model 中...'.format(model))
    if 'bin' in model:
        word_vectors = gensim.models.KeyedVectors.load_word2vec_format( ('D:\\word2vec\\model\\{}'.format(model)), binary=True )
    else:
        word_vectors = gensim.models.KeyedVectors.load_word2vec_format( ('D:\\word2vec\\model\\{}'.format(model)), binary=False )
    print('載入完畢!')


    for user in usersData:
        print('\n')
        print( user )
        print('\n')
        countPost = 0
        countLike = 0
        countComment = 0
        imageScoreDic = {}
        videoScoreDic = {}
        
        # 換帳號，圖片分類分數初始化
        countImages = 0
        for t in myTypes:
            imageScoreDic[t] = 0

        # 換帳號，影片分類分數初始化
        countVideos = 0
        for t in myTypes:
            videoScoreDic[t] = 0


        for timestamp in usersData[user]['data']:
            
            if usersData[user]['data'][timestamp]['labels'] != 'igtv':
                
                countPost += 1
                countLike += usersData[user]['data'][timestamp]['likes']
                countComment += usersData[user]['data'][timestamp]['comments']
                
                if usersData[user]['data'][timestamp]['is_video']:
                    countVideos += 1
                else:
                    countImages += 1

                if len(usersData[user]['data'][timestamp]['labels']) >= 1:

                    for t in myTypes:
                        
                        maxScore = 0
                        maxScore2 = 0

                        for label in usersData[user]['data'][timestamp]['labels']:


                            try:
                                score = word_vectors.similarity(t, label)
                            except:
                                score = 0
                            

                        if usersData[user]['data'][timestamp]['is_video']:
                            videoScoreDic[t] += maxScore
                            
                        else:
                            imageScoreDic[t] += maxScore


            if  countPost != 0 and countPost % 50 == 0 :
                print(countPost)
                users = { load_dict[str(countPost)][i]['name']:i for i in range( 0, len(load_dict[str(countPost)]) ) }
                try:
                    currentImgScoreDic = { t:round(imageScoreDic[t]/countImages*100, 3) for t in myTypes }
                except :
                    currentImgScoreDic = {}
                    print("目前沒有圖片")
                try:
                    currentVideoScoreDic = { t:round(videoScoreDic[t]/countVideos*100, 3) for t in myTypes }
                except :
                    currentVideoScoreDic = {}
                    print("目前沒有影片")
                    
                if user in users:
                    load_dict[str(countPost)][ users[user] ]['follower'] = usersData[user]['followers']
                    load_dict[str(countPost)][ users[user] ]['like'] = round( countLike/countPost, 3)
                    load_dict[str(countPost)][ users[user] ]['comment'] = round(countComment/countPost,3)
                    load_dict[str(countPost)][ users[user] ]['image']['amount'] = countImages
                    load_dict[str(countPost)][ users[user] ]['image']['score'] = currentImgScoreDic
                    load_dict[str(countPost)][ users[user] ]['video']['amount'] = countVideos
                    load_dict[str(countPost)][ users[user] ]['video']['score'] = currentVideoScoreDic
                    load_dict[str(countPost)][ users[user] ]['ERate'] = round( ((countLike/countPost)+(countComment/countPost))/usersData[user]['followers'], 5 )
                else:
                    new_dic = {}
                    new_dic['name'] = user
                    new_dic['follower'] = usersData[user]['followers']
                    new_dic['like'] = round( countLike/countPost, 3)
                    new_dic['comment'] = round(countComment/countPost,3)
                    new_dic['image'] = {}
                    new_dic['image']['amount'] = countImages
                    new_dic['image']['score'] = currentImgScoreDic
                    new_dic['video'] = {}
                    new_dic['video']['amount'] = countVideos
                    new_dic['video']['score'] = currentVideoScoreDic
                    new_dic['ERate'] = round( ((countLike/countPost)+(countComment/countPost))/usersData[user]['followers'], 5 )

                    load_dict[str(countPost)].append( new_dic )
            
            if( countPost == 300 ):
                break

        if countPost < 300:
                
            if countPost > 250:
                countPost = 300
            elif countPost > 200:
                countPost = 250
            elif countPost > 150:
                countPost = 200
            elif countPost > 100:
                countPost = 150
            elif countPost > 50:
                countPost = 100
            else:
                countPost = 50
            
            users = { load_dict[str(countPost-50)][i]['name']:i for i in range( 0, len(load_dict[str(countPost-50)]) ) }
            finalDic = load_dict[str(countPost-50)][ users[user] ]
            while countPost <= 300:
                users = { load_dict[str(countPost)][i]['name']:i for i in range( 0, len(load_dict[str(countPost)]) ) }
                if user in users:
                    load_dict[str(countPost)][ users[user] ] = finalDic
                else:
                    load_dict[str(countPost)].append( finalDic )
                
                countPost += 50
        
        with open(scoreFile, "w") as dump_f:
            json.dump(load_dict, dump_f)


if __name__ == '__main__':

    if not os.path.exists(scorePath):
        os.mkdir(scorePath)
    
    for f in os.listdir(modelPath):
        
        fullpath = join(modelPath, f)
        
        if isfile(fullpath):
            getScore(f)

    # print( usersData )
