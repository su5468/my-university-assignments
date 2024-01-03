#! python
import re

T = """ABstartBBB roAA4AAB leAB3BA2A 2'B2AfindA3BA ABABB iABBAB k AABBB tBA://ABB
ps://wBABBA BA.noBBA .noBtAeABB ioABBAB .so/cAAABA s-AAAAB inaBAAAB y/AABBB
BABBA -4-6AABAB 0AAA.AA 449A-ABAA 2836487AA.BAA 89297AAfindAAB AAlinkABB
AAreallyABA 5f67AAAAB 014
 ABBBB BAA.AB obAB-ABB em3'BAaaaABA ABABB iABBAB k AAhBBB BAttpABB BAA-BB
ABBBB s://BA5B1BA BA-BBA BA22BBA .ABB-AB ABBBA BAABB ABAAA ABBBA
ABBAB .sABBBA /cAAABA s-AAgoodAAB inAA-AAA B-AAAB y/AA-BBB BABBA -4-AAABB
354496AABAA AAAAB AAAAB 4AA3BAB 49AAABA 4AA-AAA AAfightingAAA AAyouABA
AAcanAAA 53AAtheoryAofAcomputationB AABdoAB 2e2AAitABB AA.ABB e07"""


def code_to_text(text):
    """
    map table into string
    """
    if re.match(r".*?[AB]{5}.*?", text):
        prefix, text_AB, postfix = re.match(r"(.*?)([AB]{5})(.*?)", text).groups()
        text_01 = text_AB.translate(str.maketrans("AB", "01"))
        return prefix + chr(97 + int("0b" + text_01, 2)) + postfix
    return text


def clean_text(text):
    """
    clean lowercase letters inside code
    """
    ans = []
    for word in text.split():
        while 1:
            new_word = re.sub("(^.*?[AB]+?)([^AB]+?)([AB]+?.*?$)", r"\1\3", word)
            if word == new_word:
                ans.append(new_word)
                break
            word = new_word
    return ans


print("".join(map(code_to_text, clean_text(T))))
