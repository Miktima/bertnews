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
artText = ''
pattern = re.compile(r"-{4}(\d+)-{4}")
i = 0
for l in read_list:
    idmatch = pattern.search(l)
    if idmatch:
        if len(artText) > 0:
            artText['text'] = artText
            artList.append(artDict)
        artDict = {
            'id': idmatch.group(1),
            'text': ''
        }
    else:
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

