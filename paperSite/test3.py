import json

scoreDic = {}
scoreFile = "D://instagram//score2.json"
with open(scoreFile,'r') as load_f:
    load_dict = json.load(load_f)
    scoreDic = load_dict

scoreDic['150'] = sorted( scoreDic['150'], key = lambda x : ( (x['image']['score']['car'] if not bool(x['video']['score']) else (x['image']['score']['car']*0.8+x['video']['score']['car']*0.2) ), (x['ERate']) ), reverse=True )