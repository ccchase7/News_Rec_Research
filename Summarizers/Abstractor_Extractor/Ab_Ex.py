from Extractor.Extractor import Extractor
from Abstractor.Abstractor import Abstractor

class Hybrid_Abstractor_Extractor():
    def __init__(self, news_article_content) -> None:
        self.news_article_content = news_article_content

        self.summary = self.create_summary()

    def create_summary(self):
        abstractor = Abstractor(self.news_article_content)
        extractor = Extractor(" ".join(abstractor.summary), size_limit_type="word_count")

        return extractor.summary

    def print_summary(self):
        for ln in self.summary:
          print(ln)