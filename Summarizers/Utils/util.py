import json
import os
from Utils.NewsItem import NewsItem
from Utils.SimpleNewsArticle import SimpleNewsArticle

def json_to_SearchResult(json_string) -> NewsItem:
  ad = json.loads(json_string)
  sd = ad["searchResult"]
  return json.loads(json_string, object_hook=lambda d: NewsItem(ad["webpage_title"], ad["contents"], **sd))

def news_items_from_json(input_file_path):
  try:
    with open(input_file_path, "r") as inFile:
      news_item_json = inFile.read().splitlines()
      
      news_items = []

      for json_line in news_item_json:
        news_items.append(json_to_SearchResult(json_line))

    return news_items
  except:
    return SimpleNewsArticle("", "", "")

def news_item_to_simpleNewsArticle(newsItem):
  return SimpleNewsArticle(newsItem.title, newsItem.contents, newsItem.index_number)

def check_dir_exists_or_create(dir_name):
  if not os.path.isdir(dir_name):
    print(f"Creating directory {dir_name}...")
    os.makedirs(dir_name)

  return True
