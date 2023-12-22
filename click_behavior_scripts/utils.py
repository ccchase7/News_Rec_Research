import operator
import json
import os

out_base_dir = "out_formatted_tst"

def check_dir_exists_or_create(dir_name):
  if not os.path.isdir(dir_name):
    print(f"Creating directory {dir_name}...")
    os.makedirs(dir_name)

  return True

def print_relations(related, suggested, clicked, suggested_clicked):
    print(f"****************************************\nSuggested Articles:\n")
    # How many times suggested_article was suggested when click_hist_article was in the user's history
    for click_hist_article in related:
        print(f"Hist Article {click_hist_article}:")
        curr_dict = sorted(related[click_hist_article].items(), key=operator.itemgetter(1), reverse=True)
        for suggested_article, num in curr_dict:
            print(f"\t{suggested_article}: {num}")

    print(f"How many times hist_article was in user's history when suggested_article was suggested")

    print(f"****************************************\nSuggested Articles:\n")
    # How many times hist_article was in user's history when suggested_article was suggested
    for suggested_article in suggested:
        print(f"Suggested Article {suggested_article}:")
        curr_dict = sorted(suggested[suggested_article].items(), key=operator.itemgetter(1), reverse=True)
        for hist_article, num in curr_dict:
            print(f"\t{hist_article}: {num}")

    print(f"How many times 'clicked_article' was clicked when 'click_hist_article' was in user's history")

    print(f"****************************************\nClicked:\n")
    # How many times "clicked_article" was clicked when "click_hist_article" was in user's history
    for click_hist_article in clicked:
        print(f"Hist Article {click_hist_article}:")
        curr_dict = sorted(clicked[click_hist_article].items(), key=operator.itemgetter(1), reverse=True)
        for clicked_article, num in curr_dict:
            print(f"\t{clicked_article}: {num}")

    print(f'How many times "click_hist_article" was in history when "clicked_article" was clicked')
    
    print(f"****************************************\nSuggested Clicked:\n")
    # How many times "click_hist_article" was in history when "clicked_article" was clicked
    for suggested_clicked_article in suggested_clicked:
        print(f"Suggested Clicked Article {suggested_clicked_article}:")
        curr_dict = sorted(suggested_clicked[suggested_clicked_article].items(), key=operator.itemgetter(1), reverse=True)
        for click_hist_article, num in curr_dict:
            print(f"\t{click_hist_article}: {num}")

def write_r_to_file(r, label, file_no):
    label = "_".join(label.split())

    dir_name = f"{out_base_dir}/{file_no}"
    check_dir_exists_or_create(dir_name)

    with open(f"{dir_name}/{label}.txt", "w") as out_file:
        for row in r:
            json.dump(row, out_file)
            out_file.write('\n')

def write_r_to_json(related, suggested, clicked, suggested_clicked, file_no):
    related_r_label = f"How many times suggested_article was suggested when click_hist_article was in the user's history"
    related_r = [(click_hist_article, sorted(related[click_hist_article].items(), key=operator.itemgetter(1), reverse=True)) for click_hist_article in related]
    
    write_r_to_file(related_r, related_r_label, file_no)

    suggested_r_label = f"How many times hist_article was in user's history when suggested_article was suggested"
    suggested_r = [(suggested_article, sorted(suggested[suggested_article].items(), key=operator.itemgetter(1), reverse=True)) for suggested_article in suggested]

    write_r_to_file(suggested_r, suggested_r_label, file_no)

    clicked_r_label = f"How many times 'clicked_article' was clicked when 'click_hist_article' was in user's history"
    clicked_r = [(click_hist_article, sorted(clicked[click_hist_article].items(), key=operator.itemgetter(1), reverse=True)) for click_hist_article in clicked]

    write_r_to_file(clicked_r, clicked_r_label, file_no)

    suggested_clicked_r_label = f'How many times "click_hist_article" was in history when "clicked_article" was clicked'
    suggested_clicked_r = [(suggested_clicked_article, sorted(suggested_clicked[suggested_clicked_article].items(), key=operator.itemgetter(1), reverse=True)) for suggested_clicked_article in suggested_clicked]

    write_r_to_file(suggested_clicked_r, suggested_clicked_r_label, file_no)
