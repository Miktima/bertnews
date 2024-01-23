import pandas as pd
import nltk
from io import StringIO
import random
import re

class GenError:

    def __init__(self):
        self.errorType = {
            1: ["ом", "ому"],
            2: ["ться" "тся"],
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

            70: ["также", "так же"],

            100: ["добавить букву"],
            101: ["убрать букву"],
            102: ["заменить букву"],
            103: ["убрать пробел"],
            104: ["переставить две буквы"]
        }

    def getLen(self):
        return len(self.errorType.keys())

    def getErr(self, type, text):
        find = False
        if type < 30:
            words = text.split()
            sh_words =random.shuffle(words)
            for w in sh_words:
                testw = re.sub(r'[^\w]', '', w.lower())

with open('datanews.json', encoding="utf-8") as f:
    read_data = f.read()
read_data = read_data.replace('\n][\n', ',\n')
articles = pd.read_json(StringIO(read_data), orient='records')

pst = nltk.PunktSentenceTokenizer()
sentences = pd.DataFrame({"text": [], "label": []})
for ind in articles.index:
    sentArticle = pst.tokenize(articles['Article'][ind])
    m = 0
    for s in sentArticle:
        if m != 1:
            sentences.loc[len(sentences.index)] = [s, 1]

error_list = []
with open('errorsents.txt', encoding="utf-8") as fe:
    error_list = fe.readlines()
for s in error_list:
    sentences.loc[len(sentences.index)] = [s, 0]

print("Number of correct sentences: ", len(sentences.index))
print("Number of incorrect sentences: ", len(error_list))

nadd = len(sentences.index) - len(error_list)
print ("Number of generated sentences: ", nadd)

random.seed()

sentError = GenError()
print (sentError.getLen())