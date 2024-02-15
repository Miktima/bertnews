import re
import requests
import pandas as pd
import urllib.parse
import urllib3

urllib3.disable_warnings()
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
p = re.compile(r'[\w-]+')

TP = 0
TN = 0
FP = 0
FN = 0

for ind in sentences.index:
    if (ind % 10) == 0:
        print ("Index: ", ind)
    # Формируем текст запроса в urlencoded
    context = "text=" + urllib.parse.quote_plus(sentences["sentences"][ind]) + "&lang=" + urllib.parse.quote_plus(splang)\
         + "&options=" + spoptions + "&format=" + spformat
    # Отправляем POST запрос
    request = requests.post(httpposturl, data=context, headers={"Content-Type": "application/x-www-form-urlencoded"}, verify=False)
    response = request.json()
    if len(response) == 0:
        # No errors found
        ntoken = len(p.findall(sentences["sentences"][ind]))
        nerr = len(sentences["errors_pos"][ind])
        # True Negative = number of words without errors
        TN += ntoken - nerr
        # False Negative - nerr errors were not found
        FN += nerr
    else:
        # errors were found: iter by found errors
        nfound = 0
        for e in response:
            # Only for error code = 1 (unknown word)
            if e["code"] == 1:
                # found errors correct or not
                iscorrect = 0
                for trueerr in sentences["errors_pos"][ind]:
                    if trueerr[0] == e["pos"]:
                        iscorrect = 1
                        nfound += 1
                        break
                if iscorrect == 1:
                    # True Positive - error word was found
                    TP += 1
        # False Positive - wrong errors were found
        if (len(response) - nfound) > 0:
            FP += len(response) - nfound
        # False Negative - errors were not found
        if (len(sentences["errors_pos"][ind]) - nfound) > 0:
            FN += len(sentences["errors_pos"][ind]) - nfound

precision = TP / (TP + FP)
recall = TP / (TP + FN)
fmeasure = 2 * recall * precision / (recall + precision)
print ("Precision: ", precision)
print ("Recall: ", recall)
print ("F-measure: ", fmeasure)









