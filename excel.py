from openpyxl import Workbook

WV = Workbook()
WN = Workbook()

WVResult = WV.active
WNResult = WN.active

WVResult.append(['編號','帳號','問卷數量','問卷    cat',  '問卷  dog', 'Word2Vec  cat', 'Word2Vec  dog','距離'])
WNResult.append(['編號','帳號','問卷數量','問卷    cat',  '問卷  dog', 'Wordnet  cat', 'Wordnet  dog','距離'])

WV.save("example.xlsx")