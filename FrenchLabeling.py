# -*- coding: utf-8 -*-
"""
@author: Asma Baccouche
"""
import Lexicons
import re
import treetaggerwrapper
import GetTags

def french_labeling(New,lang):

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
            lang='en'
    else :
        if lang == 'French':
            lang='fr'
    #1) build a TreeTagger wrapper accordng to the language:
    tagger = treetaggerwrapper.TreeTagger(TAGLANG=lang)
    for i in range(len(New)):
        s=New['description'][i]
        s=re.sub('#','',s)
        #2) Tagging the text
        tags = tagger.tag_text(s)
        tags2 = treetaggerwrapper.make_tags(tags)
        pos_s=1
        neg_s=1        
        for j in range(len(tags2)):
            if tags2[j][0] in Positive or tags2[j][2] in Positive:
                if tags2[j-1][0] in ['jamais','pas','ne','non']:            
                    pos_s=pos_s-(pos_s*d[tags2[j][1]])
                else :
                    pos_s=pos_s+(pos_s*d[tags2[j][1]])
            else :
                if tags2[j][0] in Negative or tags2[j][2] in Negative:
                    if tags2[j-1][0] in ['jamais','pas','ne','non']:              
                        neg_s=neg_s-(neg_s*d[tags2[j][1]])
                    else :
                        neg_s=neg_s+(neg_s*d[tags2[j][1]])
        # Mapping scores to labels            
            if pos_s/len(s) == neg_s/len(s) or abs(pos_s-neg_s) < 0.05 :
                polarity='Neutral'
            else :
                if neg_s/len(s) > pos_s/len(s) :
                   polarity='Negative' 
                else :
                    if pos_s/len(s) > neg_s/len(s) :
                        polarity='Positive'
                    
        L.append(s+'\t'+polarity)
    LL=[a.split('\t')[1] for a in L]
    
    return(LL)
