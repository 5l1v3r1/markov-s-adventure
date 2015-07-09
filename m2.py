#!/usr/bin/env python
import random
import re

class Markov(object):
    def __init__(self, story_file, order=2, letters = 0):
        self.story_file = story_file
        self.order = order
        self.letters = letters
        self.words = self.generateWords()
        self.model = self.createModel()
        
        
    def generateWords(self):
        with open(self.story_file) as story:
            data = story.read()
            #if letters = 1, split into letters, else, split to words.
            if (self.letters): words = list(data)
            else: words = data.split()
        return words
        
    def triples(self, size=2):
        if len(self.words) < size+1: return
        for i in range(len(self.words)-size):
            x = []
            for off in range(size+1):
                x.append(self.words[i+off])
            yield tuple(x)
            
    def createModel(self):
        model = {}
        for x in self.triples(self.order):
            key = x[:-1]
            if key in model: model[key].append(x[-1]) #append word to list
            else: model[key] = [x[-1]] #brackets ensure its initialized as a list
        return model
        
    def createStory(self, size=20):
        seed = random.randint(0, len(self.words)-(self.order+2))
        
        currentkey = []
        for off in range(self.order):
            currentkey.append(self.words[seed+off])#seed words
        generatedtext = []
        for i in range(size+1):
            generatedtext.append(currentkey[0])
            currentkey.append(random.choice(self.model[tuple(currentkey)]))
            currentkey = currentkey[1:]
        delim = '' if self.letters else ' '
        return delim.join(generatedtext+currentkey)


testing = Markov('text/sherlock.txt', 3, 0)
#print testing.model.items()[1:10]

# Create A Paragraph.
rt= testing.createStory(200)    # Generate text (rt = rawtxt)
sl = re.split('([.?!])', rt);   # Split on punctuation (sl = sentencelist)
paragraph = ''.join(sl[2:-1])   # ['fragment', '.', ..., 'fragment'] --> [...]

print paragraph