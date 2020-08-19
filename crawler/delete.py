import os
import json

usersDataFile = "D:\\g1080265\\instagram\\usersData.json"

with open(usersDataFile, 'r') as load_f:
    usersData = json.load(load_f)

for user in usersData:
    for timestamp in usersData[user]['data']:
        if 'display_url' in usersData[user]['data'][timestamp]:
            del usersData[user]['data'][timestamp]['display_url']
        if 'video_url' in usersData[user]['data'][timestamp]:
            del usersData[user]['data'][timestamp]['video_url']

with open(usersDataFile, "w") as dump_f:
    json.dump(usersData, dump_f)

print(usersData)