from frequency_helper import Frequency_Helper
from tf_idf_helper import TF_IDF_Helper
from heapq import *

class TF_IDF_Recommender():
    def __init__(self, data, feature) -> None:
        self.feature = feature
        frequency_helper = Frequency_Helper()

        self.data = data
        self.data["Stop_Stem"] = data[self.feature].apply(frequency_helper.get_stop_stem)
        self.data["Freq"] =  data["Stop_Stem"].apply(frequency_helper.get_freq_data)
        self.data["Max_Freq"] = data["Freq"].apply(lambda x: x[1])
        self.data["Freq"] = data["Freq"].apply(lambda x: x[0])

        self.N = len(self.data.index)

        self.tf_idf_helper = TF_IDF_Helper(self.data, frequency_helper.all_word_freq, self.N)
        self.num_recommendations = 10

    def score_one(self, index_1, index_2):
        if index_1 < 0 or index_2 < 0:
            raise ValueError("Tried to score negative index.")
        if index_1 >= self.N or index_2 >= self.N:
            raise ValueError(f"Tried to score index out of bounds. Max index: {self.N - 1}")
        try:
            return self.tf_idf_helper.calculate_TF_IDF_score(index_1, index_2)
        except:
            return 0.000001
    
    def get_top_matches_index(self, index):
        matches = [(0, 0)]

        for i in range(self.N):
            if i != index:
                curr_score = self.score_one(index, i)

                if curr_score > matches[0][0]:
                    if len(matches) >= self.num_recommendations:
                        heappop(matches)
                    heappush(matches, (curr_score, i))
        return [match[1] for match in matches]

    def get_top_matches(self, index):
        top_matches_indices = self.get_top_matches_index(index)

        return self.matches_to_string(index, top_matches_indices)
    
    def matches_to_string(self, query_index, match_indexes):
        print_feature = "title"
        ans = self.data[print_feature].iloc[query_index]
        ans += ":\n\n"
        for match_index in match_indexes:
            ans += "\t" + self.data[print_feature].iloc[match_index]
            ans += "\n"

        return ans

    def fill_all_recommendations(self, cols_to_compare):
        for col in cols_to_compare:
            self.data[f"{col}_recommendations"] = self.data[col].apply()



        
        
