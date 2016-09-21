# encoding=utf-8
import jieba
import pandas as pd

path = U'D:/Python27/py/Hound_V2/data/'
# target = '奶食'
target = '女装'
df = pd.read_csv(path+unicode(target,'utf-8')+'.csv',encoding='utf-8')

seq = df['title'].values
L = len(seq)
# print s
# seg_list = jieba.cut(s, cut_all=True)
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式

# seg_list = jieba.cut(s, cut_all=False)
# print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

seg_lists = []
for i in range(len(seq)):
	seg_list = jieba.lcut_for_search(seq[i])  # 搜索引擎模式
	seg_lists.extend(seg_list)

words = seg_lists	
word_freq = {}
for word in words:
    if word in word_freq:
        word_freq[word] += 1
    else:
        word_freq[word] = 1

freq_word = []
for word, freq in word_freq.items():
    freq_word.append((word, freq))
freq_word.sort(key = lambda x: x[1], reverse = True)

# max_number = int(raw_input(u"需要前多少位高频词？ "))
max_number = 50
for word, freq in freq_word[: max_number]:
    print word, freq/float(L)