# -*- coding: utf-8 -*-
"""
@author: Asma Baccouche
"""
import treetaggerwrapper
import pandas as pd
from Lexicons import lexicons
    
def Tagg_Lemma(sentences,path):
    if path == 'English':
        lang='en'
    else :
        if path == 'French':
           lang='fr'
           
    Positive,Negative=lexicons(path)      
    #1) build a TreeTagger wrapper accordng to the language:
    tagger = treetaggerwrapper.TreeTagger(TAGLANG=lang)
    f=pd.DataFrame(columns=['Unigram', 'POS-Tag', 'Lemma', 'Polarity'])  
      
    for i in range(len(sentences)):
        s=' '.join(sentences[i])
        #2) tag your text
        tags = tagger.tag_text(s)
        #3) use the tags list... (list of string output from TreeTagger)
        tags2 = treetaggerwrapper.make_tags(tags)
        
        for j in range(len(tags2)):
            word,pos,lemma=tags2[j]
            if word in Positive:
                f.loc[len(f)]=[word,pos,lemma,1]
            else :
                if word in Negative:
                    f.loc[len(f)]=[word,pos,lemma,-1]
                else :
                    f.loc[len(f)]=[word,pos,lemma,0]
        
    f=f.sort_values(by='Unigram')
    f=f.reset_index(drop=True)
    
    #4) remove duplicate words
    final=pd.DataFrame(columns=['Unigram', 'POS-Tag', 'Lemma', 'Polarity'])
    for j in range(len(f)-1):
        if(f['Unigram'][j]!=f['Unigram'][j+1]):
            final.loc[len(final)]=[f['Unigram'][j],f['POS-Tag'][j],f['Lemma'][j],f['Polarity'][j]]
            
    return(final)

