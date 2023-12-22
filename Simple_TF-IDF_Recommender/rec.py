print(f"Resolving imports...")
import pandas as pd
from tf_idf_recommender import TF_IDF_Recommender

def cls():
    import os
    os.system('clear')

print(f"Reading file...")
data_path = '/mnt/c/Users/cchase/Documents/CS_497_R/simple_TF_IDF/other/other_master.xlsx'
data = pd.read_excel(data_path)
data.columns = ["index", "data_id", "id", "date", "source", "title", "content", "author", "url", "published", "published_utc", "collection_utc", "category_level_1", "category_level_2", "article_num", "abstractor_summary", "extractor_summary", "abstractor_extractor_summary", "extractor_abstractor_summary"]


print(f"Initializing Recommender...")
#rec = TF_IDF_Recommender(data, "extractor_abstractor_summary")
rec = TF_IDF_Recommender(data, "title")

input_types = ["title", "content", "abstractor_summary", "extractor_summary", "abstractor_extractor_summary", "extractor_abstractor_summary"]

recs = {i_t: TF_IDF_Recommender(data, i_t) for i_t in input_types}


def recommend(query_index, i_t=input_types[0]):
    i_t_rec = recs[i_t]
    print(f"Finding recommendations for {data.iloc[query_index]['title']} ({query_index}) based on {i_t} ...")
    print(i_t_rec.get_top_matches(query_index))

def recommend_all(query_index):
    for c_i_t in input_types:
        recommend(query_index, i_t=c_i_t)
        print(f"*" * 30)


recommend(15)


