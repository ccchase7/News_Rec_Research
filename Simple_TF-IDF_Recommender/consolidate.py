import pandas as pd

base_dir = "/mnt/c/Users/cchase/Documents/CS_497_R/Summarizers/new_summarizer/z_other_content"
extractor_abstractor_hybrid_dir = "extractor_abstractor_hybrid_dir"
extractor_abstractor_hybrid_suff = "_Extractor_Abstractor_Hybrid.txt"

abstractor_extractor_hybrid_dir = "abstractor_extractor_hybrid_dir"
abstractor_extractor_hybrid_suff = "_Abstractor_Extractor_Hybrid.txt"

abstractor_only_dir = "abstractor_only_dir"
abstractor_only_suff = "_Abstractor_Only.txt"

extractor_only_dir = "extractor_only_dir"
extractor_only_suff = "_Extractor_Only.txt"

print(f"Reading file...")
data_path = '/mnt/c/Users/cchase/Documents/CS_497_R/CS_497_R/scrappy/mind/MN-DS-news-classification.csv'
data = pd.read_csv(data_path)
data.columns = ["data_id", "id", "date", "source", "title", "content", "author", "url", "published", "published_utc", "collection_utc", "category_level_1", "category_level_2"]
data["article_num"] = range(len(data))

def read_contents(dir_path, file_suff, index):
    try:
        with open(f"{base_dir}/{dir_path}/{index}{file_suff}", 'r') as f:
            return f.read()
    except Exception as e:
        return ""

print(f"Reading Abstractor Summaries...")
data["abstractor_summary"] = data["article_num"].apply(lambda x: read_contents(abstractor_only_dir, abstractor_only_suff, x))
print(f"Reading Extractor Summaries...")
data["extractor_summary"] = data["article_num"].apply(lambda x: read_contents(extractor_only_dir, extractor_only_suff, x))
print(f"Reading Abstractor Extractor Summaries...")
data["abstractor_extractor_summary"] = data["article_num"].apply(lambda x: read_contents(abstractor_extractor_hybrid_dir, abstractor_extractor_hybrid_suff, x))
print(f"Reading Extractor Abstractor Summaries...")
data["extractor_abstractor_summary"] = data["article_num"].apply(lambda x: read_contents(extractor_abstractor_hybrid_dir, extractor_abstractor_hybrid_suff, x))

dest_path = "/mnt/c/Users/cchase/Documents/CS_497_R/simple_TF_IDF/other/other_master.xlsx"
print(f"Writing to {dest_path}")
data.to_excel(dest_path)