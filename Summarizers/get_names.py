print(f"Importing Modules...")

from Utils.util import *

print(f"Initializing get names context...")

base_dir = "/mnt/c/Users/cchase/Documents/CS_497_R/Summarizers/new_summarizer/"
json_file_path = f"{base_dir}/newsItemJson_Big.txt"

import pandas as pd

from Utils.SimpleNewsArticle import *

simple_news_articles = [news_item_to_simpleNewsArticle(news_item) for news_item in news_items_from_json(json_file_path)]
simple_news_articles = [news_item for news_item in simple_news_articles if len(news_item.article_contents) > 0]