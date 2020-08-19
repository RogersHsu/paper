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

    for i in range(0, len(qScores[user]['dog'])):
        qDog = qScores[user]['dog'][i]
        qCat = qScores[user]['cat'][i]
        plt.scatter(qDog, qCat, s=100, c='r', marker='o')
    
    plt.xlim(0, 105)
    plt.ylim(0, 105)

    #设置坐标轴刻度
    my_x_ticks = np.arange(0, 105, 10)
    my_y_ticks = np.arange(0, 105, 10)
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)

    plt.xlabel("dog")               #設定X軸名稱
    plt.ylabel("cat")               #設定Y軸名稱

    plt.title(user)

    plt.scatter(120, 120, label='Questionare', c='r', s=100, marker='o')


    plt.legend(loc='lower left')
    plt.show()