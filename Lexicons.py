# -*- coding: utf-8 -*-
"""
@author: Asma Baccouche
"""
import pandas as pd
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer

def lexic(word):
    blob = TextBlob(word, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
    return(blob.sentiment[0])

def lexicons(path):
    if (path=='English'):
  
        with open('Util_Files/English_positive.txt') as f:
            content = f.readlines()
        Positive = [x.strip() for x in content]
        
        with open('Util_Files/English_negative.txt') as f:
            content = f.readlines()
        Negative = [x.strip() for x in content]
    else:
        if (path=='Arabic'):

            lex=pd.read_excel('Util_Files/Arabic_lexicons.xlsx')
            Lexicons=pd.DataFrame(columns=['word', 'polarity'])
            Lexicons2=pd.DataFrame(columns=['word', 'polarity'])
            for i in range(len(lex)):
                if (len(lex['ngram'][i].split()) < 2 ):
                    Lexicons.loc[len(Lexicons)]=[lex['ngram'][i],lex['polarity'][i]]
                else :
                    if (len(lex['ngram'][i].split()) == 2 ):
                        Lexicons2.loc[len(Lexicons2)]=[lex['ngram'][i],lex['polarity'][i]]
                        
                            
            Positive=[]
            Negative=[]
            for i in range(len(Lexicons)):
                if Lexicons['polarity'][i] == 1:
                    Positive.append(Lexicons['word'][i])
                else:
                    Negative.append(Lexicons['word'][i])
                    
            Pos_bigram=list()
            Neg_bigram=list()
            for i in range(len(Lexicons2)):
                if Lexicons['polarity'][i] == 1:
                    Pos_bigram.append(Lexicons2['word'][i])
                else:
                    Neg_bigram.append(Lexicons2['word'][i])
                        
            
            with open('Util_Files/Arabic_Pos_Bigrams.txt', 'w', encoding='utf-8') as thefile:
                for item in Pos_bigram:
                    thefile.write("%s\n" % item)
            thefile.close()
            with open('Util_Files/Arabic_Neg_Bigrams.txt', 'w', encoding='utf-8') as thefile:
                for item in Neg_bigram:
                    thefile.write("%s\n" % item)
            thefile.close()
                    
            with open('Util_Files/Arabic_positive.txt', 'w', encoding='utf-8') as thefile:
                for item in Positive:
                    thefile.write("%s\n" % item)
            thefile.close()
                    
            with open('Util_Files/Arabic_negative.txt', 'w', encoding='utf-8') as thefile:
                for item in Negative:
                    thefile.write("%s\n" % item)
            thefile.close()
      
        else:
            if (path=='French'):

                lex=pd.read_excel('Util_Files/French_lexicons.xlsx')
                Lexicons=pd.DataFrame(columns=['word', 'polarity'])
                
                for i in range(len(lex)):
                    if (lex['TomDS'][i]>0):
                        Lexicons.loc[len(Lexicons)]=[lex['ADJECTIVE'][i],1]
                    else :
                        if (lex['TomDS'][i]<0):
                            Lexicons.loc[len(Lexicons)]=[lex['ADJECTIVE'][i],-1]
                        else :
                            if (lex['TomDS'][i]==0):
                                Lexicons.loc[len(Lexicons)]=[lex['ADJECTIVE'][i],0]
                            else :
                                if ((lex['POS FREQ'][i]==1) and (lex['NEG FREQ'][i]==0)):
                                    Lexicons.loc[len(Lexicons)]=[lex['ADJECTIVE'][i],1]
                                else :
                                    if ((lex['POS FREQ'][i]==0) and (lex['NEG FREQ'][i]==1)):
                                        Lexicons.loc[len(Lexicons)]=[lex['ADJECTIVE'][i],-1]
                                    else :
                                        if (lexic(lex['ADJECTIVE'][i]) > 0):
                                            Lexicons.loc[len(Lexicons)]=[lex['ADJECTIVE'][i],1]
                                        else :
                                            if (lexic(lex['ADJECTIVE'][i]) < 0):
                                                Lexicons.loc[len(Lexicons)]=[lex['ADJECTIVE'][i],-1]
                                            else :
                                                Lexicons.loc[len(Lexicons)]=[lex['ADJECTIVE'][i],0]
                Positive=[]
                Negative=[]
                for i in range(len(Lexicons)):
                    if Lexicons['polarity'][i] == 1:
                        Positive.append(Lexicons['word'][i])
                    else:
                        if Lexicons['polarity'][i] == -1:
                            Negative.append(Lexicons['word'][i])
                            
                with open('Util_Files/French_positive.txt', 'w') as thefile:
                    for item in Positive:
                        thefile.write("%s\n" % item)
                thefile.close()
                        
                with open('Util_Files/French_negative.txt', 'w') as thefile:
                    for item in Negative:
                        thefile.write("%s\n" % item)
                thefile.close()
                         
    yield(Positive)
    yield(Negative)