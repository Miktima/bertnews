import re
import requests
import pandas as pd
from transformers import AutoTokenizer, AutoModel, pipeline, logging
import nltk
import time



def mask_bert_sent(text, model, tokenizer):
    # masking whole text and return errors if available
    tr = 0.000003 #threshold of the error (parameter !!!)
    unmasker = pipeline("fill-mask", model=model, tokenizer=tokenizer)
    p = re.compile(r'[\w-]+')
    sentArticle = nltk.tokenize.sent_tokenize(text, language="russian")
    listErr = []
    ind = 0
    for s in sentArticle:
        ind = text.index(s)
        iter = p.finditer(s)
        for match in iter:
            if match.start() == 0:
                masktext = "[MASK]" + s[match.end():]
            elif match.end() == len(s):
                masktext = s[:match.start()] + "[MASK]"
            else:
                masktext = s[:match.start()] + "[MASK]" + s[match.end():]
            res = unmasker(masktext, targets=[match.group()], batch_size=8)
            if res[0]['score'] < tr:
                errorrDesc = {
                    "word": match.group(),
                    "start": ind + match.start(),
                    "end": ind + match.end(),
                    "prob": res[0]['score']
                }
                listErr.append(errorrDesc)
    return listErr

initTime = time.time()

nltk.download('punkt')

modelpath = "../model/fine-train256"
tokenizer = AutoTokenizer.from_pretrained("ai-forever/ruBert-base")
model = AutoModel.from_pretrained(modelpath)

print ("Time initialization: ", time.time() - initTime)
logging.set_verbosity_error()

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

p = re.compile(r'[\w-]+')

TP = 0
TN = 0
FP = 0
FN = 0

for ind in sentences.index:
    if (ind % 10) == 0:
        print ("Index: ", ind, "   Time:", time.time() - initTime)
    response = mask_bert_sent(sentences["sentences"][ind], modelpath, tokenizer)
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
            # found errors correct or not
            iscorrect = 0
            for trueerr in sentences["errors_pos"][ind]:
                if trueerr[0] == e["start"]:
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









