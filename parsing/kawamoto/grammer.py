import csv
from sets import Set
from collections import defaultdict
class lang:
    def __init__(self,rule_file):
        #input grammer and lexicon
	"""
        f = open(lexicon_file,'rb')
        reader = csv.reader(f)
        self.lexicon={ x[0]:x[1:] for x in reader}
        self.terminal = self.lexicon.keys()
        self.non_terminal=Set()
        f = open(grammer_file,'rb')
        reader = csv.reader(f)
        self.cfgs = []
        for i in reader:
            self.cfgs.append((i[0], tuple(i[1:])))
            for sig in i:
                if self.is_terminal(sig) != True:
                    self.non_terminal.add(sig)
        self.non_terminal=list(self.non_terminal)
        """
        f = open(rule_file,'rb')
        reader = csv.reader(f,delimiter=' ')
        self.lexicon=defaultdict(list)
        self.cfgs = []
        for row in reader:
            if row[1][0] == '_':
                self.lexicon[row[0]].append(row[1][1:])
            else:
                self.cfgs.append((row[0],tuple(row[1:])))
        self.terminal = self.lexicon.keys()
        self.non_terminal=Set()
        for i in self.cfgs:
             self.non_terminal.add(i[0])
             for j in i[1]:
                 self.non_terminal.add(j)
        self.non_terminal=list(self.non_terminal)
    def make_cnfs(self):
        self.cnfs_lexicon = self.lexicon
        self.cnfs = []
        self.temp_gram = []
        for cfg in self.cfgs:
            self.cnfs.extend(self.cfg2cnf(cfg))
        self.cnfs.extend(self.temp_gram)
    def is_terminal(self, sig):
        return self.lexicon.has_key(sig)
    def cfg2cnf(self,cfg):
        cnfs = []
        if (len(cfg[1]) == 3):
            if( self.search_gram(cfg[1][0],cfg[1][1],self.temp_gram) ==[] ):
                self.non_terminal.append(len(self.non_terminal))
                self.temp_gram.append( (cfg[0],(len(self.non_terminal),cfg[1][2])) )
                self.temp_gram.append( (len(self.non_terminal),(cfg[1][0],cfg[1][1])) )
            else:
                cnfs.append((cfg[0],(self.search_gram(cfg[1][0],cfg[1][1],self.temp_gram)[0],cfg[1][2])))
        elif(len(cfg[1]) == 2):
            cnfs.append(cfg)
        elif(len(cfg[1]) == 1):
            if self.is_terminal(cfg[1][0]):
                if self.cnfs_lexicon.has_key(cfg[0]):
                    self.cnfs_lexicon[cfg[0]].extend(self.cnfs_lexicon[cfg[1][0]])
                else:
                    self.cnfs_lexicon[cfg[0]]=self.cnfs_lexicon[cfg[1][0]]
            for i in self.cfgs:
                if cfg[1][0]==i[0]:
                    cnfs.extend( self.cfg2cnf((cfg[0],i[1]) ))
        else:
            self.non_terminal.append(len(self.non_terminal))
            cnfs.append( (cfg[0],(len(self.non_terminal),cfg[1][len(cfg[1])-1])) )
            cnfs.extend( self.cfg2cnf(cfg[1][:-1]) )
        return cnfs
    def taglist(self,word):
        taglist = []
        for x,y in self.lexicon.items():
            if y.count(word) > 0:
                taglist.append(x)
        return tuple(taglist)
    def search_gram(self,tagA,tagB, cnfs=None):
        taglist = []
        if cnfs==None:
            cnfs = self.cnfs
        for x,y in cnfs:
            if y==(tagA,tagB):
                taglist.append(x)
        return taglist


if __name__ == '__main__':
    L = lang('./data/rules.txt')
    L.make_cnfs()
    for x in L.cnfs:
        print x[0],x[1]
    for x in L.cnfs_lexicon.items():
	print x
