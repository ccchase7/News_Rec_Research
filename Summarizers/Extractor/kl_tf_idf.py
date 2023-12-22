import numpy as np

# KL_TF_IDF for one sentence
# For getting number of sentences with the target keyword
def getNumSenWithKeyword(senList, keyword):
  count = 0
  for sentence_data in senList :
    if (sentence_data.dictionary.get(keyword) != None ) :
      count += 1

  return count

def GetSenWordWithMaxFrequency(senDict) :  #get the frequency of the most frequent word in sentence
  maxFrequency = 0
  for word in senDict :
    if senDict[word] > maxFrequency :
      maxFrequency = senDict[word]
  return maxFrequency

def GetTF_Score(senDict, word, maxFrequency) :
  return senDict[word] / maxFrequency

import math

def GetIDF_Word(arcNumSen, numSenWithKeyword ) :
  return math.log2(arcNumSen / numSenWithKeyword)

def KL_TF_IDF(total_num_sentences, sentence_data, filtered_sentences) :
  senScore = 0
  #print(" sentence:", sen.filt_sen, "_____\n\n")
  maxFrequency = GetSenWordWithMaxFrequency(sentence_data.dictionary)
  if maxFrequency == 0 :
    return 0
  for word in sentence_data.dictionary :
    numSenWithKeyword = getNumSenWithKeyword(filtered_sentences, word)
    IDF = GetIDF_Word(total_num_sentences, numSenWithKeyword)
    TF = GetTF_Score(sentence_data.dictionary, word, maxFrequency)
    # print(f"Tf: {TF}\tIDF: {IDF}")
    senScore += (IDF * np.log(IDF / TF))

  senScore = senScore / sentence_data.filt_num_words
  # print(f"{senScore} for {sentence_data.og_sen}")
  return senScore