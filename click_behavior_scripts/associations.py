import pandas as pd
import numpy as np

df = pd.read_excel("/mnt/c/Users/cchase/Documents/CS_497_R/click_behavior_scripts/have_master.xlsx")

have_ids_list = list(df["News ID"])

df["Has_Articles"] = df["Related Article IDs"].apply(lambda x: [y.split('=')[0] for y in  str(x).split('\t') if y.split('=')[0] in have_ids_list])

have_matches = df.loc[df["Has_Articles"].apply(lambda x: len(x) > 0 and np.NaN not in x)]

have_matches.to_excel("/mnt/c/Users/cchase/Documents/CS_497_R/click_behavior_scripts/with_matches.xlsx")

