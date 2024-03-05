import pandas as pd
import json
import re
import html
from io import StringIO

class tagStripper(html.parser.HTMLParser):
    # HTML stripper 
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()


with open('EDWHITE5510.txt', encoding="utf-8") as f:
    read_list = f.readlines()

artList = []
indList = []
artText = ''
pattern = re.compile(r"-{4}(\d+)-{4}")
i = 0
for l in read_list:
    idmatch = pattern.search(l)
    if idmatch:
        nln = 0
        # Добавляем индекс при первом нахождении, а текст к этому индексу при втором
        # Если индекс = 0, выходим 
        if len(artText) > 0:
            artList.append(artText)
        if int(idmatch.group(1)) == 0:
            break
        else:
            indList.append(idmatch.group(1))
    else:
        # Ставим точку в конце заголовка (первай строка после индекса)
        if nln == 0:
            nln += 1
            l = re.sub(r'\n', r'\.\n', l)
        if re.match()
        cl = html.unescape(l)
        parser = tagStripper()
        parser.feed(cl)
        clt = parser.get_data()
    ncount += 1
    if ncount % 10000 == 0:
        print ("Number of articles: ", ncount)
    if ncount == nlimit + nfrom:
        break

nrow = 0
labels = [1] * len(sentList)
datanews = pd.DataFrame(list(zip(sentList, labels)))
datanews.columns =['text', 'label']
# checked data

with open('gitriaDN.json', 'w', encoding='utf-8') as file:
    datanews.to_json(file, force_ascii=False)

