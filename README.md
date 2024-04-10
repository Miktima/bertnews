# R&D LLM model for spelling news in Russian
## Included files
### DATA corpus
* **CorrectDN.json** - JSON file with corrected news articles. The articles were saved after editor reviews twice or more times and checked by
[Yandex Speller](https://yandex.ru/dev/speller/). The file is saved with pandas.DataFrame.to_json method in file **precorrect.py**. The file is used for fune-tuning models
* **datanews.json** - Raw articles with url. It is a source for CorrectDN.json. Also see [copyright RIA.RU](https://ria.ru/docs/about/copyright.html)
* **FullDN.json** - JSON file with checked artciles, real error sentences and synthetic error sententes. The file is saved with pandas.DataFrame.to_json method in file **preperror.py**
* **gitriaDN.json** - slice from https://github.com/RossiyaSegodnya/ria_news_dataset. It is generated with **gitriaload.py** or **gitriaload_rnd.py**
* **correctsents.txt** - Checked sentences (almost) whithout error. The data will be wrapped in JSON later. The file is used for F-score calculation.
* **EDWHITE5510.txt** - Raw data from editors.
* **errorsents.txt** - Sentences with real errors. The data will be wrapped in JSON later. The file is used for F-score calculation.

### Python files
* **editorriacorrect.py** - generates **correctsents.txt**
* **editorriaload.py** - generates **editorriaDN.json** file from **EDWHITE5510.txt** the same format as **CorrectDN.json**. The **editorriaDN.json** file is (temporarily?) used for fune-tuning models
* **f_score_speller.py** - calculate f-score for [Yandex Speller](https://yandex.ru/dev/speller/).
* **gitriaload.py** - takes **first** *n* articles from https://github.com/RossiyaSegodnya/ria_news_dataset.
* **gitriaload_rnd.py** - takes **random** *n* articles from https://github.com/RossiyaSegodnya/ria_news_dataset.
* **precorrect.py** - generates **CorrectDN.json**
* **preperror.py** - generates **FullDN.json**
* **test_answer.py** - the algorithm test of finding error words from answer of m2m100 model.

### Notebooks
* **FT_MaskedLM.ipynb** - fine-tune of masked language modeles (excluding ruRoberta) (Colab)
* **FT_MaskedLM_ruRoberta.ipynb** - fine-tune of the ruRoberta model (Colab)
* **FT_M2M100.ipynb** - fine-tune RuM2M100-1.2B model (dev) (Colab)
* **F_score_model.ipynb** - F-score calculation for masked language modeles (Colab)
* **F_score_M2M100.ipynb** - F-score calculation by corrected words for RuM2M100-1.2B model (Colab)
* **F_score_M2M100_token.ipynb** - F-score calculation by tokens for RuM2M100-1.2B model (Colab)
* **Fscore.ipynb** - Results of F-score. **Fscore old.ipynb** - old version
* **FT_AF_rubert_results.ipynb**, **FT_AF_ruRoberta_results.ipynb**, **FT_DeepPavlov_results.ipynb** - results of fine-tining
* **LRate_ruBert-tiny2.ipynb** - Results of Leaning rate ruBert-tiny2
* **Spell_article.ipynb** - spell-checking articles from https://ria.ru/. Checking URL = articleURL