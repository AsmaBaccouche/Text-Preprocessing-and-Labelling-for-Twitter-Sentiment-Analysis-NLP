# -*- coding: utf-8 -*-
"""
@author: Asma Baccouche
"""

import treetaggerwrapper
import GetTags
import Lexicons
import re

file = open('Util_Files/Pos_Bigrams.txt', 'r')
Pos = [line[:-1].split(' ') for line in file.readlines()]
Pos = Pos[1:]

file = open('Util_Files/Neg_Bigrams.txt', 'r')
Neg = [line[:-1].split(' ') for line in file.readlines()]
Neg = Neg[1:]
 
def find_bigrams(input_list):
  bigram_list = []
  for i in range(len(input_list)-1):
      bigram_list.append((input_list[i], input_list[i+1]))
  return bigram_list

def english_labeling(New,lang):
    
    TAGS=GetTags.get_tags(lang)
    
    A=[1/(n) for n in range(1,len(TAGS)+1)]
    A.sort()
    # Ranking the tags
    d={}
    for i in range(len(A)):
        d[TAGS[i]]=A[len(A)-1-i]
    # Generating positive and negative lexicos for words labeling
    Positive,Negative=Lexicons.lexicons(lang)
    # Extracting sentences      
    L=[]
    if lang == 'English':
            l='en'
    else :
        if lang == 'French':
            l='fr'
    #1) build a TreeTagger wrapper accordng to the language:
    tagger = treetaggerwrapper.TreeTagger(TAGLANG=l)
    for i in range(len(New)):
        s=New['description'][i]
        s=re.sub('#','',s)
                
        a=s.split()
        m=find_bigrams(a)
        bigram_pos_s=0
        bigram_neg_s=0
        
        pos_s_bi=0
        neg_s_bi=0
        for bigram in m :
            if [bigram[0],bigram[1]] in Pos :
                index=a.index(bigram[0])
                if a[index-1] in ['not','no','dont','cant','wont','didnt','couldnt','never'] :
                    bigram_neg_s=bigram_neg_s+1
                else :
                    bigram_pos_s=bigram_pos_s+1
            else :
                if [bigram[0],bigram[1]] in  Neg:
                    index=a.index(bigram[0])
                    if a[index-1] in ['not','no','dont','cant','wont','didnt','couldnt','never'] :
                        bigram_pos_s=bigram_pos_s+1
                    else :
                        bigram_neg_s=bigram_neg_s+1
                    
        if not(bigram_pos_s == 0 and bigram_neg_s== 0) : 
            pos_s_bi = bigram_pos_s
            neg_s_bi = bigram_neg_s
        
        else:
            # Get the occurence of words in each sentence
            occ=dict((word,s.count(word)) for word in s.split())
            #2) Tagging the text
            tags = tagger.tag_text(s)
            tags2 = treetaggerwrapper.make_tags(tags)
            pos_s_uni=1
            neg_s_uni=1        
            for j in range(len(tags2)):
                if tags2[j][0] in Positive or tags2[j][2] in Positive:
                    if tags2[j-1][0] in ['not','no','dont','cant','wont','didnt','couldnt','never'] :         
                        pos_s_uni=pos_s_uni-(pos_s_uni*d[tags2[j][1]]*occ[tags2[j][0]])
                    else :
                        pos_s_uni=pos_s_uni+(pos_s_uni*d[tags2[j][1]]*occ[tags2[j][0]])
                else :
                    if tags2[j][0] in Negative or tags2[j][2] in Negative:
                        if tags2[j-1][0] in ['not','no','dont','cant','wont','didnt','never'] :             
                            neg_s_uni=neg_s_uni-(neg_s_uni*d[tags2[j][1]]*occ[tags2[j][0]])
                        else :
                            neg_s_uni=neg_s_uni+(neg_s_uni*d[tags2[j][1]]*occ[tags2[j][0]])
                            
        pos_score=(pos_s_uni-1)*0.25+pos_s_bi*0.75
        neg_score=(neg_s_uni-1)*0.25+neg_s_bi*0.75
        # Mapping scores to labels            
        if pos_score/len(s) == neg_score/len(s) or abs(pos_score-neg_score) < 0.05 :
            polarity='Neutral'
        else :
            if neg_score/len(s) > pos_score/len(s) :
               polarity='Negative' 
            else :
                if pos_score/len(s) > neg_score/len(s) :
                    polarity='Positive'
                    
                    
        L.append(s+'\t'+polarity)
    LL=[a.split('\t')[1] for a in L]
    
    return(LL)