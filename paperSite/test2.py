import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from nltk.corpus import wordnet as wn


scoreDic = {}
scoreFile = "D://instagram//score2.json"
with open(scoreFile,'r') as load_f:
    load_dict = json.load(load_f)
    scoreDic = load_dict

newType = 'dog'
postNum = 200
imageRate = 9
videoRate = 1

responseDic = {}
responseDic['success'] = True
responseDic['newType'] = newType
responseDic['postNum'] = postNum

scoreDic[str(postNum)] = sorted( scoreDic[str(postNum)], key = lambda x : ( ( x['image']['score'][newType] if not bool(x['video']['score']) else (x['image']['score'][newType]*imageRate+x['video']['score'][newType]*videoRate) ), (x['ERate']) ), reverse=True )
responseDic['score'] = scoreDic[str(postNum)]

print( responseDic['score'] )