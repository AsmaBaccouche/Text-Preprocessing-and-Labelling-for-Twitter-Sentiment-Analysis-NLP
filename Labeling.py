# -*- coding: utf-8 -*-
"""
@author: Asma Baccouche
"""
import pandas as pd
import Util
import re
import ArabicLabeling
import EnglishLabeling
import FrenchLabeling

# Emoji labeling
Positive_emojis=["😀","😁","😂","😃","😄","😅","😆","😉","😊","😋","😎","😍","😘","❤️"]  
Negative_emojis=["☺","😨","😩","😢","😟","😞","🙁","😔","😯","😥","😑","🤔","😪","💔","😏","😭"]


def polarity(label1,label2) :
    if (label1=="Positive" and label2=="Negative") :
        n="Negative"            
    else :
        if (label1=="Negative" and label2=="Positive") :
            n="Negative"
        else :
            if label1==label2 :
                n=label1
            else :
                if label1=="Neutral":
                    n=label2
                else :
                    n=label1
        return(n)
    
functions={'polarity' : polarity}

def emojis_labeling(D,path):
    file=D
    # Adding new column for empojis labeling
    file['polarity'] = pd.Series('', index=file.index)    
    # Mapping sentences thant contain +/- emojis
    for i in range(len(file)):   
        L=file['description'][i].split()
        for j in range(len(L)):
            if (L[j] in Positive_emojis):
                b="Pos"
            else :
                if (L[j] in Negative_emojis):
                    b="Neg"
                else :
                    b="Neu"
        if b=="Pos":
            file['polarity'][i] = "Positive"
        else : 
            if b=="Neg":        
                file['polarity'][i] = "Negative"
            else :            
                file['polarity'][i] = "Neutral"
    # Removing emojis from sentences after labeling it                 
    New=pd.DataFrame(columns=['description','polarity'])   
    for j in range(len(file)):        
        s=file['description'][j]
        t=s.split()  
        for i in range(len(t)):
            t[i]=Util.strip_symbol(t[i])
        New.loc[j] = [' '.join(t),file['polarity'][j]]
        
    return(New)

def semantic_labeling(New,lang):
               
    if lang=='English':
        LL=EnglishLabeling(New,lang)
    else :
        if lang=='French':
            LL=FrenchLabeling(New,lang)
        else :
            LL=ArabicLabeling(New,lang)
    
    # Adding new column for unigrams labeling
    Result=pd.DataFrame(columns=['description','emojis_polarity'])
    for i in range(len(New)):
        Result.loc[len(Result)]=[re.sub('#','',New['description'][i]),New['polarity'][i]]    
    Result['unigrams_polarity'] = pd.Series(LL, index=Result.index)
    # Merging two labels into a final one
    Final=pd.DataFrame(columns=['description','polarity'])

    for i in range(len(Result)):
        a=Result['emojis_polarity'][i]
        b=Result['unigrams_polarity'][i]
        polarity=functions['polarity']
        Final.loc[len(Final)]=[Result['description'][i],polarity(a,b)]
    return(Final)

def labeling(D,path):
    
    New = emojis_labeling(D,path)
    Final = semantic_labeling(New,path)
    return(Final)