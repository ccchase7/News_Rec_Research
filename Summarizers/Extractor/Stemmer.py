import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.stem.porter import *

class NewsStemmer():
    def __init__(self) -> None:
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))

    def remove_stop_words_sentence(self, sentence):
        words = sentence.split()
        return [word for word in words if word not in self.stop_words]
    
    def stem_and_stop_sentence(self, sentence):
        return [self.stemmer.stem(w) for w in sentence.split() if not w in self.stop_words]