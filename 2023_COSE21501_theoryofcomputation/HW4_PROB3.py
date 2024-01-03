#! python

import re
import nltk

FILES = [
    "2014-0160",
    "2018-20250",
    "2019-0752",
    "2020-0688",
    "2021-21972",
    "2021-26263",
    "2021-26947",
    "2021-44228",
    "2022-48476",
    "2023-22577",
]
descs = []
for filenum in FILES:
    with open(f"CVE-{filenum}.html", "rt", encoding="utf-8") as f:
        t = f.read()
        descs.append(
            re.search(
                '<p data-testid="vuln-description">(.*?)</p>', t, re.DOTALL
            ).group(1)
        )

try:
    words = nltk.tokenize.word_tokenize("\n".join(descs))
except LookupError:
    nltk.download("punkt")
    words = nltk.tokenize.word_tokenize("\n".join(descs))

try:
    tags = nltk.pos_tag(words)
except LookupError:
    nltk.download("averaged_perceptron_tagger")
    tags = nltk.pos_tag(words)

freq_noun = {}
freq_verb = {}
for word, tag in tags:
    if tag in ("NN", "NNS", "NNP", "NNPS"):
        freq_noun.setdefault(word, 0)
        freq_noun[word] += 1
    elif tag in ("VB", "VBD", "VBG", "VBN", "VBP", "VBZ"):
        freq_verb.setdefault(word, 0)
        freq_verb[word] += 1

freq_dict = dict(freq_noun, **freq_verb)
freq_list = sorted(freq_dict.items(), key=lambda x: -x[1])
print(
    """# Result over 10 html files
# "words" -  frequency"""
)
for i, (word, freq) in enumerate(freq_list, 1):
    print(f'{i}. "{word}" -  {freq}')
    if i == 10:
        break
