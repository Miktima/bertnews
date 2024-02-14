import re
import numpy as np
import pandas as pd

with open('errorsents.txt', encoding="utf-8") as f:
    sent_list = f.readlines()
i = 0
for s in sent_list:
    errormask_Sent = re.sub("_[\w\s-]+_", "[ERR]", s)
    words = errormask_Sent.split()
    print (words)
    if i == 3:
        break
    i += 1
    








