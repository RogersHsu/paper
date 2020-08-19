# import json

# userNames = [ line.rstrip('\n') for line in open('D:\\g1080265\\instagram\\users_sure.txt', 'r') if line.rstrip('\n') != '']

# # print(userNames)

# def cool():
#     tew = ['test']
#     return []


# if __name__ == '__main__':
    
#     # value = cool()

#     # if( value ):
#     #     print( value )
#     # else:
#     #     print( '空' )
#     userNames = ['motorcycle.adrenaline', 'kikevelasquez777', 'indianmotorcycle', 'motorcycledreams', 'biker_mountains', 'caferacer.street']
#     usersDataFile = "D:\\g1080265\\instagram\\usersData.json"
#     with open(usersDataFile, 'r') as load_f:
#         usersData = json.load(load_f)
    
#     for user in userNames:
#         print( usersData[user] )
#         print('\n\n\n')

from datetime import datetime

print( datetime.fromtimestamp(1584028799) )





# from nltk.corpus import wordnet as wn

# car_synsets = wn.synsets('dog')

# for car in car_synsets:
#     print( car, end=' ' )
#     print( car.definition() )