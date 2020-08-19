from nltk.corpus import wordnet as wn

types = 'dog'
responseDic = {}
typesList = types.split(" ")
for t in typesList:
    sysets = wn.synsets(t)
    for s in sysets:
        responseDic[str(s)] = s.definition()

responseDic['success'] = True
responseDic['message'] = '推薦成功'
print(responseDic)