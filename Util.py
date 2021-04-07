# -*- coding: utf-8 -*-
"""
@author: Asma Baccouche
"""
from os import listdir
from os.path import isfile, join
import pandas as pd

def open_folder(path):
    files = [f for f in listdir(path) if isfile(join(path, f))]    
    return(files)

def merge(path,files):
    D=pd.read_csv(path+'/'+files[0],index_col=0)
    for k in range(len(files)):        
        A=pd.read_csv(path+'/'+files[k],index_col=0)
        D = D.append(A)        
    D=D.reset_index(drop=True)
    return(D)

def is_symbol(char):
    b=False
    ranges = [(0x1F601, 0x1F64F),
              (0x2702, 0x27B0),
               (0x1F680, 0x1F6C0),
                (0x24C2, 0x1F251),
                (0x1F600, 0x1F636),
                 (0x1F681, 0x1F6C5),(0x0038, 0x1F5FF),
                (0x1F30D, 0x1F567),(0x00A9, 0x00AE)]
    
    for current_range in ranges :
        if ord(char) in current_range or ord(char) >120000 or ord(char)>9000:
            b=True
    return(b)

def strip_symbol(t):   
    if len(t) <2 and is_symbol(t) :
        s=t.replace(t,"")
    else :
        s=t
    return(s)

def strip_stopwords(f,Stopwords):
    meaningful_words = [w for w in f if not w in Stopwords]       
    return(meaningful_words)
