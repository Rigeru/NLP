#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import *
from collections import Counter
import gzip
import math

dict1 = Counter()
dict2 = Counter()
dict3 = Counter()
VOCB_SIZE = 632237

def mkngram( dictn, sentence, n):
    for i in range(len(sentence) - n + 1 ):
        dictn[tuple(sentence[i:i+n])] += 1

def calcprob( sentence ):
    p = 0
    for i in range(len(sentence) - 2):
        tmp = math.log((dict3[tuple(sentence[i:i+3])] + 1) / ( dict2[tuple(sentence[i:i+2])] + VOCB_SIZE + 1 ))
#        print([tuple(sentence[i:i+3])[j].decode('utf-8') for j in range(3)])
#        print ("tmp" ,tmp,dict3[tuple(sentence[i:i+3])], dict2[tuple(sentence[i:i+2])], len(dict1))
        p += tmp
    print (p)
    return p

if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: # python %s \"SOURCE_FILE_SIZE\" \"TARGET_FILE_SIZE\" " % argv[0], file=stderr)
        quit()
    sentence = [b"<s>"]*2
    learning_file = "/home/ynaga/ngrams/data/2012-01-01.cdr." + str(argv[1]) + ".gz"
    for line in gzip.open(learning_file,'rb'):
        word = line.split()[0]
        if word == b"EOS":
            sentence.append(b"</s>")
            if len(sentence) > 2:
                mkngram( dict1, sentence[2:], 1 )
                mkngram( dict2, sentence, 2 )
                mkngram( dict3, sentence, 3 )
            sentence = [b"<s>"]*2
        else:
            sentence.append(word)
    prob = 0
    sentence = [b"<s>"]*2
    linenum = 0
    target_file =  "/home/ynaga/ngrams/data/2013-01-02.cdr." + str(argv[2]) + ".gz"
    for line in gzip.open(target_file,'rb'):
        linenum += 1
        word = line.split()[0]
        if word == b"EOS":
            sentence.append(b"</s>")
            if len(sentence) > 2:
                prob += calcprob( sentence )
            sentence = [b"<s>"]*2
        else:
            sentence.append(word)
    print ("log of Probability : " ,prob)
    pp = math.exp( -1 * prob /linenum )
    print ("Perplexity : ",pp)
#    for k, v in sorted(dict1.items()):
#        print (v, k[0])
#    print(dict2)
#    for k, v in sorted(dict2.items()):
#        print ( v, k[0], k[1] )
#    for k, v in sorted(dict3.items()):
#       print ("%d\t%s %s %s" %( v, k[0].decode('utf-8','surrogateescape'), k[1].decode('utf-8','replace'), k[2].decode('utf-8','replace')))
