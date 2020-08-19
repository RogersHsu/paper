import os
import json
import gensim
import random
from os.path import isfile, isdir, join

myTypes = ['animal', 'vehicle',  'food', 'fashion', 'dog', 'cat', 'car', 'motorcycle']

#photography life makeup 

usersDataFile = "D:\\g1080265\\instagram\\usersData.json"
with open(usersDataFile, 'r') as load_f:
    usersData = json.load(load_f)

def getScore(model):
    
    new_dic = {}
    scoreFile = ("D:\\g1080265\\instagram\\score\\{}.json".format( model ) )
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
                            # 當type是car時為了讓 屬於motorcycle的帳號car的分數低
                            if (t=='car' and 'motorcycle' in usersData[user]['data'][timestamp]['labels']):
                                maxScore = 0.4
                                continue
                            
                            # 當type是motorcycle時為了讓 屬於car的帳號motorcycle的分數低 但是要避免掉排除是motorcycle 又有car
                            if (t=='motorcycle' and 'car' in usersData[user]['data'][timestamp]['labels'] and 'motorcycle' not in usersData[user]['data'][timestamp]['labels']):
                                maxScore = 0.4
                                continue

                            

                            # if (t == 'car' and label == 'motorcycle') or (t=='motorcycle' and 'car' in usersData[user]['data'][timestamp]['labels']):
                            #     continue
                            # if (t == 'motorcycle' and label == 'car') or (t=='car' and label == 'motorcycle'):
                            #     continue

                            try:
                                score = word_vectors.similarity(t, label)
                            except:
                                score = 0
                            if score > maxScore:
                                # print( 'type:{} vs result:{}'.format(t, label) )
                                maxScore = score
                                # 當type是 dog 時為了讓 屬於cat的帳號 dog 的分數低
                                if (t=='dog' and 'cat' in usersData[user]['data'][timestamp]['labels']):
                                    maxScore -= 0.15

                                # 當type是 cat 時為了讓 屬於dog的帳號 cat 的分數低
                                if (t=='cat' and 'dog' in usersData[user]['data'][timestamp]['labels']):
                                    maxScore -= 0.2


                        if usersData[user]['data'][timestamp]['is_video']:
                            # print( '這部影片在{}獲得{}分'.format(t, maxScore) )
                            videoScoreDic[t] += maxScore
                            
                        else:
                            # print( '這張圖片在{}獲得{}分'.format(t, maxScore) )
                            imageScoreDic[t] += maxScore
                    
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

    path = "D:\\word2vec\\model\\"
    for f in os.listdir("D:\\word2vec\\model\\"):
        
        fullpath = join(path, f)
        
        if isfile(fullpath):
            getScore(f)

    # print( usersData )