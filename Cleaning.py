# -*- coding: utf-8 -*-
"""
@author: Asma Baccouche
"""
import TweetsCleaning
import pandas as pd

def clean(data,path,Cleaning_threshold):
    # first cleaning
    S,d = TweetsCleaning.similarity(data,path,Cleaning_threshold)
    l = TweetsCleaning.remove_duplicate(S,d)
    # second cleaning
    D = l.sort_values(by='description')
    D = D.reset_index(drop=True)    
    C = TweetsCleaning.duplication(D,Cleaning_threshold)
    Clean = TweetsCleaning.remove_duplicate(C,D)
    yield(d)
    yield(C)
    yield(Clean)
    
def preprocessing(f,path,Cleaning_threshold) :
    
    data = pd.read_excel(path+'/'+f)
    data = TweetsCleaning.reconstruct_data(data,path)
        
    d,_,Clean=clean(data,path,Cleaning_threshold)
    filter = Clean['description'] != ""
    Clean = Clean[filter]
    filter = Clean['description'] != 'NaN'
    Clean = Clean[filter]
    Name=f.replace(".xlsx","",1)       
    # saving the clean files
    Clean.to_csv(Name+'_clean.csv',encoding='utf-8')      
    yield(d)
    yield(Clean)
    