import requests
import nltk
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import urllib3
import re
import time
import argparse
from transformers import AutoTokenizer, AutoModel, pipeline, logging

class getContent(HTMLParser):
    # HTML parser 
    def __init__(self, tag:str, attrs:list):
        self.tag = tag # tag of text block
        self.attrs = attrs # attributes of HTML element of text block
        self.intag = 0 # flag for parsing into specified tag
        self.result = ""
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        seta1 = set(self.attrs)
        seta2 = set(attrs)
        # Search for HTML element with tag and attribute
        if tag == self.tag and seta1 == seta2:
            self.intag = 1
    
    def handle_endtag(self, tag):
        if tag == self.tag and self.intag == 1:
            self.intag = 0

    def handle_data(self, data):
        # copy text data in they are into specifuied tag - attribute pair
        if self.intag == 1:
            self.result += data

def mask_bert_sent(text, model, tokenizer):
    # masking whole text and return errors if available
    tr = 0.00001 #threshold of the error (parameter !!!)
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

def addtags(inittext, tags, errors):
	# Функция добавления тегов к найденным в статье ошибкам
	# на входе: содержание статьи, срез с начальным и конечным тегами и структура с ошибками
	# на выходе - статья с тегами вокруг ошибок
	article_err = ""
	startPos = 0
	for e in errors:
		article_err += inittext[startPos:e['start']] + tags[0] + inittext[e['start']:e['end']] + tags[1]
		startPos = e['end']
	article_err += inittext[startPos:]
	return article_err

initTime = time.time()
urllib3.disable_warnings()
nltk.download('punkt')

userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit"
headers = {
    'user-agent': userAgent
    }

modelpath = "../model/fine-train-roberta"
tokenizer = AutoTokenizer.from_pretrained("ai-forever/ruRoberta-large")
model = AutoModel.from_pretrained(modelpath)

print ("Time initialization: ", time.time() - initTime)
logging.set_verbosity_error()

html_body = '<!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1">\
    		<meta http-equiv="X-UA-Compatible" content="IE=edge"> <title>Article errors</title> </head> <body>'
html_err = ""

parser = argparse.ArgumentParser()
parser.add_argument("--xml", help="use https://ria.ru/export/rss2/archive/index.xml for parsing",\
                    action="store_true")
parser.add_argument("--url", help="specify the URL artcile for parsing", type=str)
parser.add_argument("--file", help="specify the file artcile for parsing", type=str)
args = parser.parse_args()

if args.xml:
    xmlUrl = "https://ria.ru/export/rss2/archive/index.xml"
    xmlResponse = requests.get(xmlUrl, headers=headers, verify=False)
    
    root = ET.fromstring(xmlResponse.content)

    parser = getContent("div", [("class", "article__text")])
    for item in root.iter('item'):
        link = item.find("link").text
        article = ""
        htmlResponse = requests.get(link, headers=headers, verify=False)
        parser.feed((htmlResponse.content).decode('utf-8'))
        print ("Link: ", link)
        html_err += "<p>Link to the article: <a href='" + link + "'>" + link + "</a></p>"
        print ("---------------------")
        inittext = parser.result
        errors = mask_bert_sent(inittext, modelpath, tokenizer)
        # errors = mask_bert_sent(inittext.casefold(), modelpath, tokenizer)
        if len(errors) > 0:
            html_err += "<p>"
            textwe = addtags(inittext, ['<mark>', '</mark>'], errors)
            for e in errors:
                print (f"Incorrect world: {e['word']}, start: {e['start']}, end: {e['end']}, prob: {e['prob']}")
                html_err += f"<p>Incorrect world: {e['word']}, start: {e['start']}, end: {e['end']}, prob: {e['prob']}</p>\n"
            print ("Article with errors: ", textwe)
            html_err += "<p>" + textwe + "</p>\n"
        html_err += "<br><br>\n"
elif args.url is not None:
    link = args.url
    article = ""
    print ("Before request: ", time.time() - initTime)
    htmlResponse = requests.get(link, headers=headers, verify=False)
    parser = getContent("div", [("class", "article__text")])
    parser.feed((htmlResponse.content).decode('utf-8'))
    print ("After request: ", time.time() - initTime)
    print ("Link: ", link)
    html_err += "<p>Link to the article: <a href='" + link + "'>" + link + "</a></p>"
    print ("---------------------")
    inittext = parser.result
    errors = mask_bert_sent(inittext, modelpath, tokenizer)
    print ("After masking: ", time.time() - initTime)

    # errors = mask_bert_sent(inittext.casefold(), modelpath, tokenizer)
    if len(errors) > 0:
        html_err += "<p>"
        textwe = addtags(inittext, ['<mark>', '</mark>'], errors)
        for e in errors:
            print (f"Incorrect world: {e['word']}, start: {e['start']}, end: {e['end']}, prob: {e['prob']}")
            html_err += f"<p>Incorrect world: {e['word']}, start: {e['start']}, end: {e['end']}, prob: {e['prob']}</p>\n"
        print ("Article with errors: ", textwe)
        html_err += "<p>" + textwe + "</p>\n"
    html_err += "<br><br>\n"
elif args.file is not None:
    articlefile = args.file
    with open(articlefile, encoding="utf-8") as f:
        inittext = f.read()
    print ("File: ", articlefile)
    html_err += "<p>File with the article: " + articlefile + "</p>"
    print ("---------------------")
    errors = mask_bert_sent(inittext, modelpath, tokenizer)
    # errors = mask_bert_sent(inittext.casefold(), modelpath, tokenizer)
    if len(errors) > 0:
        html_err += "<p>"
        textwe = addtags(inittext, ['<mark>', '</mark>'], errors)
        for e in errors:
            print (f"Incorrect world: {e['word']}, start: {e['start']}, end: {e['end']}, prob: {e['prob']}")
            html_err += f"<p>Incorrect world: {e['word']}, start: {e['start']}, end: {e['end']}, prob: {e['prob']}</p>\n"
        print ("Article with errors: ", textwe)
        html_err += "<p>" + textwe + "</p>\n"
    html_err += "<br><br>\n"
else:
    print ("Wrong key")

# Выводим результаты проверки в файл
with open('errors.html', 'w', encoding='utf-8') as file:
    file.write(html_body+html_err+"</body>")
print ("The end: ", time.time() - initTime)