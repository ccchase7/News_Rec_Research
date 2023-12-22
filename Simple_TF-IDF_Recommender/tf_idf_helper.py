from math import log2

class TF_IDF_Helper():
    def __init__(self, data, all_words_freq, N) -> None:
        self.all_words_freq = all_words_freq
        self.N = N
        self.df = data

    def calculate_TF_IDF_score(self, q, d):
        q = self.df.iloc[q]
        d = self.df.iloc[d]

        score = 0

        for word in q["Stop_Stem"]:
            score += self.calculate_TF(word, d) * self.calculate_IDF(word)

        return score

    def calculate_TF(self, word, d):
        return self.freq(word, d["Freq"])
    
    def calculate_IDF(self, word):
        return log2(self.N / self.all_words_freq[word])

    # How many times word appears in document d
    # word is the word in question and d_word_dict is a dictionary that contains the
    # word frequencies in document d
    def freq(self, word, d_word_dict):
        return d_word_dict[word]
    
    # The number of times that document d's most frequent word occurred in document d
    def max_freq(self, d_row):
        return d_row["Max_Freq"]
        

    

