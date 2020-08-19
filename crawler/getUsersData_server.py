from __future__ import unicode_literals

import io
import os
import re
import sys
import json
import time
import random
import requests
import collections
from os import listdir
from hashlib import md5
from pyquery import PyQuery as pq
from itertools import combinations #計算排列組合 
from nltk.corpus import wordnet as wn
from datetime import datetime

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

from google.cloud import videointelligence

url_base = 'https://www.instagram.com/'
uri = 'https://www.instagram.com/graphql/query/?query_hash=a5164aed103f24b03e7b7747a2d94e3c&variables=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A12%2C%22after%22%3A%22{cursor}%22%7D'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'cookie': 'csrftoken=clEUpQamQkCExoxJjDPjWWCZTHYSU7O9; mid=XNz4mAALAAHBH-Comwo8lpvwN-yN; rur=PRN; urlgen="{\"61.218.134.33\": 3462}:1hRG6Y:UVQcciDZf4C8ZYFbrtPSK1eoOO4" fbsr_124024574287414='' '
}

credential_path = 'D:\\paper.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# Instantiates a client
client = vision.ImageAnnotatorClient()

"""Detect labels given a file path."""
video_client = videointelligence.VideoIntelligenceServiceClient()
features = [videointelligence.enums.Feature.LABEL_DETECTION]


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


def get_json(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print('請求網頁json錯誤, 錯誤狀態碼：', response.status_code)
    except Exception as e:
        print(e)
        time.sleep(60 + float(random.randint(1, 4000))/100)
        return get_json(url)


def get_content(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.content
        else:
            print('請求照片二進制錯誤, 錯誤狀態碼：', response.status_code)
    except Exception as e:
        print(e)
        return None


def processImage(content):
    file_path = r'{}\{}\{}\{}.jpg'.format(
        storeFolder, user, 'image', md5(content).hexdigest())

    with open(file_path, 'wb') as f:
        f.write(content)
        f.close()
    
    # The name of the image file to annotate
    file_name = os.path.abspath(file_path)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    error = True
    while error:
        try:
            # Performs label detection on the image file
            response = client.label_detection(image=image)
            error = False
        except:
            print('sleep 10 seconds')
            time.sleep(10)
    
    result = response.label_annotations
    
    # print(result)

    resultLabels = []
    for label in result:
        if label.score > 0.7:
            try:
                tmp = label.description.split(" ")
                resultLabels.append( tmp[len(tmp)-1].lower() )
            except:
                # resultLabels.append( result[i][0].lower() )
                resultLabels.append( label.description.lower() )
    
    return resultLabels


def processVideo(content):

    file_path = r'{}\{}\{}\{}.mp4'.format(
        storeFolder, user, 'video', md5(content).hexdigest())

    with open(file_path, 'wb') as f:
        f.write(content)
        f.close()
    
    resultDic = {}
    error = True
    countError = 0
    while error:
        try:
            with io.open(file_path, 'rb') as movie:
                input_content = movie.read()
                operation = video_client.annotate_video(
                    features=features, input_content=input_content)
                print('\nProcessing video for label annotations:')
                result = operation.result(timeout=20)

                print('\nFinished processing.\n')
                # Process video/segment level label annotations
                segment_labels = result.annotation_results[0].segment_label_annotations
                
                for i, segment_label in enumerate(segment_labels):
                    label = segment_label.entity.description

                    for i, segment in enumerate(segment_label.segments):
                        confidence = segment.confidence
                        resultDic[label] = confidence
            error = False
        
        except:
            countError += 1
            print("video result = {}".format(resultDic))
            print('sleep 65 seconds')
            time.sleep(65)
            error = True
        
        if countError >= 2:
            break
    
    if error:
        print('\n\n\n\n\n')
        print( 'igtv' )
        print('\n\n\n\n\n')
        return 'igtv'

    print("video result = {}".format(resultDic))          

    resultDic = sorted(resultDic.items(), key=lambda item: item[1], reverse=True)

    resultLabels = []
    for i in range(0, len(resultDic)):
        if resultDic[i][1] > 0.7:
            try:
                tmp = resultDic[i][0].split(" ")
                resultLabels.append( tmp[len(tmp)-1].lower() )
            except:
                resultLabels.append( resultDic[i][0].lower() )
    
    return resultLabels


def getData(edge, userData):

    broken = False

    timestamp = str( edge['node']['taken_at_timestamp'] )
    # timestamp = edge['node']['taken_at_timestamp']

    notIn = False
    if timestamp not in userData['data']:
    # if  int(timestamp) > 1583942400:
        notIn = True
        userData['data'][timestamp] = {}

    if edge['node']['is_video']:
        print('\n\n')
        print("is_video:", edge['node']['is_video'])
        
        if 'display_url' in userData['data'][timestamp]:
            del userData['data'][timestamp]['display_url']
        
        try:
            # userData['data'][timestamp]['video_url'] = edge['node']['video_url']
            content = get_content(edge['node']['video_url'])
            
        except KeyError:
            vUrl = "https://www.instagram.com/p/"+edge['node']["shortcode"]
            print( vUrl )
            html = get_html( vUrl )
            doc = pq( html )
            vUrl = doc("meta[property='og:video']").attr('content')
            print( vUrl )

            # userData['data'][timestamp]['video_url'] = vUrl
            content = get_content( vUrl )


        file_path = r'{}\{}\{}\{}.mp4'.format(
        storeFolder, user, 'video', timestamp)

        userData['data'][timestamp]['video_url'] = timestamp

        if notIn or ('labels' not in userData['data'][timestamp]) :
            print("notIn:", notIn)
            
            userData['data'][timestamp]['labels'] = processVideo(content)
            userData['data'][timestamp]['is_video'] = True

            print( "sleep 20 seconds" )
            time.sleep(20)
            
    else:
        if 'video_url' in userData['data'][timestamp]:
            del userData['data'][timestamp]['video_url']

        content = get_content(edge['node']['display_url'])

        file_path = r'{}\{}\{}\{}.jpg'.format(
        storeFolder, user, 'image', timestamp)  
        
        userData['data'][timestamp]['display_url'] = timestamp

        if notIn or ('labels' not in userData['data'][timestamp]):   
            print("notIn:", notIn)
            userData['data'][timestamp]['labels'] = processImage(content)
        
        userData['data'][timestamp]['is_video'] = False

    try:
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()
        print('下載成功')
        print( file_path )
    except:
        print('\n\n\n')
        print('下載失敗')
        print('\n\n\n')
        broken = True

    userData['data'][timestamp]['likes'] = edge['node']['edge_media_preview_like']['count']
    userData['data'][timestamp]['comments'] = edge['node']['edge_media_to_comment']['count']

    # try:
    #     # rule = re.compile( u"[^\u4e00-\u9fa5]" )
    #     rule = re.compile( u"[^\u4e00-\u9fa5^.^a-z^A-Z^' ']" )
    #     userData['data'][timestamp]['caption'] = rule.sub( '', edge['node']['edge_media_to_caption']['edges'][0]['node']['text'] )
    # except:
    #     userData['data'][timestamp]['caption'] = ''
    #     print("無貼文內容")

    # if 'caption' in userData['data'][timestamp]:
    #     del userData['data'][timestamp]['caption']
    
    if broken:
        del userData['data'][timestamp]
    else:
        print(userData['data'][timestamp])
    
    return userData


def update(user, userData):

    print( '\n'+user+'\n\n' )

    countPost = 0
    maxPost = 350
    
    url = url_base + user + '/'
    html = get_html(url)
    user_id = re.findall('"profilePage_([0-9]+)"', html, re.S)[0]
    doc = pq(html)
    items = doc('script[type="text/javascript"]').items()

    for item in items:
        if item.text().strip().startswith('window._sharedData'):
            js_data = json.loads(item.text()[21:-1], encoding='utf-8')
            edges = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
            page_info = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]['page_info']
            cursor = page_info['end_cursor']
            flag = page_info['has_next_page']
            
            countFollowers = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_followed_by"]["count"]
            print( countFollowers )
            # userData['followers'] = countFollowers

            for edge in edges:
                
                countPost += 1
                # timeArray = time.localtime(edge['node']['taken_at_timestamp'])
                # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                # print(otherStyleTime)

                timestamp = edge['node']['taken_at_timestamp']

                if  int(timestamp) < 1584028799:
                    print( datetime.fromtimestamp(timestamp) )
                    getData(edge, userData)
                    print("目前讀取貼文數量 : {} \n".format(countPost))
                    print('\n')

    while flag:
        url = uri.format(user_id=user_id, cursor=cursor)
        js_data = get_json(url)
        edges = js_data['data']['user']['edge_owner_to_timeline_media']['edges']
        cursor = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        flag = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']

        for edge in edges:

            countPost += 1
            if countPost > maxPost:
                break
            
            timestamp = edge['node']['taken_at_timestamp']
            if  int(timestamp) < 1584028799:
                print( datetime.fromtimestamp(timestamp) )
                getData(edge, userData)
                print("目前讀取貼文數量 : {} \n".format(countPost))
                print('\n')

        if countPost >= maxPost:
            break

        # print(cursor, flag)
        # if countPost > 2000, turn on
        # time.sleep(4 + float(random.randint(1, 800))/200)

        time.sleep(2 + float(random.randint(1, 800))/200)

    # userData = [ ( k,userData[k] ) for k in sorted( userData.keys() ) ]
    sortData = {}
    for k in sorted( userData['data'].keys(), reverse=True ):
        sortData[k] = userData['data'][k]
    # userData = collections.OrderedDict(sorted(userData.items()))
    
    userData['data'] = sortData
    
    return userData


def setUserUrls(userData, user):

    usersUrlsFile = "D:\\g1080265\\instagram\\usersUrls20200312.json"
    if not os.path.exists(usersUrlsFile):
        with open(usersUrlsFile, "w") as dump_f:
            usersUrls = {}
            json.dump(usersUrls, dump_f, ensure_ascii=False)
    else:
        with open(usersUrlsFile, 'r') as load_f:
            usersUrls = json.load(load_f)

    print('\n\n\n\n\n')
    print( user )
    usersUrls[user] = []

    imgFiles = listdir("D:\\instagram\\{}\\image".format(user))
    vieFiles = listdir("D:\\instagram\\{}\\video".format(user))

    count = 0    
    for timestamp in userData['data']:

        if userData['data'][timestamp]['labels'] != 'igtv':
            

            urlData = {}
            if userData['data'][timestamp]['is_video']  and  '{}.{}'.format(timestamp, 'mp4') in vieFiles:
                urlData['is_video'] = True
                urlData['video_url'] = ( 'instagram/{}/{}/{}.{}'.format(user, 'video', timestamp, 'mp4') )
                count += 1
                usersUrls[user].append( urlData )
                
            elif '{}.{}'.format(timestamp, 'jpg') in imgFiles:
                urlData['is_video'] = False

                urlData['display_url'] = ( 'instagram/{}/{}/{}.{}'.format(user, 'image', timestamp, 'jpg') )
                count += 1
                usersUrls[user].append( urlData )
            
            else:
                print(userData['data'][timestamp])

            print(urlData)
            print("目前讀取貼文數量 : {} \n".format(count))
            
            if count == 100:
                break

    with open(usersUrlsFile, "w") as dump_f:
        json.dump(usersUrls, dump_f)

    print( len(usersUrls[user]) )
    print('\n\n\n\n\n')


if __name__ == '__main__':
    
    start = time.time()


    storeFolder = 'D:\\instagram'
    if not os.path.exists(storeFolder):
        os.mkdir(storeFolder)

    # with open("D:\\g1080265\\instagram\\users.json", 'r') as load_f:
    #     userNames = json.load(load_f)['users']
    #     print(userNames)
    # userNames = [ line.rstrip('\n') for line in open('D:\\g1080265\\instagram\\questionnaire_vehicle.txt', 'r') if line.rstrip('\n') != '' ]
    # userNames = [ line.rstrip('\n') for line in open('D:\\g1080265\\instagram\\questionnaire_animal.txt', 'r') if line.rstrip('\n') != '' ]
    # userNames = ['motorcycledreams']
    # userNames = ["bernese.life"]
    userNames = [ line.rstrip('\n') for line in open('D:\\g1080265\\instagram\\users_sure.txt', 'r') if line.rstrip('\n') != '']
    userNames = ['dogs.associates']

    for user in userNames:
        print(user)

    usersDataFile = "D:\\g1080265\\instagram\\usersData.json"
    if not os.path.exists(usersDataFile):
        with open(usersDataFile, "w") as dump_f:
            usersData = {}
            json.dump(usersData, dump_f, ensure_ascii=False)
    else:
        with open(usersDataFile, 'r') as load_f:
            usersData = json.load(load_f)

    for user in userNames:

        userPath = r'{}\{}'.format(storeFolder, user)
        imgPath = r'{}\{}'.format(userPath, 'image')
        videoPath = r'{}\{}'.format(userPath, 'video')

        if not os.path.exists(userPath):
            os.mkdir(userPath)
            os.mkdir(imgPath)
            os.mkdir(videoPath)
            
        if user not in usersData:
            usersData[user] = {}
            usersData[user]['data'] = {}

        try:
            usersData[user] = update(user, usersData[user])

            with open(usersDataFile, "w") as dump_f:
                json.dump(usersData, dump_f)
            
            # print( usersData[user] )
            setUserUrls(usersData[user], user)

        except IndexError:
            print( user )
            print( "找不到此用戶" )
        
    print('Complete!!!!!')

    end = time.time()
    spend = end - start
    hour = spend // 3600
    minu = (spend - 3600 * hour) // 60
    sec = spend - 3600 * hour - 60 * minu

    print(f'一共花費了{hour}小時{minu}分鐘{sec}秒')