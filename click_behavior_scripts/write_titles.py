import json

from utils import *

base_dir = "/mnt/c/Users/cchase/Documents/CS_497_R/click_behavior_scripts"

in_file =  "How_many_times_'clicked_article'_was_clicked_when_'click_hist_article'_was_in_user's_history.txt"
in_file_dir = "out_formatted"
size = "75000"
in_file_path = f"/mnt/c/Users/cchase/Documents/CS_497_R/click_behavior_scripts/{in_file_dir}/{size}/{in_file}"

titles_out_file = "titles_out.txt"
out_file_path = f"{base_dir}/titles_out"

check_dir_exists_or_create(out_file_path)

out_file_path = f"{out_file_path}/{titles_out_file}"

art_list = []

from match_titles import *
id_to_title = get_id_to_title_dict()

with open(in_file_path) as f:
    for ln in f:
        d = json.loads(ln)
        art_list.append(d)

for art in art_list[:10]:
    initial_art = id_to_title[art[0]]
    related_art = art[1]
    print(f"{initial_art}")

    with open(out_file_path, "a") as o_f:
                o_f.write(f"{initial_art}")

    for related in related_art:
        if related[1] > 5:
            print(f"\t{related[1]} -- {id_to_title[related[0]]}")

            with open(out_file_path, "a") as o_f:
                o_f.write(f"\t{related[1]} -- {id_to_title[related[0]]}")

    print(30 * "*")

