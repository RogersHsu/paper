import json


scoreDic100 = {}
scoreFile = "D:\\g1080265\\instagram\\score\\zhfn100w5m5it5sg1.model.bin.json"
with open(scoreFile, 'r') as load_f:
    load_dict = json.load(load_f)
    scoreDic100 = load_dict["100"]

WNScoreDic100 = {}
WNScoreFile = "D:\\g1080265\\instagram\\score\\wordNet.json"
with open(WNScoreFile, 'r') as load_f:
    load_dict = json.load(load_f)
    WNScoreDic100 = load_dict["100"]

userKey = {}

for i in range(0, len(scoreDic100)):
    userKey[scoreDic100[i]["name"]] = i

print(userKey)
print('\n\n\n')

WNUserKey = {}

for i in range(0, len(WNScoreDic100)):
    WNUserKey[WNScoreDic100[i]["name"]] = i

print(WNUserKey)
print('\n\n\n')

animalUsers = [ line.rstrip('\n') for line in open('D:\\g1080265\\instagram\\questionnaire_animal.txt', 'r') if line.rstrip('\n') != '']

animalScore100 = {}


for user in animalUsers:
    print(user)
    # print(scoreDic100[userKey[user]])
    animalScore100[user] = {}
    animalScore100[user]['word2vec'] = {}
    animalScore100[user]['wordnet'] = {}

    try:
        animalScore100[user]['word2vec']["dog"] = round( (( scoreDic100[userKey[user]]["image"]["score"]['dog']*scoreDic100[userKey[user]]["image"]["amount"]/100 + scoreDic100[userKey[user]]["video"]["score"]['dog']*scoreDic100[userKey[user]]["video"]["amount"]/100)), 2 )
    except :
        print("no video")
        animalScore100[user]['word2vec']["dog"] = round( (( scoreDic100[userKey[user]]["image"]["score"]['dog'])), 2 )

    try:
        animalScore100[user]['word2vec']["cat"] = round( (( scoreDic100[userKey[user]]["image"]["score"]['cat']*scoreDic100[userKey[user]]["image"]["amount"]/100 + scoreDic100[userKey[user]]["video"]["score"]['cat']*scoreDic100[userKey[user]]["video"]["amount"]/100)), 2 )
    except :
        print("no video")
        animalScore100[user]['word2vec']["cat"] = round( (( scoreDic100[userKey[user]]["image"]["score"]['cat'])), 2 )
    
    try:
        animalScore100[user]['wordnet']["dog"] = round( ((WNScoreDic100[WNUserKey[user]]["image"]["score"]['dog']*WNScoreDic100[WNUserKey[user]]["image"]["amount"]/100 + WNScoreDic100[WNUserKey[user]]["video"]["score"]['dog']*WNScoreDic100[WNUserKey[user]]["video"]["amount"]/100)), 2 )
    except :
        print("no video")
        animalScore100[user]['wordnet']["dog"] = round( ((WNScoreDic100[WNUserKey[user]]["image"]["score"]['dog'])), 2 )

    try:
        animalScore100[user]['wordnet']["cat"] = round( ((WNScoreDic100[WNUserKey[user]]["image"]["score"]['cat']*WNScoreDic100[WNUserKey[user]]["image"]["amount"]/100 + WNScoreDic100[WNUserKey[user]]["video"]["score"]['cat']*WNScoreDic100[WNUserKey[user]]["video"]["amount"]/100)), 2 )
    except :
        print("no video")
        animalScore100[user]['wordnet']["cat"] = round( ((WNScoreDic100[WNUserKey[user]]["image"]["score"]['cat'])), 2 )
    
    print(animalScore100[user])



animalDataFile = "D:\\g1080265\\instagram\\animal.json"

with open(animalDataFile, "w") as dump_f:
    json.dump(animalScore100, dump_f)


vehicleUsers = [ line.rstrip('\n') for line in open('D:\\g1080265\\instagram\\questionnaire_vehicle.txt', 'r') if line.rstrip('\n') != '']

vehicleScore100 = {}

for user in vehicleUsers:
    print(user)
    # print(scoreDic100[userKey[user]])
    vehicleScore100[user] = {}
    vehicleScore100[user]['word2vec'] = {}
    vehicleScore100[user]['wordnet'] = {}

    try:
        vehicleScore100[user]['word2vec']["car"] = round( ((scoreDic100[userKey[user]]["image"]["score"]['car']*scoreDic100[userKey[user]]["image"]["amount"]/100 + scoreDic100[userKey[user]]["video"]["score"]['car']*scoreDic100[userKey[user]]["video"]["amount"]/100 )), 2 )
    except :
        print("no video")
        vehicleScore100[user]['word2vec']["car"] = round( ((scoreDic100[userKey[user]]["image"]["score"]['car'])), 2 )

    try:
        vehicleScore100[user]['word2vec']["motorcycle"] = round( ((scoreDic100[userKey[user]]["image"]["score"]['motorcycle']*scoreDic100[userKey[user]]["image"]["amount"]/100 + scoreDic100[userKey[user]]["video"]["score"]['motorcycle']*scoreDic100[userKey[user]]["video"]["amount"]/100)), 2 )
    except :
        print("no video")
        vehicleScore100[user]['word2vec']["motorcycle"] = round( ((scoreDic100[userKey[user]]["image"]["score"]['motorcycle'])), 2 )

    try:
        vehicleScore100[user]['wordnet']["car"] = round( ((WNScoreDic100[WNUserKey[user]]["image"]["score"]['car']*WNScoreDic100[WNUserKey[user]]["image"]["amount"]/100 + WNScoreDic100[WNUserKey[user]]["video"]["score"]['car']*WNScoreDic100[WNUserKey[user]]["video"]["amount"]/100)), 2 )
    except :
        print("no video")
        vehicleScore100[user]['wordnet']["car"] = round( ((WNScoreDic100[WNUserKey[user]]["image"]["score"]['car'])), 2 )

    try:
        vehicleScore100[user]['wordnet']["motorcycle"] = round( ((WNScoreDic100[WNUserKey[user]]["image"]["score"]['motorcycle']*WNScoreDic100[WNUserKey[user]]["image"]["amount"]/100 + WNScoreDic100[WNUserKey[user]]["video"]["score"]['motorcycle']*WNScoreDic100[WNUserKey[user]]["video"]["amount"]/100)), 2 )
    except :
        print("no video")
        vehicleScore100[user]['wordnet']["motorcycle"] = round( ((WNScoreDic100[WNUserKey[user]]["image"]["score"]['motorcycle'])), 2 )
    
    print(vehicleScore100[user])


vehicleDataFile = "D:\\g1080265\\instagram\\vehicle.json"

with open(vehicleDataFile, "w") as dump_f:
    json.dump(vehicleScore100, dump_f)
