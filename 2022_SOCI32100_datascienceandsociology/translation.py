from googletrans import Translator
from numpy import column_stack
import xlwt
import pandas as pd
import time

names = ["사회학전체", "일반2018", "일반2019", "일반2020", "일반2021"]
t = Translator()


def colTrans(name, colnum):
    try:
        df = pd.read_excel(name + "_t.xls")
    except:
        df = pd.read_excel(name + ".xls")
    try:
        with open(name + "_num.txt", "rt", encoding="UTF-8") as f:
            start = int(f.readline())
    except:
        with open(name + "_num.txt", "wt", encoding="UTF-8") as f:
            start = 0
            f.write("0")
    for i in range(start, len(df)):
        try:
            if not i % 200:
                print(f"<<{i}>>\n")
                time.sleep(1)
            if t.detect(df.iloc[i, colnum]).lang != "ko":
                # print(df.iloc[i, colnum], end="\t\t <TO> \t\t")
                df.iloc[i, colnum] = t.translate(df.iloc[i, colnum], dest="ko").text
                # print(df.iloc[i, colnum])
        except Exception as ex:
            print(f"Exception Occured : {ex}, {i}th Record")
            with open(name + "_num.txt", "wt", encoding="UTF-8") as f:
                f.write(str(i))
            break
    df.to_excel(name + "_t.xls", index=0)


for name in names[1:-1]:
    print(f"#########{name} STARTED")
    colTrans(name, 14)
