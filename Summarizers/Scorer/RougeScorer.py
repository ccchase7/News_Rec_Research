print(f"Downloading dependencies...")
from rouge_score import rouge_scorer
import pandas as pd

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
from nltk.stem.porter import *

class NewsStemmer():
    def __init__(self) -> None:
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))

    def remove_stop_words_sentence(self, sentence):
        words = sentence.split()
        return [word for word in words if word not in self.stop_words]

    def stem_and_stop_sentence(self, sentence):
        return [self.stemmer.stem(w) for w in sentence.split() if not w in self.stop_words]
    
def calculate_scores(summary_dir, orig_dir, summary_file_suffix, orig_file_suffix, num_files):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    all_scores = []
    stemmer = NewsStemmer()
    #print("calculating...")
    for i in range(num_files):
        try:
            with open(f"{summary_dir}/{i}{summary_file_suffix}", "r") as summary_file, open(f"{orig_dir}/{i}{orig_file_suffix}", "r") as original_file:
                original = original_file.read()
                original = " ".join([" ".join(stemmer.stem_and_stop_sentence(sentence)) for sentence in nltk.tokenize.sent_tokenize(original)])
                #print(original)
                summary = summary_file.read()
                summary = " ".join([" ".join(stemmer.stem_and_stop_sentence(sentence)) for sentence in nltk.tokenize.sent_tokenize(summary)])
                #print(summary)

                scores = scorer.score(original, summary)
                print(scores)
                all_scores.append(scores)
        except Exception as ex:
            print(ex)

    return all_scores
    
def scores_to_dataframes(scores):
  df = pd.DataFrame(scores)

  df['rouge1_precision'] = df.apply(lambda x: list(x['rouge1'][:1]), axis=1)
  df['rouge1_recall'] = df.apply(lambda x: list(x['rouge1'][1:2]), axis=1)
  df['rouge1_fmeasure'] = df.apply(lambda x: list(x['rouge1'][2:]), axis=1)
  df['rouge2_precision'] = df.apply(lambda x: list(x['rouge2'][:1]), axis=1)
  df['rouge2_recall'] = df.apply(lambda x: list(x['rouge2'][1:2]), axis=1)
  df['rouge2_fmeasure'] = df.apply(lambda x: list(x['rouge2'][2:]), axis=1)
  df['rougeL_precision'] = df.apply(lambda x: list(x['rougeL'][:1]), axis=1)
  df['rougeL_recall'] = df.apply(lambda x: list(x['rougeL'][1:2]), axis=1)
  df['rougeL_fmeasure'] = df.apply(lambda x: list(x['rougeL'][2:]), axis=1)

  rouge1_scores = df[["rouge1_precision", "rouge1_recall", "rouge1_fmeasure"]]
  rouge2_scores = df[["rouge2_precision", "rouge2_recall", "rouge2_fmeasure"]]
  rougeL_scores = df[["rougeL_precision", "rougeL_recall", "rougeL_fmeasure"]]

  return {"rouge1": rouge1_scores, "rouge2": rouge2_scores,"rougeL": rougeL_scores}

def calculate_all_scores():
    #base_dir = "drive/MyDrive/Ng/summary_results_Big_1"
    print(f"Defining directory paths...")
    base_dir = "/mnt/c/Users/cchase/Documents/CS_497_R/Summarizers/new_summarizer/z_other_content"

    orig_content_dir = f"{base_dir}/original_content"
    orig_content_suff = "_all_original.txt"

    ex_ab_hyb_dir = f"{base_dir}/extractor_abstractor_hybrid_dir"
    ex_ab_hyb_suff = "_Extractor_Abstractor_Hybrid.txt"

    ab_ex_hyb_dir = f"{base_dir}/abstractor_extractor_hybrid_dir"
    ab_ex_hyb_suff = "_Abstractor_Extractor_Hybrid.txt"

    ab_only_dir = f"{base_dir}/abstractor_only_dir"
    ab_only_suff = "_Abstractor_Only.txt"

    ex_only_dir = f"{base_dir}/extractor_only_dir"
    ex_only_suff = "_Extractor_Only.txt"

    num_files = 522

    print(f"Scoring Extractor-Abstractor summaries...")
    ex_ab_scores = calculate_scores(ex_ab_hyb_dir, orig_content_dir, ex_ab_hyb_suff, orig_content_suff, num_files)
    #print(ex_ab_scores)
    ex_ab_dfs = scores_to_dataframes(ex_ab_scores)

    print(f"Scoring Abstractor-Extractor summaries...")
    ab_ex_scores = calculate_scores(ab_ex_hyb_dir, orig_content_dir, ab_ex_hyb_suff, orig_content_suff, num_files)
    ab_ex_dfs = scores_to_dataframes(ab_ex_scores)
    #ab_ex_2_recall = [x["rouge2"][1] for x in ab_ex_scores]
    #sum(ab_ex_2_recall) / len(ab_ex_2_recall)
    print(f"Scoring Extractor only summaries...")
    ex_only_scores = calculate_scores(ex_only_dir, orig_content_dir, ex_only_suff, orig_content_suff, num_files)
    ex_only_dfs = scores_to_dataframes(ex_only_scores)
    print(f"Scoring Abstractor only summaries...")
    ab_only_scores = calculate_scores(ab_only_dir, orig_content_dir, ab_only_suff, orig_content_suff, num_files)
    ab_only_dfs = scores_to_dataframes(ab_only_scores)

    def scores_to_df_2(scores, rouge_type):
        c_df = pd.DataFrame(scores)
        rouge_type_df = pd.DataFrame(list(c_df[rouge_type]))
        return rouge_type_df

    def dfs_to_merged(ab_only_scores, ex_only_scores, ab_ex_scores, ex_ab_scores, rouge_type):
        ab_only_rouge1_df = scores_to_df_2(ab_only_scores, rouge_type)
        ex_only_rouge1_df = scores_to_df_2(ex_only_scores, rouge_type)
        ab_ex_rouge1_df = scores_to_df_2(ab_ex_scores, rouge_type)
        ex_ab_rouge1_df = scores_to_df_2(ex_ab_scores, rouge_type)
        ds = {}
        ds['ab_only'] = ab_only_rouge1_df
        ds['ex_only'] = ex_only_rouge1_df
        ds['ab_ex'] = ab_ex_rouge1_df
        ds['ex_ab'] = ex_ab_rouge1_df
        merged = pd.concat(ds, axis=1)
        return merged

    def to_df_and_organize(rouge_type):
        merged_rouge = dfs_to_merged(ab_only_scores, ex_only_scores, ab_ex_scores, ex_ab_scores, rouge_type)
        nms = ["summ_type", "measure_type"]
        merged_rouge.columns.names = nms

        merged_rouge = merged_rouge.describe().loc["mean"].groupby("measure_type").head()[["ex_ab", "ab_ex", "ex_only", "ab_only"]]# .to_string(index=False, header=False)
        return merged_rouge

    merged_rouge1 = to_df_and_organize("rouge1")
    merged_rouge2 = to_df_and_organize("rouge2")
    merged_rougeL = to_df_and_organize("rougeL")


    print(f"Rouge1:\n{merged_rouge1.to_string(index=True, header=False)}")
    print(f"Rouge2:\n{merged_rouge2.to_string(index=True, header=False)}")
    print(f"RougeL:\n{merged_rougeL.to_string(index=True, header=False)}")

calculate_all_scores()