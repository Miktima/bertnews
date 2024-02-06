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


with open('ria_20.json', encoding="utf-8") as f:
    read_list = f.readlines()

sentList = []
pattern = re.compile(r"^[\w]+,\s\d+[\w\-—\s]+риа новости[,\s\w]*.", re.IGNORECASE)
for l in read_list:
    d = json.loads(l)
    parser = tagStripper()
    parser.feed(d['text'])
    tt = parser.get_data()
    riamatch = pattern.findall(tt)
    if riamatch:
        s = pattern.sub("", tt)
    else:
        s = tt
    sentList.append(d['title'] + ". " + s)

datanews = pd.DataFrame({"text": [], "label": []})
# checked data
for s in sentList:
    datanews.loc[len(datanews.index)] = [s, 1]

with open('gitriaDN.json', 'w', encoding='utf-8') as file:
    datanews.to_json(file, force_ascii=False)

