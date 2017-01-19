#!/usr/bin/env python
from collections import defaultdict
from random import choice
class markov(object):
    
    def __init__(self,  blocklen=2, chain=defaultdict(list)):
        self.blocklen = blocklen
        self.chain = chain
    
    # The magic - creating the chain
    def update(self, text):
        x = text.split(" ")
        #append first blocklen words to beginning
        self.chain[""].append(x[:self.blocklen]) 
        
        for key, val in enumerate(x):
            if key < self.blocklen: continue
            new_key = tuple(x[key - self.blocklen:key])
            self.chain[new_key].append(val)
    
    # Wrapper - update chain with full file input
    def updatefile(self, filename):
        with open(filename) as f:
            self.update(f.read())
    
    # Wrapper - update chain with line by line file input
    def updatefilebyline(self, filename):
        with open(filename) as f:
            for line in f:
                self.update(line)
    
    #for debugging purposes only
    def printchain(self):
        for k in self.chain:
           print  k, self.chain[k]
        print len(self.chain)
        
    # The other magic - actually creating text
    def generate(self, start="", length=100):
        try:
            x = []
            y = choice( self.chain[start] )
            yield " ".join(y)
            x += y
            while length:
                x = x[-self.blocklen:]
                start = tuple(x)
                y = choice( self.chain[start] )
                yield y
                x += [y]
                length -= 1
        except IndexError, StopIteration: pass
        finally: return


if __name__ == "__main__":
    y = markov()
    y.updatefilebyline("blerr.txt")
    #y.printchain()
    
    for i in range(4):
        mytext = y.generate()
        print " ".join(mytext),