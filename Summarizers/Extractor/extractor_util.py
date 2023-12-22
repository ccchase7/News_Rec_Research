import numpy as np
import math
from scipy.special import rel_entr

# formula for P's divergence from Q: KL(P || Q) = – sum x in X P(x) * log(Q(x) / P(x))
# If we are attempting to approximate an unknown probability distribution, then the target probability distribution from data is P, and Q is our approximation of the distribution.

def kl_archive_divergence(arcDict, arcWordNum, senDict, senWordNum):
  sum = 0
  if( senWordNum == 0): #Sometimes punctuation will slip, causing a new sentence that has no words this filters those out.
    return 1000
  for word in senDict:
    a = arcDict[word] / arcWordNum
    b = (senDict[word] / senWordNum)
    val = a * np.log( a / b )    #Sophie version
    sum += val
    #print("for: ", word, "\t", a," * log(", a , " / ", b, ") = \t", val, flush=True)
  sum = sum / senWordNum #normalizes the scores based on sentence length.
  return sum

p = [0.10, 0.40, 0.50]
q = [0.80, 0.15, 0.05]
def kl_ex(p, q):
	return sum(p[i] * np.log(p[i]/q[i]) for i in range(len(p)))

def GetTF_Score(senDict, word, maxFrequency) :
  return senDict[word] / maxFrequency

# getting IDF_keyword
def GetIDF_Word(arcNumSen, numSenWithKeyword ) :
  return math.log2(arcNumSen / numSenWithKeyword)

# KL_TF_IDF for one sentence
def KL_TF_IDF(num_sentences, sentence_data, full_dict, sentences_with_word_dict) :
  sen_word_freq_dict = sentence_data.dictionary
  senScore = 0
  maxFrequency = max(full_dict, key=full_dict.get)
  
  for word in sen_word_freq_dict :
    numSenWithKeyword = sentences_with_word_dict[word]
    IDF = GetIDF_Word(num_sentences, numSenWithKeyword)
    TF = GetTF_Score(sen_word_freq_dict, word, maxFrequency)
    senScore += (IDF * np.log(IDF / TF))

  senScore = senScore / sentence_data.filt_num_words
  return senScore