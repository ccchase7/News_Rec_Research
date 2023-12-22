print(f"Importing Modules...")

from Utils.util import *
from Abstractor.Abstractor import Abstractor
from Extractor.Extractor import Extractor
from Extractor_Abstractor.Ex_Ab import Hybrid_Extractor_Abstractor
from Abstractor_Extractor.Ab_Ex import Hybrid_Abstractor_Extractor

import time

print(f"Initializing Summary context...")

base_dir = "/mnt/c/Users/cchase/Documents/CS_497_R/Summarizers/new_summarizer/"
#json_file_path = f"{base_dir}/newsItemJson_Big.txt"
json_file_path = f"{base_dir}/newsItemJson_Big.txt"

#results_dir = "summary_results_Big_1"
results_dir = "z_other_content"
base_dir = f"{base_dir}/{results_dir}"

check_dir_exists_or_create(f"{base_dir}")

time_file_path = f"{base_dir}/durations.txt"
info_file_path = f"{base_dir}/info.txt"
orig_contents_dir = f"original_content"

check_dir_exists_or_create(f"{base_dir}/{orig_contents_dir}")

#simple_news_articles = [news_item_to_simpleNewsArticle(news_item).article_contents for news_item in news_items_from_json(json_file_path)]

#################################################################################################
import pandas as pd

from Utils.SimpleNewsArticle import *

df = pd.read_csv("/mnt/c/Users/cchase/Documents/CS_497_R/CS_497_R/scrappy/mind/MN-DS-news-classification.csv")

titles = list(df["title"])
content = list(df["content"])
ids = list(df["data_id"])

simple_news_articles = []

for i in range(len(titles)):
    simple_news_articles.append(SimpleNewsArticle(titles[i], content[i], ids[i]).article_contents)
#################################################################################################

simple_news_articles = [news_item for news_item in simple_news_articles if len(news_item) > 0]
#simple_news_articles = simple_news_articles[:2]

summary_classes = {
                    "Extractor_Abstractor_Hybrid": Hybrid_Extractor_Abstractor,
                    "Abstractor_Extractor_Hybrid": Hybrid_Abstractor_Extractor,
                    "Abstractor_Only": Abstractor,
                    "Extractor_Only": Extractor
                    }

summarizer_names = summary_classes.keys()

destination_directories = {name: f"{name.lower()}_dir" for name in summarizer_names if check_dir_exists_or_create(f"{base_dir}/{name.lower()}_dir")}
durations = {f"{name}_time": [] for name in summarizer_names}

def run_summarizer(article_contents, summarizer_class, duration_list):
    
    print(f"Running {summarizer_class}")
    startTime = time.process_time()
    summarizer = summarizer_class(article_contents)
    endTime = time.process_time()
    duration_list.append(endTime - startTime)
    print(f"avg time: {sum(duration_list) / len(duration_list)}")

    return summarizer
print(f"Running summary loop...")
try:
   for i in range(len(simple_news_articles)):
      print(f"processing article {i}")
      article = simple_news_articles[i]
      try:
         summarizer_instances = {}

         for summarizer_name in summarizer_names:
            summarizer = run_summarizer(article, summary_classes[summarizer_name], durations[f"{summarizer_name}_time"])
            summarizer_instances[summarizer_name] = summarizer

      except Exception as exc:
         print(f"Failed on article {i}: {exc}")
         continue

      print(f"Writing Summaries...")
      try:
         # Write the original article contents to a file
         with open(base_dir + "/" + orig_contents_dir +  f"/{i}_all_original" + ".txt", "w") as orig_content_outfile:
                  orig_content_outfile.write(" ".join(article.split("\n")))

         # Write each summary to a file
         for summarizer_name in summarizer_names:
            with open(base_dir + "/" + destination_directories[summarizer_name] +  f"/{i}_" + summarizer_name + ".txt", "w") as summary_outfile:
                  summary_outfile.write(" ".join(summarizer_instances[summarizer_name].summary))

      except Exception as Ex:
         print(f"Failed to write summary on article {i}: {Ex}")
except KeyboardInterrupt:
   print(f"Interrupt received.")
finally:
   print(f"Writing info to files...")
   # Write duration information
   try:
      print(f"Writing time info...")
      with open(time_file_path, "w") as time_outfile:

         for summarizer_name in summarizer_names:
            time_outfile.write(f"{summarizer_name}\n")
            duration_list = durations[f"{summarizer_name}_time"]
            time_outfile.write(f"Avg Duration: {sum(duration_list)/len(duration_list)}\n\n")
            time_outfile.write(str(duration_list) + "\n")
   except Exception as ex:
       print(f"Could not write time info: {ex}")

   # Write path information
   try:
      print(f"Writing file info...")
      with open(info_file_path, "w") as info_outfile:
         # Specify base directory path
         info_outfile.write("base_dir = " + '"' + base_dir + '"\n')

         # Specify original content directory
         info_outfile.write("orig_content_dir = " + orig_contents_dir + "\n")

         for summarizer_name in summarizer_names:
            # Specify directory paths for the summaries from each respective summarizer type
            info_outfile.write(summarizer_name.lower() + "_dir = " + '"' + destination_directories[summarizer_name] + '"\n')
            # Specify suffixes for summary files
            info_outfile.write(summarizer_name.lower() + "_suff = \"_" + summarizer_name + ".txt\"\n")
   except Exception as ex:
       print(f"Could not write file info: {ex}")
      
