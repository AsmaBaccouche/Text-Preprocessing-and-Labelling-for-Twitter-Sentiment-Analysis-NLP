# -*- coding: utf-8 -*-
"""
@author: Asma Baccouche
"""
from POSTaggerLemma import Tagg_Lemma

def tagging(sentences,path):
    if path == 'Arabic':    
        return(POSTagg(sentences))
    else:
        return(Tagg_Lemma(sentences,path))