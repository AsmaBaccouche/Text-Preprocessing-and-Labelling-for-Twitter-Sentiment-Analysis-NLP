# -*- coding: utf-8 -*-
"""
@author: Asma Baccouche
"""
import pandas as pd
import re
from difflib import SequenceMatcher

def reconstruct_data(data,lang):
    
    if (lang=='English'):
        lang='en'
    else :
        if(lang=='French'):
            lang='fr'
        else :
            lang='ar'
            
    D=pd.DataFrame(columns=['description'])
    for i in range(len(data)):
        if type(data['description'][i])!=float and type(data['description'][i])!=int and data['lang'][i]==lang:
            D.loc[len(D)]=data.ix[i]['description']
    return(D)

# Remove URL , @user and other symbols
def strip_sentence(s,lang):    
    s=re.compile("http\S+").sub('', re.compile('RT @\w+: ').sub('', s, count=1)).strip()
    s=re.compile("@\w").sub('', re.compile('RT ').sub('', s, count=1)).strip()
    # Remove repeating characters from words
    s=re.sub(r'(.)\1+', r'\1\1', s)
    s=re.sub(chr(1617),'',s)
    s=re.sub(chr(1615),'',s)

    Symbols='‍ø{}[]✔()¤»“‘¨ºðŸ‡•↕‼¶▬↨↑↓→↩←∟↔\"&½¼*+,-./@¯±²³´µ™›œŸ¡¢£¤¦¨©ª«¬®¶·¸¹º»¼½¾ˆÿœ؟°¯¾ºƒ£^â~//íóñü¿¡¼â¹³‹“”…,._:\|\"«*»+?!;-=،%$€¦™±´–¶ï¸¨¢˜¥ð§¡¤®—‘’„†‡•…‰><‚›ª²'   
    for char in Symbols:
        s = s.replace(char,'')
        
    Numbers=["0","1","2","3","4","5","6","7","8","9","٠","١","٢","٣","٤","٥","٦","٧","٨","٩"]    
    for char in Numbers :
        s=re.sub(char,'', s)
    Codes='\x90\xad\x9d'
    for char in Codes:
        s = s.replace(char,'')
    Alephs="آأإ"
    for char in Alephs:
        s = s.replace(char,"ا")
    t=s.split(' ')
    n=list()
    for a in t:
        if len(a) > 1:
            for char in a :
                if char == 'Ã' :
                    a=re.sub(char,"é", a)
            n.append(a)
        else :
            a=re.sub('Ã',"à", a)
            n.append(a)
    s=' '.join(n)
    
    t=s.split(' ')
    m=list()
    for word in t:
        if len(word)>1:
            for char in word :
                if char == 'â' :
                    word=re.sub(char,"", word)
            m.append(word)
        else :
            m.append(word)
    s=' '.join(m)
    
    Synonyms=[('السرطان', 'سرطان'),('الضغط', 'ضغط'),('الصحة', 'صحة'),('السمنه','السمنة'), ('التامين','تامين')
        , ('حميه','حمية'),('شركات', 'شركة'),('بقصف','قصف'),('المصحات', 'مصحة')
        ,('لمرضى','مرضى'),('مصحه','مصحة'),('صيدليه','صيدلية'),('obésite','obésité'),('obesité','obésité'),('touscandidatsalamaladie','tous candidats à la maladie' ),
        ('obesite','obésité'),('perdredupoids','perdre du pois'),('l\'obesité','obésité'),('sante','santé'),
       ('hépital','hopital'),('gréce','grâce'),('déjé','déjà'),('yrs','years'),('\'ll','will'),
       ('wont','will not'),('méme','même'),('challengingbehaviors','challenging behaviors'),
       ('rememb','remember'),('personshedfieldlodge','person shedfield lodge'),('retweeted','')]
        #('regime','régime')
    for i in range(len(Synonyms)):
        s=re.sub(Synonyms[i][0],Synonyms[i][1],s)

    for char in s:
        if char == 'ž' :
            s=re.sub(char,"", s)
    for char in s:
        if char == '\'s' :
            s=re.sub(char,"", s)
    if lang !='French':
        for char in s:
            if char == '\'' :
                s=re.sub(char,"", s)
            if char == '`' :
                s=re.sub(char,"", s)
            if char == 'œ' :
                s=re.sub(char,"", s)
            if char == 'é' :
                s=re.sub(char,"", s)
                
    for char in s:
        if char == 'š' :
            s=re.sub(char,"", s)
            
    return(s)
    
def is_arabic(char):
    B=False
    if ord(char) in range (0x0600, 0x06FF):
          B=True
    return(B)

def split_arabic_latin(word):
    new=''
    i=0
    while(i<len(word)-1):
        if (is_arabic(word[i])==is_arabic(word[i+1])):
            new=new+word[i]
        else :
            if (word[i]=='#') or (word[i+1]=='#'):
                new=new+word[i]
            else :
                new=new+word[i]+' '
        i=i+1
    word=new+word[len(word)-1]    
    return(word)

def reconstruct_hashtags(word):    
    new=''
    for i in range(1,len(word)):
        
        if word[i]=='#':
            if word[i-1]!=' ':
                new=new+' '+word[i]
            else :
                new=new+word[i]
        else :
            new=new+word[i]
    new=word[0]+new               
    return(new)

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

def split_symbol_char(word):
    new=''
    i=0
    while(i<len(word)-1):
        if (is_symbol(word[i]) == True and is_symbol(word[i+1]) == False) or (is_symbol(word[i]) == False and is_symbol(word[i+1]) == True):
            if is_arabic(word[i]) or is_arabic(word[i+1]):                
                new=new+word[i]+' '
            else :
                new=new+word[i]+' '
        else:
            new=new+word[i] 
        i=i+1
    word=new+word[len(word)-1]    
    return(word)

def split_symbol_symbol(word):
    new=''
    for i in range(len(word)-1):
        if (is_symbol(word[i]) == True and is_symbol(word[i+1]) == True):
            new=new+(word[i])+' '
        else:
            new=new+(word[i])
    new=new+word[len(word)-1]
    return(new)

def recostruct_tweet(s,lang):
    s=strip_sentence(s,lang)
    t=s.split()
  
    for i in range(len(t)):
        t[i]=split_symbol_symbol(t[i])
        t[i]=split_symbol_char(t[i])
        #t[i]=strip_symbol(t[i])
    str1 = ' '.join(t)
    t=str1.split()
    
    for i in range(len(t)):
        t[i]=split_arabic_latin(t[i])
        t[i]=reconstruct_hashtags(t[i])
                
    str2 = ' '.join(t)
    sentence=str2.split()    
    return(sentence)

# Striping ponctuation
def strip_ponct(f): 
    ponct=['️','؛','٪','’','+','--','\'','‼️','/','"','!!','.(','#','#)','!@...','!..','!.','!-','-','!','.',':','…','?'
    '...','؟','؟؟','(',')','..','|','،','?','=','.','--','\'','!','/','"','#','-',':','…','?','...','_',
]
    sentence = [w for w in f if not w in ponct]  
    return(sentence)

def tweet_vector(s,lang):
    f=recostruct_tweet(s,lang)
    low_words = [word.lower() for word in f]
    sentence=strip_ponct(low_words)
    return(sentence)

def similar(a,b):
    return SequenceMatcher(None, a, b).ratio()

def duplication(d,Cleaning_threshold):
    duplication=pd.DataFrame(columns=['index','duplicate_index'])
    for i in range(len(d)-1):
        s1=d['description'][i]
        s2=d['description'][i+1]
        
        if similar(s1,s2)*100 > Cleaning_threshold:
            duplication.loc[len(duplication)]=[i,i+1]
    return(duplication)

def similarity(data,lang,Cleaning_threshold):
    data['hash'] = pd.Series('',index=data.index)
    for j in range(len(data)):
        s=' '.join(tweet_vector(data['description'][j],lang))
        data['description'][j]=s
        data['hash'][j]=hash(s)
    d=data.sort_values(by='hash')
    d=d.reset_index(drop=True)   
    dup=duplication(d,Cleaning_threshold)
    yield(dup)
    yield(d)    

def remove_duplicate(S,d):    
    L=S['duplicate_index'].tolist()
    New=pd.DataFrame(columns=['description'])
    for i in range(len(d)):
        if i not in L:
            New.loc[len(New)]=[d['description'][i]]        
    return(New)