import pandas as pd
import json
import re
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


with open('processed-ria.json', encoding="utf-8") as f:
    read_list = f.readlines()

sentList = []
ncount = 0 # счетчик статей
nlimit = 5000 # количество статей
pattern = re.compile(r"[\w]+,\s\d+[\w\-—\s]+риа новости[,\s\w]*.", re.IGNORECASE)
for l in read_list:
    d = json.loads(l)
    t = re.sub('&nbsp;', ' ', d['text'])
    t = re.sub('&mdash;', '-', t)
    parser = tagStripper()
    parser.feed(t)
    tt = parser.get_data()
    riamatch = pattern.findall(tt)
    if riamatch:
        s = pattern.sub("", tt)
    else:
        s = tt
    title = re.sub('&nbsp;', ' ', d['title'])
    title = re.sub('&mdash;', '-', title)
    sentList.append(title + ". " + s)
    ncount += 1
    if ncount % 10000 == 0:
        print ("Number of articles: ", ncount)

labels = [1] * len(sentList)
all_datanews = pd.DataFrame(list(zip(sentList, labels)))
all_datanews.columns =['text', 'label']
# checked data
datanews = all_datanews.sample(n=nlimit)

with open('gitriaDN_rnd.json', 'w', encoding='utf-8') as file:
    datanews.to_json(file, force_ascii=False)

