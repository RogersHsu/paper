import os
import nltk
from nltk.corpus import wordnet as wn

# Imports the Google Cloud client library
from google.cloud import translate_v3beta1 as translate
from googletrans import Translator

# 引用詞幹提取器
# from nltk.stem import PorterStemmer
# from nltk.stem import LancasterStemmer
# from nltk.stem import SnowballStemmer

# # 詞性還原 
from nltk.stem import WordNetLemmatizer

# from itertools import combinations #計算排列組合 

# result = [("cat", 0.997473955154419), ("animal", 0.9256876111030579), ("pet", 0.8643725514411926), ("room", 0.7402945160865784), ("carnivoran", 0.5184839963912964), ("floor", 0.4950612485408783), ("kitten", 0.4765672981739044), ("flooring", 0.4409010410308838), ("play", 0.39492350816726685), ("dog", 0.3830379843711853), ("hardwood", 0.3411344289779663)]
# resultDic = [("cat", 0.997473955154419), ("pet", 0.9810512661933899), ("animal", 0.9568819999694824), ("small to medium sized cats", 0.9529238939285278), ("kitten", 0.7980900406837463), ("domestic short haired cat", 0.6511285901069641), ("carnivoran", 0.629082441329956), ("cat like mammal", 0.5508931279182434), ("whiskers", 0.5055666565895081), ("vertebrate", 0.3984883427619934)]

# print( wn.synset( "vehicle.n.01" ).wup_similarity( wn.synset("car.n.01") ) )


# label = ["yang", "cuisine", "ingredient", "dish", "food"]

# labelCom = list(combinations(label, 2)) #計算所有label內的排列組合

# print( labelCom )

myTypes = ["cat.n.01", "dog.n.01", "fashion.n.03", "fashion.n.04", "food.n.01"]

# text = nltk.word_tokenize('It is a cute dog')
# print( text )
# print( nltk.pos_tag(text) )
# maxScore = 0.5
# finalType = []

# for word in words:
#     for ws in wn.synsets(word):
#         for t in myTypes:

#             ts = wn.synset( t )
#             score = ws.wup_similarity(ts)

#             if (score is not None) and (score > 0.6) and (t.split(".")[0] not in finalType):
#                 print("{}:{} : {}".format(word, ws, ws.definition()) )
#                 print("{}:{} vs {} = {}".format(word, ws, ts, score))                
#                 print("\n")
#                 finalType.append( t.split(".")[0]  )

# print(finalType)
# print( not finalType )

# print( wn.synset( "cat.n.01" ).definition() )
# print( wn.synset( "dog.n.01" ).definition() )
# print( wn.synset( "fashion.n.03" ).definition() )
# print( wn.synset( "fashion.n.04" ).definition() )
# print( wn.synset( "food.n.01" ).definition() )
# print( wn.synset( "food.n.02" ).definition() )


# eating = 'eating'
# ate = 'ate'

# 詞幹提取初始化
# pst = PorterStemmer()
# lst = LancasterStemmer()
# snow = SnowballStemmer('english')#需定義語言
# # 使用 (以Porter Stemmer為例）
# eating = pst.stem(eating)
# ate = pst.stem(ate)
# print ( eating )
# print ( ate )

# # 詞性還原 初始化
# wtlem = WordNetLemmatizer()
# # 指定詞性為動詞
# print( wtlem.lemmatize( 'exersize', 'n' ) )
# print( wtlem.lemmatize( ate, 'n' ) )


# text = 'a member of the genus Canis (probably descended from the common wolf) that has been domesticated by man since prehistoric times; occurs in many breeds'
# text = "穿時尚衣服的小狗"
# text = '穿衣服的貓在吃pizza'
# print(text)
# zh_tw = False
# for ch in text:
#     if u'\u4e00' <= ch <= u'\u9fff':
#         zh_tw = True
#         break

# print(zh_tw)
# if(zh_tw):

#     translator = Translator()
#     text = translator.translate(text, dest='en').text
#     # client = translate.TranslationServiceClient()

#     # location = 'global'
#     # project_id = 'paper-253304'
#     # parent = client.location_path(project_id, location)

#     # response = client.translate_text(
#     #     parent=parent,
#     #     contents=[text],
#     #     mime_type='text/plain',  # mime types: text/plain, text/html
#     #     source_language_code='zh-tw',
#     #     target_language_code='en-US')

#     # print(text)
#     # text = str(response.translations[0])[18:-2]
#     # print(text)

# print(text)
# text = text.split(' ')
# print(text)

# if len(text) > 1:
#     keyWords = []

#     for word, pos in nltk.pos_tag(text):
#         if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS' or pos=='JJ'):
#             print( "{}({})".format(word, pos) )
#             keyWords.append(word)
#         elif pos=='JJR' or pos=='JJS':
#             # 詞性還原 初始化
#             wtlem = WordNetLemmatizer()
#             # 指定詞性為形容詞
#             keyWords.append( wtlem.lemmatize(word, wn.ADJ) )
# else:
#     keyWords = text

# print(keyWords)
# similarTypes = {}
# for word in keyWords:
#     print(word)
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

# print(similarTypes)
# similarTypes = sorted(similarTypes.items(), key=lambda kv: kv[1], reverse=True)
# similarTypes = [ value[0] for value in similarTypes ]
# print(similarTypes)


print( wn.synsets('fashionable') )
print( wn.synsets('fashion') )