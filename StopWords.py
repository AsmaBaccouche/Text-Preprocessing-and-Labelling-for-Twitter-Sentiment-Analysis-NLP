# -*- coding: utf-8 -*-
"""
@author: Asma Baccouche
"""
import pandas as pd

def get_stopWords(Language):
    
    if(Language=='Arabic'):
        file=pd.read_excel('Util_Files/Arabic_stop_words.xlsx')
        stops=file.values.T.tolist()
        T=stops[0]
        stop_words=T
    else :
        if(Language=='French'):
            file=pd.read_excel('Util_Files/French_stop_words.xlsx')
            stops=file.values.T.tolist()
            T=stops[0]
            stop_words=T
            
        else :
            file=pd.read_excel('Util_Files/English_stop_words.xlsx')
            stops=file.values.T.tolist()
            T=stops[0]
            stop_words=T
            
    return(stop_words)