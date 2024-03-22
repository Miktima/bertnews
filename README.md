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
