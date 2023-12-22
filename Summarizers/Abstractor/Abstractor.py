from Abstractor.bart_utils import *
import nltk
nltk.download('punkt')

class Abstractor():
    def __init__(self, news_article_content) -> None:
        self.news_article_content = news_article_content

        self.numBeams = 10

        self.summary = self.create_summary()

    def create_summary(self):
        return nltk.tokenize.sent_tokenize(run_bart_beam(self.news_article_content, self.numBeams))