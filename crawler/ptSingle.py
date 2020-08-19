from openpyxl import Workbook

import json
import matplotlib.pyplot as plt    #引入函式庫
import numpy as np
import math


qScoresFile = "D:\\g1080265\\instagram\\questionnaire_scores.json"
with open(qScoresFile, 'r') as load_f:
    qScores = json.load(load_f)

animalDataFile = "D:\\g1080265\\instagram\\animal.json"
with open(animalDataFile, 'r') as load_f:
    animalScore100 = json.load(load_f)

color = ['m', 'y', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
marker = []

animalUsers = [ line.rstrip('\n') for line in open('D:\\g1080265\\instagram\\questionnaire_animal.txt', 'r') if line.rstrip('\n') != '']


for user in animalUsers:

    qDog = round( (sum( qScores[user]['dog'] )/len(qScores[user]['dog'])),2 )
    qCat = round( (sum( qScores[user]['cat'] )/len(qScores[user]['cat'])),2 )
    wvDog = animalScore100[user]['word2vec']["dog"]
    wvCat = animalScore100[user]['word2vec']["cat"]
    wnDog = animalScore100[user]['wordnet']["dog"]
    wnCat = animalScore100[user]['wordnet']["cat"]

    plt.xlim(0, 100)
    plt.ylim(0, 100)

    #设置坐标轴刻度
    my_x_ticks = np.arange(0, 101, 10)
    my_y_ticks = np.arange(0, 101, 10)
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)

    # 
    plt.scatter(qDog, qCat, s=100, c='r', marker='o')
    plt.annotate("({},{})".format(qDog, qCat), xy=(qDog, qCat), xytext=(5, 0), textcoords='offset points',ha='left', va='center') #label on each point

    plt.scatter(wvDog, wvCat, s=100, c='b', marker='*')
    plt.annotate("({},{})".format(wvDog, wvCat), xy=(wvDog, wvCat), xytext=(5, 0), textcoords='offset points',ha='left', va='center') #label on each point
    # plt.annotate(i, xy=(wvDog, wvCat), xytext=(5, 0), textcoords='offset points',ha='left', va='center') #label on each point

    plt.scatter(wnDog, wnCat, s=100, c='g', marker='^')
    plt.annotate("({},{})".format(wnDog, wnCat), xy=(wnDog, wnCat), xytext=(5, 0), textcoords='offset points',ha='left', va='center') #label on each point
    # plt.annotate(i, xy=(wnDog, wnCat), xytext=(5, 0), textcoords='offset points',ha='left', va='center') #label on each point

    plt.xlabel("dog")               #設定X軸名稱
    plt.ylabel("cat")               #設定Y軸名稱

    plt.title(user)

    plt.scatter(120, 120, label='Questionare', c='r', s=100, marker='o')
    plt.scatter(120, 120, label='Word2Vec', c='b', s=100, marker='*')
    plt.scatter(120, 120, label='Wordnet', c='g', s=100, marker='^')

    plt.legend(loc='lower left')
    plt.show()