"""
Rock News NLP: Dictionary-based Named Entity Recognition
Created on Sun Jun 25 15:56:58 2023
@author: IvoBarros
"""

import pandas as pd
import numpy as np
import os
import os.path
from rock_news_nlp_class_text_preprocessing import text_preprocessing as tpp
import rock_news_nlp_utilities as utils_tpp
from time import time

def text_preprocessing(lst):
    """
    To execute preprocessing tasks
    
    Args:
        lst : list         
		
    Returns:
	list
    """   
    
    lst_txt_temp = [tpp.remove_punctuation(i) for i in lst]
    lst_txt_temp = [tpp.replace_keywords(i, {'himband': ['HIM']}) for i in lst_txt_temp]
    lst_txt = [i.lower() for i in lst_txt_temp]
    return lst_txt

def dfcol_to_list(df,df_column):
    """
    To convert a pandas dataframe column into a list and execute the defined 
    preprocessing tasks

    Args:
        df : DataFrame
        df_column : str
		
    Returns:
	list     
    """    
    list_df_col = df[df_column].to_list()
    list_clean = text_preprocessing(list_df_col)
    return list_clean

print("The script is running...")
t_start = time()

#==============================================================================
# 1. TEXT PREPROCESSING
#==============================================================================

## 1.1. LOAD DATA
path_parent_dir = os.path.dirname(os.getcwd())
path_data = f'{path_parent_dir}\data'
path_data_web_scrapers = f'{path_data}\web_scrapers'
path_data_support_files = f'{path_data}\support_files'
path_output_csv = f'{path_parent_dir}\output\csv'

df_rock_news = pd.read_csv(f'{path_data_web_scrapers}/rock_news.csv',sep=';')
df_rock_artist_md = pd.read_csv(f'{path_data_web_scrapers}/rock_artist_masterdata.csv',sep=';')
df_rock_artist_members = pd.read_csv(f'{path_data_web_scrapers}/rock_artist_members.csv',sep=';')
df_dict_text_clean_support = pd.read_csv(f'{path_data_support_files}/support_dict_rock_artist_text_clean.csv',sep=';')

## 1.2. CREATE SUPPORT DICTIONARIES FROM THE ROCK ARTIST REFERENCE TABLES
## ROCK ARTIST DICTIONARIES & SET
df_rock_artist_md = df_rock_artist_md[~df_rock_artist_md['rock_artist'].isin(['The Band',"Sweet","!!!"])]
list_rock_artist_clean = dfcol_to_list(df_rock_artist_md,'rock_artist')
dict_rock_artist = dict(zip([tpp.replace_keywords(i, {'yesband': ['yes']}) for i in list_rock_artist_clean], df_rock_artist_md['rock_artist'].to_list()))
set_rock_artist = set(dict_rock_artist.keys())
### ROCK ARTIST ADDITIONAL SET
set_rock_artist_additional = set([i[4:len(i)] for i in list_rock_artist_clean if (i.startswith('the ') and 
                                  i !='the new year' and len((i).split(' '))>=3) or i=='the beatles'])
## ROCK ARTIST MEMBER SET & DICTIONARY
list_members_clean = dfcol_to_list(df_rock_artist_members,'description')
dict_rock_artist_members = dict(zip(list_members_clean, df_rock_artist_members[['description','rock_artist']].values.tolist()))
set_rock_artist_members = set(dict_rock_artist_members.keys())

## 1.3. JOIN THE ROCK NEWS HEADLINES AND DESCRIPTIONS AND CONVERT THE TEXT CORPUS INTO A LIST
df_rock_news['title_desc'] = df_rock_news['title'] + ' ' + df_rock_news['description']
df_rock_news_subset = df_rock_news.iloc[0:20000,np.r_[-2,-1]].copy()
corpus_title_desc = df_rock_news_subset['title_desc'].to_list()

## 1.4. TEXT PREPROCESSING TASKS
corpus_title_desc_clean = text_preprocessing(corpus_title_desc)
### ADDITIONAL TEXT PREPROCESSING TASKS 
keyword_dict = df_dict_text_clean_support.groupby('values')['key'].agg(list).to_dict()
corpus_title_desc_clean = [tpp.replace_keywords(i, keyword_dict) for i in corpus_title_desc_clean]


#==============================================================================
# 2. IDENTIFY AND EXTRACT THE ROCK ARTIST AND THE ROCK ARTIST MEMBER
#==============================================================================

## 2.1. ROCK ARTIST AND ROCK ARTIST MEMBER SEARCH ON THE TEXT CORPUS AND EXTRACTION 
extracted_rock_artists = {'title_desc_clean': [], 'rock_artist_tags_prep': [], 'members_tags': []}
extracted_rock_artists['title_desc_clean'].extend(corpus_title_desc_clean)
extracted_rock_artists['rock_artist_tags_prep'].extend([[i for i in set_rock_artist if tpp.word_search(i,j)==True] for j in corpus_title_desc_clean])
extracted_rock_artists['members_tags'].extend([[i for i in set_rock_artist_members if tpp.word_search(i,j)==True] for j in corpus_title_desc_clean])
df_rock_artist_tags_prep = pd.DataFrame(extracted_rock_artists)
df_temp_tags_null = df_rock_artist_tags_prep['title_desc_clean'][df_rock_artist_tags_prep['rock_artist_tags_prep'].str.len() == 0].to_frame()
df_temp_tags_null['rock_artist_tags_add'] = df_temp_tags_null['title_desc_clean'].apply(lambda x: [f'the {i}' for i in set_rock_artist_additional if tpp.word_search(i,x)==True])
df_temp_tags_null = df_temp_tags_null.iloc[:,np.r_[-1]].copy()
df_rock_artist_tags_prep = df_rock_artist_tags_prep.join(df_temp_tags_null)
utils_tpp.return_empty_list_from_nan(df_rock_artist_tags_prep,['rock_artist_tags_add'])

## 2.2. RETURN THE BANDS OF THE IDENTIFIED MEMBERS AND REVISE PREVIOUSLY MANIPULATED ROCK ARTISTS NAMES
for i in ['rock_artist_tags_prep','rock_artist_tags_add','members_tags']:
    globals()[f'{i}_exploded'] = df_rock_artist_tags_prep[f'{i}'][df_rock_artist_tags_prep[f'{i}'].str.len()>0].copy()
    globals()[f'{i}_exploded'] = globals()[f'{i}_exploded'].to_frame().explode(i)
    globals()[f'{i}_exploded']['index_1'] = globals()[f'{i}_exploded'].index

df_members_temp = rock_artist_tags_prep_exploded.merge(rock_artist_tags_add_exploded,how="outer",on='index_1').merge(members_tags_exploded,how="outer",on='index_1') 
df_members_temp['rock_artist_tags_prep'] = df_members_temp['rock_artist_tags_prep'].map(dict_rock_artist)
df_members_temp['rock_artist_tags_add'] = df_members_temp['rock_artist_tags_add'].map(dict_rock_artist)
df_members_temp['tags_rock_artist_from_member_tags'] = df_members_temp['members_tags'].map(dict_rock_artist_members).str[1]
df_members_temp['members_tags'] = df_members_temp['members_tags'].map(dict_rock_artist_members).str[0]
df_members_temp = df_members_temp.dropna(subset=df_members_temp.columns.difference(['index_1']),how='all')
df_members_temp = df_members_temp.fillna('')
df_members_temp[df_members_temp.columns.difference(['index_1'])].astype(str)
df_members_temp = df_members_temp.groupby('index_1').agg(pd.Series.tolist)
df_rock_artist_tags = df_rock_news_subset.iloc[:,0].to_frame().join(df_members_temp)
utils_tpp.return_empty_list_from_nan(df_rock_artist_tags,['rock_artist_tags_prep','rock_artist_tags_add','tags_rock_artist_from_member_tags','members_tags'])
utils_tpp.replace_list_empty_string(df_rock_artist_tags,['rock_artist_tags_prep','rock_artist_tags_add','tags_rock_artist_from_member_tags','members_tags'])
df_rock_artist_tags['rock_artist_tags'] = df_rock_artist_tags['rock_artist_tags_prep'] + df_rock_artist_tags['rock_artist_tags_add'] + df_rock_artist_tags['tags_rock_artist_from_member_tags']
utils_tpp.remove_dups_sort_lists(df_rock_artist_tags,['rock_artist_tags','members_tags'])


#==============================================================================
# 3. SAVE DATA AS CSV FILE
#==============================================================================

## 3.1. IDENTIFIED ROCK ARTISTS AND ROCK ARTIST MEMBERS PER TEXT
df_rock_artist_tags = df_rock_artist_tags.iloc[:,np.r_[0,-1,-3]]
df_rock_artist_tags.to_csv(f'{path_output_csv}/rock_news_nlp_rock_artist_tags.csv', header=True, index=False, encoding='utf-8',sep=';')

## 3.2. DISTINCT IDENTIFIED ROCK ARTISTS AND ROCK ARTIST MEMBERS
identified_rock_artists_temp = df_rock_artist_tags['rock_artist_tags'] + df_rock_artist_tags['members_tags']
identified_rock_artists_temp = list(set([i for i in identified_rock_artists_temp.explode() if pd.isnull(i) == False]))
identified_rock_artists_temp = [tpp.remove_punctuation(i.lower()) for i in identified_rock_artists_temp]
identified_rock_artists = pd.DataFrame(identified_rock_artists_temp).rename(columns={0: "rock_artist"})
identified_rock_artists.to_csv(f'{path_data_support_files}/support_identified_rock_artists.csv', header=True, index=False, encoding='utf-8',sep=';')
print("...it has been completed sucessfully in %0.1fs." % (time() - t_start))
