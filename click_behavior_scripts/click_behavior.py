from collections import defaultdict

from utils import *

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

                if count % SAVE_INTERVAL == 0:
                    write_r_to_json(related, suggested, clicked, suggested_clicked, str(count))
                    break
                if count % NOTIFY_INTERVAL == 0:
                    print(f"Line Count: {count}")


                        
            except KeyboardInterrupt:
                print(f"Keyboard interrupt. Stopping...")
                break
            except Exception as ex:
                print(f"An Exception Occurred: {ex}. Continuing...")


        # print(f"User: {userID}, clickHistory: {clickHistory}, impression: {impression}")
except Exception as e:
    print(f"An Exception Occurred: {e}")

write_r_to_json(related, suggested, clicked, suggested_clicked, "1")

"""
print(f"How many times suggested_article was suggested when click_hist_article was in the user's history")
related_r = [(click_hist_article, sorted(related[click_hist_article].items(), key=operator.itemgetter(1), reverse=True)) for click_hist_article in related]

print(f"How many times hist_article was in user's history when suggested_article was suggested")
suggested_r = [(suggested_article, sorted(suggested[suggested_article].items(), key=operator.itemgetter(1), reverse=True)) for suggested_article in suggested]

print(f"How many times 'clicked_article' was clicked when 'click_hist_article' was in user's history")
clicked_r = [(click_hist_article, sorted(clicked[click_hist_article].items(), key=operator.itemgetter(1), reverse=True)) for click_hist_article in clicked]

print(f'How many times "click_hist_article" was in history when "clicked_article" was clicked')
suggested_clicked_r = [(suggested_clicked_article, sorted(suggested_clicked[suggested_clicked_article].items(), key=operator.itemgetter(1), reverse=True)) for suggested_clicked_article in suggested_clicked]
"""
