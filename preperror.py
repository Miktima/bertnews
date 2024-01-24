import pandas as pd
import nltk
from io import StringIO
import random
import re

class GenError:

    def __init__(self):
        self.errorType = {
            1: ["ом", "ому"],
            2: ["ться", "тся"],
            3: ["ный", "ным"],
            4: ["кий", "ких"],
            5: ["ой", "ий"],
            6: ["ою", "ую"],
            7: ["ии", "ие"],
            8: ["ом", "ым"],
            9: ["им", "ем"],
            10: ["ая", "ый"],
            11: ["ны", "ну"],
            12: ["сти", "сть"],
            13: ["ют", "ет"],
            14: ["уют", "ую"],
            15: ["ий", "ии"],
            16: ["ство", "ства"],

            30: ["нн", "н"],

            50: ["своею", "свою"],
            51: ["также", "так же"],

            100: ["добавить букву"],
            101: ["убрать букву"],
            102: ["заменить букву"],
            103: ["убрать пробел"],
            104: ["переставить две буквы"]
        }
        self.rusLetters = "абвгдежзийклмнопрстуфхцчшщыэюя"
        random.seed()

    def getLen(self):
        return len(self.errorType.keys())

    def getErr(self, text):
        keys = list(self.errorType.keys())
        random.shuffle(keys)
        find = 0
        while find < 1:
            for etype in keys:
                if etype < 30:
                    pattern = re.compile(r"([\w-]+" + self.errorType[etype][0] + r"\b)")
                    msamples = pattern.findall(text)
                    if msamples:
                        random.shuffle(msamples)
                        sample = msamples[0]
                        newword = re.sub(self.errorType[etype][0] + r"$", self.errorType[etype][1], sample)
                        return re.sub(sample, newword, text, count=1)
                    pattern = re.compile(r"([\w-]+" + self.errorType[etype][1] + r"\b)")
                    msamples = pattern.findall(text)
                    if msamples:
                        random.shuffle(msamples)
                        sample = msamples[0]
                        newword = re.sub(self.errorType[etype][1] + r"$", self.errorType[etype][0], sample)
                        return re.sub(sample, newword, text, count=1)
                elif etype >= 30 and etype < 50:
                    pattern = re.compile(r"([\w-]+" + self.errorType[etype][0] + r")")
                    msamples = pattern.findall(text)
                    if msamples:
                        random.shuffle(msamples)
                        sample = msamples[0]
                        newword = re.sub(self.errorType[etype][0] + r"$", self.errorType[etype][1], sample)
                        return re.sub(sample, newword, text, count=1)                    
                elif etype >= 50 and etype < 70:
                    pattern = re.compile(r"(\b" + self.errorType[etype][0] + r"\b)")
                    msample = pattern.search(text)
                    if msample:
                        return re.sub(msample.group(1), self.errorType[etype][1], text, count=1)                    
                    pattern = re.compile(r"(\b" + self.errorType[etype][1] + r"\b)")
                    msample = pattern.search(text)
                    if msample:
                        return re.sub(msample.group(1), self.errorType[etype][0], text, count=1)                    
                elif etype == 100: # add a letter
                    pattern = re.compile(r"([\w-]+)")
                    msamples = pattern.findall(text)
                    if msamples:
                        random.shuffle(msamples)
                        sample = msamples[0]
                        pos = random.randrange(0, len(sample))
                        letter = random.choices(self.rusLetters , k=1)
                        if pos == 0:
                            newword = letter[0] + sample
                        elif pos == len(sample):
                            newword = sample + letter[0]
                        else:
                            newword = sample[:pos] + letter[0] + sample[pos:]
                        return re.sub(sample, newword, text, count=1)
                elif etype == 101: # remove a letter
                    pattern = re.compile(r"([\w-]+)")
                    msamples = pattern.findall(text)
                    if msamples:
                        random.shuffle(msamples)
                        sample = msamples[0]
                        pos = random.randrange(0, len(sample))
                        if pos == 0:
                            newword = sample[1:]
                        elif pos == len(sample):
                            newword = sample[:pos-1]
                        else:
                            newword = sample[:pos] + sample[pos+1:]
                        return re.sub(sample, newword, text, count=1)
                elif etype == 102: # change a letter
                    pattern = re.compile(r"([\w-]+)")
                    msamples = pattern.findall(text)
                    if msamples:
                        random.shuffle(msamples)
                        sample = msamples[0]
                        pos = random.randrange(0, len(sample))
                        letter = random.choices(self.rusLetters , k=1)
                        if pos == 0:
                            newword = letter[0] + sample[1:]
                        elif pos == len(sample):
                            newword = sample[:pos-1] + letter[0]
                        else:
                            newword = sample[:pos] + letter[0] + sample[pos+1:]
                        return re.sub(sample, newword, text, count=1)
                elif etype == 103: # remove a space
                    pattern = re.compile(r"([\w-]+\s[\w-]+)")
                    msamples = pattern.findall(text)
                    if msamples:
                        random.shuffle(msamples)
                        sample = msamples[0]
                        newword = re.sub(r"\s", "", sample)
                        return re.sub(sample, newword, text, count=1)                    
                elif etype == 104: # rearrange two letters
                    pattern = re.compile(r"([\w-]{2,})")
                    msamples = pattern.findall(text)
                    if msamples:
                        random.shuffle(msamples)
                        sample = msamples[0]
                        pos = random.randrange(0, len(sample))
                        if pos == 0:
                            newword = sample[1] + sample[0]
                            if len(sample) > 2:
                                newword += sample[2:]
                        elif pos == len(sample)-1:
                            newword = sample[:pos-2] + sample[pos-1] + sample[pos-2]
                        else:
                            newword = sample[:pos-1] + sample[pos] + sample[pos-1] + sample[pos+1:]
                        return re.sub(sample, newword, text, count=1)
                    
            find = 1

nltk.download('punkt')
with open('datanews.json', encoding="utf-8") as f:
    read_data = f.read()
read_data = read_data.replace('\n][\n', ',\n')
articles = pd.read_json(StringIO(read_data), orient='records')

# pst = nltk.PunktSentenceTokenizer()
sentList = []
pattern = re.compile(r"\n[\w]+,\s\d+.+РИА Новости", re.IGNORECASE)
patred = re.compile(r"прим. ред.", re.IGNORECASE)
for ind in articles.index:
    sentArticle = nltk.tokenize.sent_tokenize(articles['Article'][ind], language="russian")
    for s in sentArticle:
        riamatch = pattern.findall(s)
        if riamatch:
            s = pattern.sub("", s)
        w = nltk.tokenize.word_tokenize(s, language="russian")
        matchred = patred.search(s)
        if len(w) <= 3 or matchred:
            print (s)           
        else:
            sentList.append(s)

error_list = []
with open('errorsents.txt', encoding="utf-8") as fe:
    error_list = fe.readlines()

print("Number of correct sentences: ", len(sentList))
print("Number of incorrect sentences: ", len(error_list))

nadd = len(sentList) - len(error_list)
print ("Number of generated sentences: ", nadd)

random.seed()
random.shuffle(sentList)

sentError = GenError()
i = 0
listGenEr = []
for row in sentList:
    listGenEr.append(sentError.getErr(row) + "\n")
    i += 1
    if i == nadd:
        break
with open('errorsents2.txt', 'w') as file:
    file.writelines(listGenEr)

datanews = pd.DataFrame({"text": [], "label": []})
# checked data
for s in sentList:
    datanews.loc[len(datanews.index)] = [s, 1]
# real error data
for s in error_list:
    datanews.loc[len(datanews.index)] = [s, 0]
# generated error data
for s in listGenEr:
    datanews.loc[len(datanews.index)] = [s, 0]

datanews.to_json('FullDN.json') 

