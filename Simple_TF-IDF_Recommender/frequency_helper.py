import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.stem.porter import *
from collections import defaultdict
import string

class Frequency_Helper():
    def __init__(self) -> None:
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        self.all_word_freq = defaultdict(lambda: 0)

    def word_counter(self, inputs):
        word_counts = defaultdict(lambda: 0)
        max_freq = 1

        for input in inputs:
            word_counts[input] += 1
            max_freq = max(max_freq, word_counts[input])

            if word_counts[input] == 1:
                self.all_word_freq[input] += 1

        return word_counts, max_freq
        
    def get_stop_stem(self, input):
        try:
            return [self.stemmer.stem(word.lower()) for word in input.translate(str.maketrans('', '', string.punctuation)).split() if word.lower() not in self.stop_words]
        except:
            return []

    def get_freq_data(self, input):
        word_counts, max_freq = self.word_counter(input)
        return word_counts, max_freq
    