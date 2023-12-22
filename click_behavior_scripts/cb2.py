from collections import defaultdict

from utils import *
from match_titles import *

#behavior_file = "test1.txt"
#behavior_path = f"/mnt/c/Users/cchase/Documents/CS_497_R/click_behavior_scripts/{behavior_file}"
SAVE_INTERVAL = 75000
NOTIFY_INTERVAL = 25000
behavior_file = "behaviors.tsv"
behavior_path = f"/mnt/c/Users/cchase/Documents/MIND/{behavior_file}"

# {articleID_from_click_history: {related_article: number_of_occurrences}}
related = defaultdict(lambda: defaultdict(lambda: 0))
# {articleID_from_suggested: {articleID_from_click_history: number_of_occurrences}}
suggested = defaultdict(lambda: defaultdict(lambda: 0))
# {articleID_from_click_history: {related_article: number_of_times_it_was_clicked}}
clicked = defaultdict(lambda: defaultdict(lambda: 0))
# {suggested_article_that_was_clicked: {articleID_from_click_history: number_of_times_it_was_in_click_history_when_suggested_was_clicked}}
suggested_clicked = defaultdict(lambda: defaultdict(lambda: 0))

count = 0

try:
    with open(behavior_path, "r") as bvr_file:
        print(f"Processing clicks from {behavior_path}...")
        lines = (ln.strip().split('\t') for ln in bvr_file)

        titles = next(lines)

        while True:
            count += 1
            try:
                curr_line = next(lines)
            except:
                print(f"Reached end of file. Stopping...")
                break
            
            try:
                # userID = curr_line[1]
                click_history = curr_line[3].split()
                #print(f"Click history: {click_history}")
                impressions = curr_line[4].split()
                impressions_total = [impression.split("-")[0] for impression in impressions]
                impressions_clicked = [impression.split("-")[0] for impression in impressions if str(impression.split("-")[1]) == "1"]
                #print(f"Impression: {impressions}")

                for click_hist in click_history:
                    for impression in impressions_total:
                        related[click_hist][impression] += 1
                        suggested[impression][click_hist] += 1

                    for impression_clicked in impressions_clicked:
                        clicked[click_hist][impression_clicked] += 1
                        suggested_clicked[impression_clicked][click_hist] += 1

                if count % NOTIFY_INTERVAL == 0:
                    print(f"Line Count: {count}")

                #if count >= 100:
                    #break


                        
            except KeyboardInterrupt:
                print(f"Keyboard interrupt. Stopping...")
                break
            except Exception as ex:
                print(f"An Exception Occurred: {ex}. Continuing...")


        # print(f"User: {userID}, clickHistory: {clickHistory}, impression: {impression}")
except Exception as e:
    print(f"An Exception Occurred: {e}")

import pandas as pd

def to_df(info_dict):
    titles = get_id_to_title_dict()
    art_ids = [n for n in info_dict]
    art_titles = [titles[n] for n in info_dict]
    correspond = ["\t".join([f"{c}={info_dict[n][c]}" for c in info_dict[n]]) for n in info_dict]
    correspond_titles = ["\t".join([f"{titles[c]}={info_dict[n][c]}" for c in info_dict[n]]) for n in info_dict]

    df = pd.DataFrame([art_ids, art_titles, correspond, correspond_titles]).transpose()
    df.columns = ["News ID", "Article Title", "Related Article IDs", "Related Article Titles"]
    return df


#mind = pd.read_excel(f"/mnt/c/Users/cchase/Documents/MIND/news.xlsx")
#mind.columns = ["News ID", "Category", "Subcategory", "Title", "Abstract", "URL", "Title Entities", "Abstract Entities"]

def sort_dict(dct, min_val=10, max_follow_len=10):
    screened_dct = {kee: {k: v for k, v in zip(valuu.keys(), valuu.values()) if v > min_val} for kee, valuu in zip(dct.keys(), dct.values())}
    for art in screened_dct:
            ordered = sorted(screened_dct[art].items(), key=operator.itemgetter(1), reverse=True)[:max_follow_len]
            curr_dict = {k: v for k, v in ordered}
            screened_dct[art] = curr_dict
    
    return screened_dct

print(f"Sorting, screening...")
sorted_screened_clicked = sort_dict(clicked)
print(f"To Dataframe...")
clicked_df = to_df(sorted_screened_clicked)
print(f"To Excel...")
clicked_df.to_excel("/mnt/c/Users/cchase/Documents/CS_497_R/click_behavior_scripts/big_out_clicked.xlsx")

def screen_and_print(dct, name):
    print(f"Sorting, screening...")
    sorted_screened_clicked = sort_dict(dct)
    print(f"To Dataframe...")
    clicked_df = to_df(sorted_screened_clicked)
    print(f"To Excel...")
    try:
        clicked_df.to_excel(f"/mnt/c/Users/cchase/Documents/CS_497_R/click_behavior_scripts/big_out_{name}.xlsx")
    except (e):
        print(f"Exception: {e}")

screen_and_print(related)
screen_and_print(suggested)
screen_and_print(suggested_clicked)


#related_df["Title"] = related_df["News ID"].apply(lambda x: mind.loc[mind["News ID"] == x]["Title"].iloc[0])
#related_df["Related Article Titles"] = 




