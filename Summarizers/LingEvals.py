def LingEvals(summary_content):
    lingList = []
    nGrams = 2
    redunScore = -1 * (1 - uniqueNgramRatio(summary_content, nGrams))

    lingList.append(0)                                                  #get_coherence_score2(self.ext250))
    lingList.append(get_focus_score(ext))
    lingList.append(redunScore)                                         #get_redundency_score(self.ext250))
    lingList.append(grammarScore(ext))
    lingList.append(sum(lingList))

    print("ext250 LingEvals: ")
    print("grammer    : \t", lingList[3])
    print("coherence  : \t", lingList[0])
    print("redundancy : \t", lingList[2])
    print("focus      : \t", lingList[1])
    print("Readability: \t", lingList[4])
