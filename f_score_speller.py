import re
import requests
import numpy as np
import pandas as pd
import urllib.parse

httpposturl = "https://speller.yandex.net/services/spellservice.json/checkText"

with open('errorsents.txt', encoding="utf-8") as f:
    sentmarked_list = f.readlines()

errPattern = re.compile("_([\w\s-]+)_")
sent_list = []
errtup_list = []
for s in sentmarked_list:
    errIter = errPattern.finditer(s)
    ss = re.sub("_", "", s)
    sent_list.append(ss)
    j = 0
    errtup = []
    for err in errIter:
        errtup.append((err.start()-j*2, err.end()-2*(1 + j)))
        j += 1
    errtup_list.append(errtup)

sentences = pd.DataFrame(list(zip(sent_list, errtup_list)), columns =['sentences', 'errors_pos'])

httpposturl = "https://speller.yandex.net/services/spellservice.json/checkText"
splang = "ru,en"
spoptions = "14"
spformat = "plain"
# Формируем текст запроса в urlencoded
text = "Точные данные по повffрежденном имуществу станут известны после поквартирного обхода."
# context = "text=" + sentences["sentences"][0] + "&lang=" + splang + "&options=" + spoptions + "&format=" + spformat
context = "text=" + text + "&lang=" + splang + "&options=" + spoptions + "&format=" + spformat
print (context)
context = urllib.parse.quote_plus(context)
print (context)
# Отправляем POST запрос
request = requests.post(httpposturl, data=context, headers={"Content-Type": "application/x-www-form-urlencoded"}, verify=False)
print (request.json())








