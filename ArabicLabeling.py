# -*- coding: utf-8 -*-
"""
@author: Asma Baccouche
"""
import re
import pandas as pd
import Lexicons
import Util
import pyaramorph
analyzer = pyaramorph.Analyzer()


file = open('Util_Files/Arabic_Pos_Bigrams.txt', 'r',encoding='utf8')
Pos_ar = [line[:-1].split(' ') for line in file.readlines()]

file = open('Util_Files/Arabic_Neg_Bigrams.txt', 'r',encoding='utf8')
Neg_ar = [line[:-1].split(' ') for line in file.readlines()]

def find_bigrams(input_list):
  bigram_list = []
  for i in range(len(input_list)-1):
      bigram_list.append((input_list[i], input_list[i+1]))
  return bigram_list

P,N=Lexicons.lexicons('English')

def arabic_labeling(New,lang):
    Positive,Negative=Lexicons.lexicons(lang)
    
    import GetTags
    TAGS=GetTags.get_tags(lang)
    
    A=[1/(n) for n in range(1,len(TAGS)+1)]
    A.sort()
    # Ranking the tags
    d={}
    for i in range(len(A)):
        d[TAGS[i]]=A[len(A)-1-i]
    
    
    New=pd.DataFrame(columns=['description'])   
    for j in range(len(file)):        
        s=file['description'][j]
        t=s.split()  
        for i in range(len(t)):
            t[i]=Util.strip_symbol(t[i])
        New.loc[j] = [' '.join(t)]
    
    A=list()
    for i in range(len(New)):
        s=New['description'][i]
        s=re.sub('#','',s)
        a=s.split()
        m=find_bigrams(s.split())
        bigram_pos_s=0
        bigram_neg_s=0
        
        pos_s_bi=0
        neg_s_bi=0
        for bigram in m :
            if [bigram[0],bigram[1]] in Pos_ar :
                index=a.index(bigram[0])
                if a[index-1] in ['ليس','غير','لا'] :
                    bigram_neg_s=bigram_neg_s+1
                else :
                    bigram_pos_s=bigram_pos_s+1
            else :
                if [bigram[0],bigram[1]] in  Neg_ar:
                    index=a.index(bigram[0])
                    if a[index-1] in ['ليس','غير','لا'] :
                        bigram_pos_s=bigram_pos_s+1
                    else :
                        bigram_neg_s=bigram_neg_s+1
                        
        if not(bigram_pos_s == 0 and bigram_neg_s== 0) : 
               pos_s_bi = bigram_pos_s
               neg_s_bi = bigram_neg_s
    
        else :
            # Tagging the text
            results = analyzer.analyze_text(s)
            L=list()
            for j in range(len(results)):
                word=results[j][0].split()[len(results[j][0].split())-2]
                R=results[j][1].split('       ')
                #R=results[j][len(results[j])-1].split('       ')
                R[0]=R[0][4:-1]
                R[1]=R[1][2:-1]
              
                a=R[2].split('+')[1][1:len(R[2].split('+')[1])-1]
                L.append([word,R[1].split('/')[len(R[1].split('/'))-1],a.split(';')[0].split('/')[0]])
            
            pos_s_ar_uni=1
            neg_s_ar_uni=1
            pos_s_en_uni=1
            neg_s_en_uni=1
            for i in range(len(L)):
                if L[i][0] in Positive:
                    if L[i-1][0] in ['ليس','غير','لا'] :
                        pos_s_ar_uni=pos_s_ar_uni-(pos_s_ar_uni*d[L[i][1]])
                    else :
                        pos_s_ar_uni=pos_s_ar_uni+(pos_s_ar_uni*d[L[i][1]])
                else :
                    if L[i][2] in P:
                        pos_s_en_uni=pos_s_en_uni+(pos_s_en_uni*d[L[i][1]])  
                    else :
                        if L[i][0] in Negative:
                            if L[i-1][0] in ['ليس','غير','لا'] :
                                neg_s_ar_uni=neg_s_ar_uni-(neg_s_ar_uni*d[L[i][1]])
                            else :
                                neg_s_ar_uni=neg_s_ar_uni+(neg_s_ar_uni*d[L[i][1]])
                        else :
                            if L[i][2] in N:
                                neg_s_en_uni=neg_s_en_uni+(neg_s_en_uni*d[L[i][1]])
                                
            pos_s_uni=pos_s_ar_uni*0.75+pos_s_en_uni*0.25
            neg_s_uni=neg_s_ar_uni*0.75+neg_s_en_uni*0.25
            
            pos_score=(pos_s_uni-1)*0.25+pos_s_bi*0.75
            neg_score=(neg_s_uni-1)*0.25+neg_s_bi*0.75
        
        if pos_score/len(s) == neg_score/len(s) or abs(pos_score-neg_score) < 0.001:
            polarity='Neutral'
        else :
            if neg_score/len(s) > pos_score/len(s) :
                polarity='Negative' 
            else :
                if pos_score/len(s) > neg_score/len(s) :
                    polarity='Positive'
               
        A.append(s+'\t'+polarity)
        
    LL=[a.split('\t')[1] for a in A]
    
    return(LL)