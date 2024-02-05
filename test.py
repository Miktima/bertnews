import requests
import nltk
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import urllib3
import re
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
    # maskin whole text and return errors if available
    tr = 0.0001 #threshold of the error (parameter !!!)
    unmasker = pipeline("fill-mask", model=model, tokenizer=tokenizer)
    p = re.compile(r'[\w-]+')
    text = '''Ранее в четверг лидеры Европейского союз единогласно согласовали выделение Украине макрофинансовой помощи в размере 50 миллиардов евро на период до 2027 года с условием ежегодной отчетности со стороны ЕК и дебатов в Евросовете. Как сообщил премьер-министр Польши Дональд Туск, главу венгерского правительства Виктора Орбана "удалось убедить".
Позиция Будапешта оставалась главным препятствием для выделения денег киевским властям. Как выяснила газета Financial Times, лидеры стран Евросоюза могли публично объявить на саммите о неконструктивном поведении Орбана и отказать Венгрии в разморозке средств из европейских фондов.
Как подчеркивал сам венгерский премьер, такое развитие событий привело бы к армагеддону. Он заявил, что европейцам 50 миллиардов евро нужны не меньше, чем украинцам, но предложил компромисс: не выделять всю сумму сразу на четыре года, а утверждать финансирование для Киева ежегодно и единогласно.'''
    sentArticle = nltk.tokenize.sent_tokenize(text, language="russian")
    listErr = []
    i = 0
    for s in sentArticle:
        if i == 1:
            break
        print (s)
        iter = p.finditer(s)
        j = 0
        for match in iter:
            if j == 3:
                break
            if match.start() == 0:
                masktext = "[MASK]" + s[match.end():]
            elif match.end() == len(s):
                masktext = s[:match.start()] + "[MASK]"
            else:
                masktext = s[:match.start()] + "[MASK]" + s[match.end():]
            print (masktext)
            res = unmasker(masktext, targets=[match.group()])
            if res[0]['score'] < tr:
                errorrDesc = {
                    "word": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                    "prob": res[0]['score']
                }
                listErr.append(errorrDesc)
            j += 1
        i += 1
    return listErr


urllib3.disable_warnings()
nltk.download('punkt')

userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit"
headers = {
    'user-agent': userAgent
    }

modelpath = "../model/fine-train"
tokenizer = AutoTokenizer.from_pretrained("DeepPavlov/rubert-base-cased")
model = AutoModel.from_pretrained(modelpath)

logging.set_verbosity_error()

parser = argparse.ArgumentParser()
parser.add_argument("--xml", help="use https://ria.ru/export/rss2/archive/index.xml for parsing",\
                    action="store_true")
args = parser.parse_args()

if args.xml:
    xmlUrl = "https://ria.ru/export/rss2/archive/index.xml"
    xmlResponse = requests.get(xmlUrl, headers=headers, verify=False)
    
    root = ET.fromstring(xmlResponse.content)
    
    html_body = '<!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1">\
    		<meta http-equiv="X-UA-Compatible" content="IE=edge"> <title>Article errors</title> </head> <body>'
    
    i = 0
    parser = getContent("div", [("class", "article__text")])
    for item in root.iter('item'):
        if i == 5:
            link = item.find("link").text
            article = ""
            htmlResponse = requests.get(link, headers=headers, verify=False)
            parser.feed((htmlResponse.content).decode('utf-8'))
            print ("Link: ", link)
            html_body += "<p>Link to the article: <a href='" + link + "'>" + link + "</a></p>"
            print ("---------------------")
            html_body += "<p>"
            # print (parser.result)
            inittext = parser.result
            errors = mask_bert_sent(inittext, modelpath, tokenizer)
            textwe = ""
            if len(errors) > 0:
                for e in errors:
                    print (e)
            else:
                textwe = inittext
            html_body += textwe
        i += 1
else:
    print ("Wrong key")


