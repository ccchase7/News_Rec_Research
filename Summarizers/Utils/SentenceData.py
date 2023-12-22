import string
from Extractor.Stemmer import NewsStemmer
from collections import defaultdict

class SentenceData():
    def __init__(self, sen, revNum=1) -> None:
        # Original Contents
        self.og_sen = sen
        if self.og_sen[-1] not in string.punctuation:
            self.og_sen = self.og_sen + "."
        # Specify number of words in original sentence
        self.og_numWords = len(self.og_sen.split())

        # Remove stop words and stem each remaining word
        stemmer = NewsStemmer()
        self.filt_sen = self.og_sen.translate(str.maketrans('', '', string.punctuation)) # Removes punctuation
        self.filt_sen = stemmer.stem_and_stop_sentence(self.filt_sen) # Removes stop words and stems each word
        # Specify number of words after stemming
        self.filt_num_words = len(self.filt_sen)

        # Create dictionary of word frequency
        self.dictionary = defaultdict(lambda: 0)
        for word in self.filt_sen:
            self.dictionary[word] += 1

        self.inSummary = False
        self.revNum = revNum
        
    def AddToSummary(self):
        self.inSummary = True
