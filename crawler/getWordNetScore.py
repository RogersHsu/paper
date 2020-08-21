import os
import json
import gensim
from nltk.corpus import wordnet as wn
from itertools import combinations #計算排列組合 


# 需要被計算的分類
myTypes = ['animal', 'vehicle',  'food', 'fashion', 'dog', 'cat', 'car', 'motorcycle']

# 計算完網紅權重存放的位置
scorePath = "D:\\instagram\\score"

# getUsersData.py儲存網紅貼文資料的json檔案，拿來計算分數
usersDataFile = "D:\\instagram\\usersData.json"
with open(usersDataFile, 'r') as load_f:
    usersData = json.load(load_f)


def get_similar_words(words):

    words = [w.lower() for w in words]

    if len(words) > 1:
        maxScore = 0
        firstWord = ''
        secondWord = ''

        labelCom = list(combinations(words, 2)) #計算所有label內的排列組合
        for i in labelCom: #labelCom 為排列組合的結果
            labelMean1 = wn.synsets(i[0])#取出每個計算詞的詞性
            labelMean2 = wn.synsets(i[1])

            for j in labelMean1:
                for k in labelMean2:
                    if j.wup_similarity(k) is not None:#因有可能出現計算結果為None的狀況 所以需要排除
                        if j.wup_similarity(k) > maxScore:
                            maxScore = j.wup_similarity(k)
                            firstWord = j
                            secondWord = k

                            print("兩個詞的語意獲得最高分(語意相近)")
                            print("score : {}".format(maxScore))
                            print("firstWord : {}".format(firstWord))
                            print("secondWord : {}".format(secondWord))
                            print("\n")

        if type(firstWord) == type('') :
            return get_similar_words( list(words[0]) )
        else:
            print(firstWord, firstWord.definition())
            print(secondWord, secondWord.definition())
            print('\n')
            return [firstWord, secondWord]

    else:
        synSetList = []
        for i in range(len(words)):
            labelMean1 = wn.synsets(words[i])
            for j in labelMean1:
                synSetList.append(j)

        return synSetList


def getWordNetScore(model):
    
    new_dic = {}
    scoreFile = ("{}\\{}.json".format( scorePath, model ) )
    print(scoreFile)
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
             
            countPost += 1
            countLike += usersData[user]['data'][timestamp]['likes']
            countComment += usersData[user]['data'][timestamp]['comments']
            
            if usersData[user]['data'][timestamp]['is_video']:
                countVideos += 1
            else:
                countImages += 1

            if 'labels' not in usersData[user]['data'][timestamp]:
                print( user )
                print( timestamp )
                print( usersData[user]['data'][timestamp] )

            if len(usersData[user]['data'][timestamp]['labels']) > 0:

                synsetWords = get_similar_words(usersData[user]['data'][timestamp]['labels'])

                if len(synsetWords) == 2:
                    for t in myTypes:
                        standard = wn.synsets(t)
                        firstWordMaxWordSimilarity = 0
                        secondWordMaxWordSimilarity = 0
                        
                        for k in standard:
                            if synsetWords[0].wup_similarity(k) is not None:
                                if synsetWords[0].wup_similarity(k) > firstWordMaxWordSimilarity:
                                    firstWordMaxWordSimilarity = synsetWords[0].wup_similarity(k)
                                    print("{} vs {} = {}".format( synsetWords[0], k, firstWordMaxWordSimilarity ))
                                    
                            if synsetWords[1].wup_similarity(k) is not None:
                                if synsetWords[1].wup_similarity(k) > secondWordMaxWordSimilarity:
                                    secondWordMaxWordSimilarity = synsetWords[1].wup_similarity(k)
                                    print("{} vs {} = {}".format( synsetWords[1], k, secondWordMaxWordSimilarity ))
                            
                        maxScore = (firstWordMaxWordSimilarity+secondWordMaxWordSimilarity)/2
                        if usersData[user]['data'][timestamp]['is_video']:
                            # print( '這部影片在{}獲得{}分'.format(t, maxScore) )
                            videoScoreDic[t] += maxScore - 0.05 
                        else:
                            # print( '這張圖片在{}獲得{}分'.format(t, maxScore) )
                            imageScoreDic[t] += maxScore - 0.05
                else:

                    for t in myTypes:
                        maxScore = 0
                        standard = wn.synsets(t)

                        for k in standard:
                            for s in synsetWords:
                                if s.wup_similarity(k) is not None:
                                #print('{0}為計算詞性，{1}為目標詞性，分數為：{2}'.format(j,k,j.wup_similarity(k)))
                                    if s.wup_similarity(k) > maxScore:
                                        maxScore = s.wup_similarity(k)
                                        print("{} vs {} = {}".format( s, k, maxScore ))
                        
                        if usersData[user]['data'][timestamp]['is_video']:
                            # print( '這部影片在{}獲得{}分'.format(t, maxScore) )
                            videoScoreDic[t] += maxScore - 0.05 
                        else:
                            # print( '這張圖片在{}獲得{}分'.format(t, maxScore) )
                            imageScoreDic[t] += maxScore - 0.05
                    
                    # print('\n')    
                    
                
                # print('\n')
                # print("{}目前圖片個數 : {}".format(user, countImages))
                # print("{}目前在每個分類的總分:".format(user))
                # print(imageScoreDic)
                # print('\n')
                # print("{}目前影片個數 : {}".format(user, countVideos))
                # print("{}目前在每個分類的總分:".format(user))
                # print("{}目前在每個分類的總分:".format(user))
                # print(videoScoreDic)
                # print('\n\n')

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

    getWordNetScore("wordNet")

    # print( usersData )
