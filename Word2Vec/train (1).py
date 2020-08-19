import time

# -*- coding: utf-8 -*-
__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
import warnings
warnings.filterwarnings(action = 'ignore', category = UserWarning, module = 'gensim')
from gensim.models import word2vec
import multiprocessing

# 主要透過 gensim 訓練成 model 並供使用
class Train(object):

	def __init__(self):
		pass

	# 可參考 https://radimrehurek.com/gensim/models/word2vec.html 更多運用
	def train(self):
		print("訓練中...(喝個咖啡吧^0^)")
		# Load file
		sentence = word2vec.Text8Corpus("D:\\word2vec\\trash\\segmentation.txt")
		# Setting degree and Produce Model(Train)
		model = word2vec.Word2Vec(sentence, size = 300, window = 5, min_count = 10, iter=5, sg=1, workers=4)
		# Save model
		model.wv.save_word2vec_format(u"D:\\word2vec\\model\\zhfn300w5m10it5sg1.model.bin", binary = True)
		print("model1 已儲存完畢")

if __name__ == "__main__":

	start = time.time()

	t = Train()
	# 訓練(shallow semantic space)
	t.train()

	end = time.time()
	spend = end - start
	hour = spend // 3600
	minu = (spend - 3600 * hour) // 60
	sec = spend - 3600 * hour - 60 * minu
	
	print(f'一共花費了{hour}小時{minu}分鐘{sec}秒')