#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys,os
#import math,re,datetime
import romkan
from edit_distance import edit_distance
import unicodedata

def hira_toroma(word):
    return unicodedata.normalize("NFKC",romkan.to_roma(word.decode("utf8")))

def hiragana_distance(target,source):
    roma1 = hira_toroma(target)
    roma2 = hira_toroma(source)
    return edit_distance(roma1,roma2)
    

if __name__ == "__main__":
    hiragana1 = sys.argv[1]
    hiragana2 = sys.argv[2]
    print hiragana_distance(hiragana1,hiragana2)
