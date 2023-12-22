from Extractor.Extractor import Extractor
from Abstractor.Abstractor import Abstractor

class Hybrid_Extractor_Abstractor():
    def __init__(self, news_article_content) -> None:
        self.news_article_content = news_article_content

        self.summary = self.create_summary()

    def create_summary(self):
        extractor = Extractor(self.news_article_content, size_limit_type="word_count")
        abstractor = Abstractor(" ".join(extractor.summary))
        return abstractor.summary

    def print_summary(self):
        for ln in self.summary:
          print(ln)