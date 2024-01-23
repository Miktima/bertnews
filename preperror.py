import pandas as pd
import numpy as np
import nltk
from transformers import AutoTokenizer, DataCollatorWithPadding, TrainingArguments, Trainer, AutoModel
from datasets import Dataset
import evaluate
from io import StringIO

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
