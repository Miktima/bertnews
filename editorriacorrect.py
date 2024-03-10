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

sentList = []
pattern = re.compile(r"^[^-*\n\r\"\s]")
nstart = 0
nend = 1200
nl = 0
for l in read_list:
    smatch = pattern.search(l)
    if smatch:
        # Добавляем "правильное" предложение, если оно начинается не с пробела или кавычек,
        # а также символов -, * или перевод строки
        # Ставим точку в конце заголовка (первая строка после индекса)
        cl = html.unescape(l)
        parser = tagStripper()
        parser.feed(cl)
        clt = parser.get_data()
        if nl >= nstart:
            sentList.append(clt)
        if nl == nend:
            break
    nl += 1

with open('corrrectsents.txt', 'w', encoding='utf-8') as file:
    file.writelines(sentList)

