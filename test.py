import re
import torch
from transformers import AutoTokenizer, AutoModel
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny2")
model = AutoModel.from_pretrained("cointegrated/rubert-tiny2")
# model.cuda()  # uncomment it if you have a GPU

def embed_bert_cls(text, model, tokenizer):
    t = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**{k: v.to(model.device) for k, v in t.items()})
    embeddings = model_output.last_hidden_state[:, 0, :]
    embeddings = torch.nn.functional.normalize(embeddings)
    return embeddings[0].cpu().numpy()

def mask_bert_sent(text, model, tokenizer):
    unmasker = pipeline("fill-mask", model="cointegrated/rubert-tiny2", tokenizer=tokenizer)
    p = re.compile(r'[\w-]+')
    iter = p.finditer(text)
    for match in iter:
        if match.start() == 0:
            masktext = "[MASK]" + text[match.end():]
        elif match.end() == len(text):
            masktext = text[:match.start()] + "[MASK]"
        else:
            masktext = text[:match.start()] + "[MASK]" + text[match.end():]
        print ("Masktext: ", masktext)
        print(unmasker(masktext))
    return


# print(embed_bert_cls('привет мир', model, tokenizer).shape)

text = "После начала российской военной спецоперации на Украине западные страны усилили санкционное давление на Москву"
mask_bert_sent(text, "cointegrated/rubert-tiny2", tokenizer)


