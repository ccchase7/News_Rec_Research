
class NewsItem():
  def __init__(self, webpage_title, contents, title, query_url, index_number, result_title, date, article_url) -> None:
    self.webpage_title = webpage_title
    self.title = title
    self.query_url = query_url
    self.index_number = index_number
    self.result_title = result_title
    self.date = date
    self.article_url = article_url
    self.contents = contents