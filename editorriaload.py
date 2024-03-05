import pandas as pd
import json
import re
import html
from html.parser import HTMLParser
from io import StringIO

class tagStripper(HTMLParser):
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
for l in read_list:
    idmatch = pattern.search(l)
    if idmatch:
        nln = 0
        # Добавляем индекс при первом нахождении, а текст к этому индексу при втором
        # Если индекс = 0, выходим 
        if len(artText) > 0:
            artList.append(artText)
            artText = ''
        if int(idmatch.group(1)) == 0:
            break
        else:
            indList.append(idmatch.group(1))
    else:
        # Ставим точку в конце заголовка (первай строка после индекса)
        if nln == 0:
            nln += 1
            l = re.sub(r'\n', r'.\n', l)
        if re.match(r'[^\n\r]+', l):
            cl = html.unescape(l)
            parser = tagStripper()
            parser.feed(cl)
            clt = parser.get_data()
            artText += clt

datanews = pd.DataFrame(list(zip(artList, indList)))
datanews.columns =['text', 'id']

grp = datanews['id'].groupby(datanews['id']).filter(lambda x: len(x) > 1).value_counts()
# checked data

with open('editorriaDN.json', 'w', encoding='utf-8') as file:
    datanews.to_json(file, force_ascii=False)

with open('grp.json', 'w', encoding='utf-8') as file:
    grp.to_json(file, force_ascii=False)
