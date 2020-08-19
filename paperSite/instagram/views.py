import os
import re
import json
import nltk
import jieba
import gensim
import requests
import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from nltk.corpus import wordnet as wn
from googletrans import Translator
from nltk.corpus import stopwords
from os.path import isfile, isdir, join


today = datetime.date.today()
nextMonday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
thisMonday = today - datetime.timedelta(days=today.weekday())
date = {}
date['nextMonday'] = nextMonday
date['thisMonday'] = thisMonday
date['today'] = today

credential_path = 'D:\\paper.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'cookie': 'csrftoken=clEUpQamQkCExoxJjDPjWWCZTHYSU7O9; mid=XNz4mAALAAHBH-Comwo8lpvwN-yN; rur=PRN; urlgen="{\"61.218.134.33\": 3462}:1hRG6Y:UVQcciDZf4C8ZYFbrtPSK1eoOO4" fbsr_124024574287414='' '
}

myTypes = [ 'animal', 'vehicle', 'food', 'fashion' ]

word_vectors = gensim.models.KeyedVectors.load_word2vec_format( ('D:\\word2vec\\model\\zhfn150w5m10it5sg1.model.bin'), binary=True )

scoreDic = {}
scoreFile = "D:\\g1080265\\instagram\\score\\zhfn100w5m5it5sg1.model.bin.json"
with open(scoreFile, 'r') as load_f:
    load_dict = json.load(load_f)
    scoreDic = load_dict

types = {}
scoreFile = "D://g1080265//instagram//types.json"
with open(scoreFile, 'r') as load_f:
    types = json.load(load_f)


def index(request):
    return render(request, 'index.html', {'date': date,})
    # return render(request, 'currentTypes2.html', {'types': types,})


def search(request):
    # try:
    text = request.GET['search']
    print(text)
    zh_tw = False
    for ch in text:
        if u'\u4e00' <= ch <= u'\u9fff':
            zh_tw = True

    
    finalWords = []
    print(zh_tw)
    if(zh_tw):
        usefulWords = []
        stopWordSet = [ line.rstrip('\n') for line in open('D:\\g1080265\\paperSite\\instagram\\stopWords.txt', 'r', encoding="utf-8") ]
        for word in jieba.cut(text, cut_all = False):
            print(word)
            if word not in stopWordSet:
                usefulWords.append(word)
        
        print('usefulWords', usefulWords)
        translator = Translator()
        
        for w in usefulWords:
            
            transWord = translator.translate(w, dest='en').text.lower()

            print('transWord', transWord)
            try:
                transWord_list = transWord.lower().split(" ")
                finalWords.extend( transWord_list )
            except:
                finalWords.append( transWord )

        print('finalWords', finalWords)


    else:
        stopWordSet = stopwords.words('english')
        for word in nltk.word_tokenize(text):
            if word not in stopWordSet:
                try:
                    word_list = transWords.lower().split(" ")
                    finalWords.extend( word_list )
                except:
                    finalWords.append(  word.lower() )
    
    # print('finalWords', finalWords)

    # if len(text) > 1:
    #     keyWords = []

    #     for word, pos in nltk.pos_tag(text):
    #         if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
    #             print( "{}({})".format(word, pos) )
    #             keyWords.append(word)
    # else:
    #     keyWords = text
    # myTypes = ["cat.n.01", "dog.n.01", "fashion.n.03", "fashion.n.04", "food.n.01"]
    # print(keyWords)
    # similarTypes = {}
    # for word in keyWords:
    #     for ws in wn.synsets(word):
    #         for t in myTypes:

    #             ts = wn.synset( t )
    #             score = ws.wup_similarity(ts)

    #             if (score is not None) and (score > 0.7):
    #                 print("{}:{} : {}".format(word, ws, ws.definition()) )
    #                 print("{}:{} vs {} = {}".format(word, ws, ts, score))
    #                 print("\n")
    #                 tp = t.split(".")[0] 
    #                 if tp not in similarTypes:
    #                     similarTypes[ str(t.split(".")[0]) ] = score
    #                 elif (tp in similarTypes) and (score>similarTypes[tp]):
    #                     similarTypes[ str(t.split(".")[0]) ] = score
    similarTypes = {}
    for word in finalWords:
        for type in myTypes:
            try:
                score = word_vectors.similarity(word, type)
                print( "{} vs {} = {}".format(word, type, score) )
                print("\n")
            except:
                score = 0
            
            if (score is not None) and (score > 0.5):
                if type not in similarTypes:
                    similarTypes[ type ] = score

    print(similarTypes)
    similarTypes = sorted( similarTypes.items(), key=lambda kv: kv[1], reverse=True )
    similarTypes = [ value[0] for value in similarTypes ]

    print(similarTypes)

    if not similarTypes:
        responseDic = {}
        responseDic['success'] = False
        responseDic['message'] = ("輸入的關鍵字'{}'無相關分類，快去推薦新分類吧!".format(text))
        return JsonResponse(responseDic,  safe=False)
    else:
        responseDic = {}
        responseDic['success'] = True
        responseDic['message'] = "success"
        responseDic['similarTypes'] = []
        responseDic['similarTypes'] = similarTypes
        # responseDic['score'] = scoreDic['150']

    return JsonResponse(responseDic,  safe=False)

    # except KeyError:
    #     responseDic = {}
    #     responseDic['success'] = False
    #     responseDic['message'] = "輸入的關鍵字無最相關分類"
    #     return JsonResponse(responseDic, safe=False)

    # except Exception as e:
    #     responseDic = {}
    #     responseDic['success'] = False
    #     responseDic['message'] = "Exception"
    #     return JsonResponse(responseDic, safe=False)


def getData(request, newType, postNum):

    responseDic = {}
    responseDic['success'] = True
    responseDic['newType'] = newType
    responseDic['postNum'] = postNum

    scoreDic[str(postNum)] = sorted(scoreDic[str(postNum)], key=lambda x: (( 
        (x['image']['score'][newType]*x['image']['amount']/100) if x['video']['amount']==0 
        else (x['image']['score'][newType]*x['image']['amount']/100  + x['video']['score'][newType]*x['video']['amount']/100) ), x['ERate']), reverse=True)


    # scoreDic[str(postNum)] = sorted(scoreDic[str(postNum)], key=lambda x: (( 
    #     (x['image']['score'][newType]*imageRate + x['image']['score'][newType]*videoRate) if x['video']['amount']==0 
    #     else (x['image']['score'][newType]*imageRate + x['video']['score'][newType]*videoRate) ), x['ERate']), reverse=True)

    # for user in scoreDic[str(postNum)]:
    #     if user['video']['amount']==0:
    #         user['video']['score'][newType] = 1
    # scoreDic[str(postNum)] = sorted(scoreDic[str(postNum)], key=lambda x: ((x['image']['score'][newType]*imageRate+x['image']['score'][newType]*videoRate), (x['ERate'])), reverse=True)
    
    # print( scoreDic[str(postNum)] )
    responseDic['score'] = [ scoreDic[str(postNum)][i] for i in range(0, 10) ]

    # responseDic['score'] = scoreDic[str(postNum)]
    return JsonResponse(responseDic, safe=False)
    # return HttpResponse(newType)


def recommend(request):
    return render(request, 'recommend2.html')

def getSysets(request, input):
    try:
        translator = Translator()

        zh_tw = False
        for ch in input:
            if u'\u4e00' <= ch <= u'\u9fff':
                zh_tw = True

        if zh_tw:
            input = translator.translate(input, dest='en').text
            print(input)
        
        responseDic = {}
        responseDic['sysets'] = []
        types = input.split(" ")
        for t in types:
            sysets = wn.synsets(t)
            for s in sysets:
                syset = {}
                syset['syset'] = str(s)
                syset['definition'] = translator.translate(s.definition(), dest='zh-tw').text+"("+s.definition()+")"
                responseDic['sysets'].append(syset)

        responseDic['success'] = True
        responseDic['message'] = '推薦成功'
        return JsonResponse(responseDic, safe=False)

    except Exception as e:
        responseDic = {}
        responseDic['success'] = False
        responseDic['message'] = '失敗'
    
    return JsonResponse(responseDic, safe=False)

def recommendNewType(request):

    responseDic = {}

    newType = request.GET['type']

    typesFile = "D://g1080265//instagram//recommend_types.txt"
    types = [ line.rstrip('\n') for line in open(typesFile, 'r') if line.rstrip('\n') != '']
    types.extend( [ line.rstrip('\n') for line in open('D:\\g1080265\\instagram\\types.txt', 'r') if line.rstrip('\n') != ''] )
    
    if newType in types:
        responseDic['success'] = False
        responseDic['message'] = "已有人推薦此分類"
    else:
        
        fp = open(typesFile, "a")
        fp.write("\n"+newType)
        fp.close()
        responseDic['success'] = True
        responseDic['message'] = '推薦成功'
        
    return JsonResponse(responseDic, safe=False)


def get_html(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print('請求網頁原代碼錯誤, 錯誤狀態碼：', response.status_code)
    except Exception as e:
        print(e)
        return None


def recommendNewUser(request):
    
    newAccount = request.GET['account']

    responseDic = {}

    usersFile = "D://g1080265//instagram//recommend_users.txt"
    userNames = [ line.rstrip('\n') for line in open(usersFile, 'r') if line.rstrip('\n') != '']
    userNames.extend( [ line.rstrip('\n') for line in open('D:\\g1080265\\instagram\\users_sure.txt', 'r') if line.rstrip('\n') != ''] )

    if newAccount in userNames:
        responseDic['success'] = False
        responseDic['message'] = "已有人推薦此帳號"
    else:
        url_base = 'https://www.instagram.com/'
        url = url_base + newAccount + '/'
        html = get_html(url)
        try:
            user_id = re.findall('"profilePage_([0-9]+)"', html, re.S)[0]
            fp = open(usersFile, "a")
            fp.write("\n"+newAccount)
            fp.close()
            responseDic['success'] = True
            responseDic['message'] = '推薦成功'
        except IndexError:
            print( newAccount )
            print( "找不到此用戶" )
            responseDic['message'] = "找不到此用戶"

    return JsonResponse(responseDic, safe=False)


def currentTypes(request):
    return render(request, 'currentTypes.html', {'types': myTypes, 'date':date})


def currentUsers(request):
    return render(request, 'currentUsers.html', {'users':scoreDic['150'], 'date':date, })


def getUsers(request, postNum):
    responseDic = {}
    responseDic['success'] = True
    responseDic['postNum'] = postNum
    responseDic['score'] = scoreDic[str(postNum)]

    return JsonResponse(responseDic, safe=False)


def questionnaire_animal(request):
    userNames = [ line.rstrip('\n') for line in open('D:\\g1080265\\instagram\\questionnaire_animal.txt', 'r') if line.rstrip('\n') != '']
    types = ['dog', 'cat']
    qType = 'animal'
    return render(request, 'questionnaire_urls.html', {'types': types, 'users':userNames, 'qType':qType})


def questionnaire_vehicle(request):
    userNames = [ line.rstrip('\n') for line in open('D:\\g1080265\\instagram\\questionnaire_vehicle.txt', 'r') if line.rstrip('\n') != '']
    types = ['car', 'motorcycle']
    qType = 'vehicle'
    return render(request, 'questionnaire_urls.html', {'types': types, 'users':userNames, 'qType':qType})


def getUserUrls(request, userName):

    responseDic = {}
    responseDic['success'] = True
    
    with open("D:\\g1080265\\instagram\\usersUrls20200312.json", 'r') as load_f:
        usersUrls = json.load(load_f)
    
    print(userName)
    
    responseDic['urls'] = usersUrls[userName]
    print( len(responseDic['urls']) )

    return JsonResponse(responseDic, safe=False)


def submitScore( request, userName, value1, value2, qType):

    responseDic = {}
    
    questionnaireScoreFile = "D:\\g1080265\\instagram\\questionnaire_scores.json"
    if not os.path.exists(questionnaireScoreFile):
        with open(questionnaireScoreFile, "w") as dump_f:
            qScore = {}
            json.dump(qScore, dump_f, ensure_ascii=False)

    else:
        with open(questionnaireScoreFile, 'r') as load_f:
            qScore = json.load(load_f)
    
    if userName not in qScore:
        qScore[userName] = {}
        qScore[userName]['dog'] = []
        qScore[userName]['cat'] = []
        qScore[userName]['car'] = []
        qScore[userName]['motorcycle'] = []
    
    if qType == 'animal':
        qScore[userName]['dog'].append(value1)
        qScore[userName]['cat'].append(value2)
    else:
        qScore[userName]['car'].append(value1)
        qScore[userName]['motorcycle'].append(value2)

    with open(questionnaireScoreFile, "w") as dump_f:
        json.dump(qScore, dump_f, ensure_ascii=False)
    
    responseDic['success'] = True

    return JsonResponse(responseDic, safe=False)


def currentTypes_admin(request):
    
    Types = [  'animal', 'vehicle',  'dog', 'cat', 'food', 'fashion', 'car', 'motorcycle' ]
    
    models = []

    path = "D:\\word2vec\\model\\"
    for f in os.listdir("D:\\word2vec\\model\\"):
        
        fullpath = join(path, f)
        
        if isfile(fullpath):
            models.append(f)
    print(Types)
    return render(request, 'currentTypes_admin.html', {'models': models,'types': Types, 'date':date})


def getAdminData(request, model, newType, postNum):

    responseDic = {}
    responseDic['success'] = True
    responseDic['newType'] = newType
    responseDic['postNum'] = postNum

    selectFile = "D:\\g1080265\\instagram\\score\\{}.json".format(model)
    with open(selectFile, 'r') as load_f:
        selectDic = json.load(load_f)
    # print(selectDic[str(postNum)]['image']['amount'])


    selectDic[str(postNum)] = sorted(selectDic[str(postNum)], key=lambda x: (( 
        (x['image']['score'][newType]*x['image']['amount']/100) if x['video']['amount']==0 
        else (x['image']['score'][newType]*x['image']['amount']/100  + x['video']['score'][newType]*x['video']['amount']/100) ), x['ERate']), reverse=True)

    responseDic['score'] = [ selectDic[str(postNum)][i] for i in range(0, 10) ]
    # responseDic['score'] = selectDic[str(postNum)]
    
    return JsonResponse(responseDic, safe=False)


def ex_results_animal(request):
    type = 'animal'
    types = {}
    types['1'] = 'dog'
    types['2'] = 'cat'
    userNames = [ line.rstrip('\n') for line in open('D:\\g1080265\\instagram\\questionnaire_animal.txt', 'r') if line.rstrip('\n') != '']
    print(userNames)

    return render(request, 'ex_results.html', {'type':type, 'types':types, 'users': userNames, 'date':date})


def ex_results_vehicle(request):
    type = 'vehicle'
    types = {}
    types['1'] = 'car'
    types['2'] = 'motorcycle'
    userNames = [ line.rstrip('\n') for line in open('D:\\g1080265\\instagram\\questionnaire_vehicle.txt', 'r') if line.rstrip('\n') != '']
    print(userNames)

    return render(request, 'ex_results.html', {'type':type, 'types':types, 'users': userNames, 'date':date})


def getUserEx(request, userName):

    print(userName)

    responseDic = {}
    responseDic['success'] = True
    
    responseDic['user'] = {} 

    usersIndex = { scoreDic['100'][i]['name']:i for i in range( 0, len(scoreDic['100']) ) }
    responseDic['user'] = scoreDic['100'][ usersIndex[userName] ]

    print(responseDic)

    return JsonResponse(responseDic, safe=False)