from Utils.SentenceData import SentenceData
from Extractor.kl_tf_idf import *

from collections import defaultdict
import numpy as np
import nltk
import math
nltk.download('punkt')

class Extractor(): #gets reviews, parses by sentence, gets KL scores, builds summary. Has 3 levels of affecting redundancy
  def __init__(self, news_article_content, size_limit_type="word_count", redundancy_level=0,):
    self.min_sentence_len = 5
    self.max_sentence_len = 29
    
    # Original content of the news article (list of sentences)
    self.news_article_content = [sentence for sentence in nltk.tokenize.sent_tokenize(news_article_content)]#  if len(sentence.split()) >= self.min_sentence_len and len(sentence.split()) <= self.max_sentence_len]
    self.original_num_words = len(" ".join(self.news_article_content).split())
    # Stemmed sentence data
    self.filtered_sentences = [SentenceData(sentence) for sentence in self.news_article_content]
    self.filtered_num_words = sum([len([curr_sent.filt_sen for curr_sent in self.filtered_sentences])])

    # Dictionary of all words
    self.full_dict = defaultdict(lambda: 0)
    self.sentences_with_word_dict = defaultdict(lambda: 0)
    for sentence in self.filtered_sentences:
      for word in sentence.dictionary:
        self.full_dict[word] += sentence.dictionary[word]
        self.sentences_with_word_dict[word] += 1

    # List of TF-IDF scores corresponding to filtered_sentences
    self.num_sentences = len(self.news_article_content)
    self.TF_IDF_list = self.calculate_TF_IDF()
    
    # Type of size limit for the summary (word_count, percent)
    self.size_limit_type = size_limit_type.lower()
    self.percentage_const = 0.1
    self.word_count_const = 250
    # Define size
    if self.size_limit_type == "word_count" :
      self.summary_word_limit = self.word_count_const
    elif self.size_limit_type == "percent":
      self.summary_word_limit = self.original_num_words * self.percentage_const
    else:
      raise ValueError("size_limit type must be one of the following: word_count, percent")
    
    self.summary = []
    self.summary_word_num = 0
    self.BuildSummary_TF_IDF()
    
    
  def calculate_TF_IDF(self) :
    return [KL_TF_IDF(len(self.news_article_content), sen, self.filtered_sentences) for sen in self.filtered_sentences]


  def BuildSummary_TF_IDF(self):
    if self.size_limit_type == "percent" :
      measure = "sentences"
    else :
      measure = "words"
    # print("Building Summary_TF_IDF. \tlimitType =", self.size_limit_type, " summary limit = ", self.summary_word_limit, measure, "\n")
    counter = 0
    while (counter < self.summary_word_limit):
      top_TF_IDF_score = min(self.TF_IDF_list)
      score_index = self.TF_IDF_list.index(top_TF_IDF_score)
      if (top_TF_IDF_score == 1000000): #breaks while loop if we're out of sentences
        break
      if (self.filtered_sentences[score_index].og_numWords >= self.min_sentence_len
          and self.filtered_sentences[score_index].og_numWords <= self.max_sentence_len) :   # only accepts 5 <= Sentence Length <= 29
        if (len(self.summary) > 0                                                # ensures that the next check doesnt go out of range.
            and self.filtered_sentences[score_index].og_sen == self.summary[-1]) :          # ignore duplicate sentences
          dummy = 0
        else:
          self.summary.append(self.filtered_sentences[score_index].og_sen) #add sentence to summary
          self.summary_word_num += self.filtered_sentences[score_index].og_numWords    #add to total word count
          #print("sentence added: ", self.summary[-1])
      self.TF_IDF_list[score_index] = 1000000   #makes it impossible to pick this sentence again
      if (self.size_limit_type == "Percent"):
        counter = len(self.summary)
      else :
        counter = self.summary_word_num
  
  