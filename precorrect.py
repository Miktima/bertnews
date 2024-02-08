import pandas as pd

from io import StringIO
import random
import re

with open('datanews.json', encoding="utf-8") as f:
    read_data = f.read()
read_data = read_data.replace('\n][\n', ',\n')
articles = pd.read_json(StringIO(read_data), orient='records')

sentList = []
# "РИА Новости" не убираем, а позле заголовка ставим точку
#pattern = re.compile(r"\n[\w]+,\s\d+.+РИА Новости", re.IGNORECASE)
for ind in articles.index:
#    riamatch = pattern.findall(articles['Article'][ind])
#    if riamatch:
#        s = pattern.sub("", articles['Article'][ind])
#    else:
#        s = articles['Article'][ind]
    s = re.sub("\n", ". ", articles['Article'][ind])
    sentList.append(s)

datanews = pd.DataFrame({"text": [], "label": []})
# checked data
for s in sentList:
    datanews.loc[len(datanews.index)] = [s, 1]

with open('CorrectDN.json', 'w', encoding='utf-8') as file:
    datanews.to_json(file, force_ascii=False)

