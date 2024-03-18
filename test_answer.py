import re

def levenshtein_distance(s, t):
    m, n = len(s), len(t)
    if m < n:
        s, t = t, s
        m, n = n, m
    d = [list(range(n + 1))] + [[i] + [0] * n for i in range(1, m + 1)]
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if s[i - 1] == t[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(d[i - 1][j], d[i][j - 1], d[i - 1][j - 1]) + 1
    return d[m][n]

def compute_similarity(input_string, reference_string):
    distance = levenshtein_distance(input_string, reference_string)
    max_length = max(len(input_string), len(reference_string))
    similarity = 1 - (distance / max_length)
    return similarity

text_lst = [
    "Точные данные по поврежденном имуществу станут известны после поквартирного обхода.",
    "Сегодня наши войны могли помолиться и причастится перед святым образом.",
    "Конституционным суд украл мандат депутата от оппозиции, который народ предоставил БКС.",
    "Мужчина признан виновным по двумя статьям УК РФ: ч. 3 ст. 30, ч. 3 ст. 205 (покушение на теракт) и ч. 1 ст. 275 (госизмена).",
    "В Кремле заявляли, что накачивание Украиныоружием со стороны Запада не способствует успеху российско-украинских переговоров и будет иметь негативный эффект.",
    "Патриарх так же затронул вопрос о деятельности православных школ и гимназий, которых в стране, по его мнению, не хватает.",
    "Викторина, посвященной 80-летнию освобождения Новгорода от немецко-фашистских захватчиков, стартовала с середины февраля."
]
answer_lst = [
    "Точные данные по поврежденному имуществу станут известны после поквартирного обхода.",
    "Сегодня наши воины могли помолиться и причаститься перед святым образом.",
    "Конституционный суд украл мандат депутата от оппозиции, который народ предоставил БКС.",
    "Мужчина признан виновным по двум статьям УК РФ: ч. 3 ст. 30, ч. 3 ст. 205 (покушение на теракт) и ч. 1 ст. 275 (госизмена).",
    "В Кремле заявляли, что накачивание Украины оружием со стороны Запада не способствует успеху российско-украинских переговоров и будет иметь негативный эффект.",
    "Патриарх также затронул вопрос о деятельности православных школ и гимназий, которых в стране, по его мнению, не хватает.",
    "Викторина, посвященная 80-летию освобождения Новгорода от немецко-фашистских захватчиков, стартовала с середины февраля."
]
errw = []
p = re.compile(r'[\w-]+')
for i in range(len(text_lst)):
    s = text_lst[i]
    a = answer_lst[i]
    sw_list = s.split()
    aw_list = a.split()
    offset = 0
    merged = 0

    # Проходим по всем словам в исходном предложении
    for nw in range(len(sw_list)):
        cs = compute_similarity(sw_list[nw], aw_list[nw+offset])
        # Если merged = -1 (то есть правильное слово слито, то пропускаем цикл)
        if offset > -1:
            # Если похожесть между 1 и 0.8, то считаем, что это ошибка в одном слове (сдвиг = 0)
            if cs < 1 and cs >=0.8:
                errw.append((nw, 0))
            # Если похожесть меньше либо равна 0.6, отрабатываем слияние и разделение слов
            elif cs <=0.6:
                # Если исходное слово меньше, то слияние
                if len(sw_list) < len(aw_list):
                    try:
                        cs_space = compute_similarity(sw_list[nw], aw_list[nw+offset]+aw_list[nw+offset+1])
                        # При слиянии- разделении (дополненные) слова должны соответствовать друг другу
                        if cs_space <= 1 and cs_space >=0.8:
                            errw.append((nw, 1))
                            offset += 1
                        else:
                            print(f'ERROR_SPACE: Word number: {nw}, input word: {sw_list[nw]}, output word: {aw_list[nw+offset]}, compute_similarity: {cs}')
                    except:
                        print(f'EXCEPTION_1: Word number: {nw}, input word: {sw_list[nw]}, output word: {aw_list[nw+offset]}, compute_similarity: {cs}')
                # Если исходное слово больше, то разделение
                elif len(sw_list) > len(aw_list):
                    try:
                        cs_merge = compute_similarity(sw_list[nw]+sw_list[nw+1], aw_list[nw+offset])
                        # При слиянии- разделении (дополненные) слова должны соответствовать друг другу
                        if cs_merge <= 1 and cs_merge >=0.8:
                            errw.append((nw, -1))
                            merged = -1
                            offset -= 1
                        else:
                            print (offset)
                            print(f'ERROR_MERGE: Word number: {nw}, input word: {sw_list[nw]}, output word: {aw_list[nw+offset]}, compute_similarity: {cs}')
                    except:
                        print(f'EXCEPTION_2: Word number: {nw}, input word: {sw_list[nw]}, output word: {aw_list[nw+offset]}, compute_similarity: {cs}')
                else:
                    print(f'ERROR_1: Word number: {nw}, input word: {sw_list[nw]}, output word: {aw_list[nw+offset]}, compute_similarity: {cs}')
            elif cs < 0.8 and cs >=0.6:
                print(f'ERROR_2: Word number: {nw}, input word: {sw_list[nw]}, output word: {aw_list[nw+offset]}, compute_similarity: {cs}')
        else:
            merged = 0
    s_iter = p.finditer(s)
    for idx, word in enumerate(s_iter):
        for e in errw:
             if idx == e[0]:
                 print(idx, word.group(), word.start(), word.end())
    errw = []
