"""
Rock News NLP: Dictionary-based Named Entity Recognition
Created on Sun Jun 25 15:56:58 2023
@author: IvoBarros
"""

"""
Goals

The purpose of this script is identifying and extracting rock artist/rock artist
member names from a text corpus comprised by rock news headlines and descriptions 
with no labeled data. With this end in view a dictionary-based named entity 
recognition (NER) approach has been implemented. The pre-built dictionary is 
made up of data from multiple wikipedia lists on rock, metal and punk bands 
gathered by a web scraper.   

*******************************************************************************

Challenges

1. Single/multiple rock artist name(s) and/or single/multiple rock artist member
name(s) might be mentioned in a news headline and/or news description. Hence the
text of the headline and the text of the description were combined to perform
the search of the rock artist and rock artist member. Additionally, only whole
words/compound words should be matched to avoid wrong labelling. On the other
hand, the pre-built dictianaries of rock artists/rock artists member names
contain 38 663 records. Given this particular context and taking into account
that the end goal is assigning lists of identified rock artist/rock artist
member names per every single text of the corpus, performance has become a
critical issue. Several methods were evaluated including vectorization,
flashtext, regex and a whole word search approcah proposed on Stack Overflow
(question 5319922, user200783). The last one, when combined with a previous text
preprocessing by removing special characters and a set of rock artists/rock
artists member names, has proved to be the fastest and most effective.

2. Acronyms are used to mention some rock artists (A7X, RHCP, RATM, GN'R) and
the definite article "The" is sometimes excluded to mention artists whose name 
starts with "The" (a stop word removal approach would perfectly work out for 
bands like The Beatles or The Rolling Stones but it is not the case for bands 
such as The Who - it would be completely removed as "The" and "Who" are both 
stop words - or The Doors - "Doors" would be matching both The Doors and Three 
Doors Down news articles afterwards). Moreover, popular songs or albums are
often mentioned with no reference to the rock artist across the headlines and 
the descriptions. Some misspellings were identified on the rock artist names 
through the headlines.            

3. The words of the news headlines from the websites Loudwire and Ultimate 
Classic Rock start with capital letter.

4. Bands like "Yes", "HIM", "Sweet" or "The Band" lead to misleading labelling
so additional text preprocessing actions were required.
"""

"""
REFURB ALL SCRIPTS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

import pandas as pd
import numpy as np
import os
import os.path
from rock_news_nlp_class_text_preprocessing import text_preprocessing as tpp
import rock_news_nlp_utilities as utils_tpp
from datetime import datetime

time_1 = datetime.now()

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


#==============================================================================
# 1. TEXT PREPROCESSING
#==============================================================================

### 1.1. LOAD DATA
path_parent_dir = os.path.dirname(os.getcwd())
path_data = path_parent_dir + '\data'
path_data_web_scrapers = path_data + '\web_scrapers'
path_data_support_files = path_data + '\support_files'
path_output_csv = path_parent_dir + '\output\csv'

df_rock_news = pd.read_csv(f'{path_data_web_scrapers}/rock_news.csv',sep=';')
df_rock_artist_md = pd.read_csv(f'{path_data_web_scrapers}/rock_artist_masterdata.csv',sep=';')
df_rock_artist_members = pd.read_csv(f'{path_data_web_scrapers}/rock_artist_members.csv',sep=';')
df_dict_text_clean_support = pd.read_csv(f'{path_data_support_files}/support_dict_rock_artist_text_clean.csv',sep=';')

### 1.2. CREATE SUPPORT DICTIONARIES FROM THE ROCK ARTIST REFERENCE TABLES
### ROCK ARTIST DICTIONARIES & SET
df_rock_artist_md = df_rock_artist_md[~df_rock_artist_md['Rock_Artist'].isin(['The Band',"Sweet","!!!"])]
list_rock_artist_clean = dfcol_to_list(df_rock_artist_md,'Rock_Artist')
dict_rock_artist = dict(zip([tpp.replace_keywords(i, {'yesband': ['yes']}) for i in list_rock_artist_clean], df_rock_artist_md['Rock_Artist'].to_list()))
set_rock_artist = set(dict_rock_artist.keys())
### ROCK ARTIST ADDITIONAL SET
set_rock_artist_additional = set([i[4:len(i)] for i in list_rock_artist_clean if (i.startswith('the ') and 
                                  i !='the new year' and len((i).split(' '))>=3) or i=='the beatles'])
### ROCK ARTIST MEMBER SET & DICTIONARY
list_members_clean = dfcol_to_list(df_rock_artist_members,'Description')
dict_rock_artist_members = dict(zip(list_members_clean, df_rock_artist_members[['Description','Rock_Artist']].values.tolist()))
set_rock_artist_members = set(dict_rock_artist_members.keys())

### 1.3. JOIN THE ROCK NEWS HEADLINES AND DESCRIPTIONS AND CONVERT THE TEXT CORPUS INTO A LIST
df_rock_news['Title_Desc'] = df_rock_news['Title'] + ' ' + df_rock_news['Description']
df_rock_news_subset = df_rock_news.iloc[:,np.r_[-2,-1]].copy()
corpus_title_desc = df_rock_news_subset['Title_Desc'].to_list()

### 1.4. TEXT PREPROCESSING TASKS
corpus_title_desc_clean = text_preprocessing(corpus_title_desc)
### ADDITIONAL TEXT PREPROCESSING TASKS 
keyword_dict = df_dict_text_clean_support.groupby('Values')['Key'].agg(list).to_dict()
corpus_title_desc_clean = [tpp.replace_keywords(i, keyword_dict) for i in corpus_title_desc_clean]


#==============================================================================
# 2. IDENTIFY AND EXTRACT THE ROCK ARTIST AND THE ROCK ARTIST MEMBER
#==============================================================================

### 2.1. ROCK ARTIST AND ROCK ARTIST MEMBER SEARCH ON THE TEXT CORPUS AND EXTRACTION 
extracted_rock_artists = {'Title_Desc_Clean': [], 'Rock_Artist_Tags_Prep': [], 'Members_Tags': []}
extracted_rock_artists['Title_Desc_Clean'].extend(corpus_title_desc_clean)
extracted_rock_artists['Rock_Artist_Tags_Prep'].extend([[i for i in set_rock_artist if tpp.word_search(i,j)==True] for j in corpus_title_desc_clean])
extracted_rock_artists['Members_Tags'].extend([[i for i in set_rock_artist_members if tpp.word_search(i,j)==True] for j in corpus_title_desc_clean])
df_rock_artist_tags_prep = pd.DataFrame(extracted_rock_artists)
df_temp_tags_null = df_rock_artist_tags_prep['Title_Desc_Clean'][df_rock_artist_tags_prep['Rock_Artist_Tags_Prep'].str.len() == 0].to_frame()
df_temp_tags_null['Rock_Artist_Tags_Add'] = df_temp_tags_null['Title_Desc_Clean'].apply(lambda x: [f'the {i}' for i in set_rock_artist_additional if tpp.word_search(i,x)==True])
df_temp_tags_null = df_temp_tags_null.iloc[:,np.r_[-1]].copy()
df_rock_artist_tags_prep = df_rock_artist_tags_prep.join(df_temp_tags_null)
utils_tpp.return_empty_list_from_nan(df_rock_artist_tags_prep,['Rock_Artist_Tags_Add'])

### 2.2. RETURN THE BANDS OF THE IDENTIFIED MEMBERS AND REVISE PREVIOUSLY MANIPULATED ROCK ARTISTS NAMES
for i in ['Rock_Artist_Tags_Prep','Rock_Artist_Tags_Add','Members_Tags']:
    globals()[f'{i.lower()}_exploded'] = df_rock_artist_tags_prep[f'{i}'][df_rock_artist_tags_prep[f'{i}'].str.len()>0].copy()
    globals()[f'{i.lower()}_exploded'] = globals()[f'{i.lower()}_exploded'].to_frame().explode(i)
    globals()[f'{i.lower()}_exploded']['Index1'] = globals()[f'{i.lower()}_exploded'].index

df_members_temp = rock_artist_tags_prep_exploded.merge(rock_artist_tags_add_exploded,how="outer",on='Index1').merge(members_tags_exploded,how="outer",on='Index1') 
df_members_temp['Rock_Artist_Tags_Prep'] = df_members_temp['Rock_Artist_Tags_Prep'].map(dict_rock_artist)
df_members_temp['Rock_Artist_Tags_Add'] = df_members_temp['Rock_Artist_Tags_Add'].map(dict_rock_artist)
df_members_temp['Tags_Rock_Artist_From_Member_Tags'] = df_members_temp['Members_Tags'].map(dict_rock_artist_members).str[1]
df_members_temp['Members_Tags'] = df_members_temp['Members_Tags'].map(dict_rock_artist_members).str[0]
df_members_temp = df_members_temp.dropna(subset=df_members_temp.columns.difference(['Index1']),how='all')
df_members_temp = df_members_temp.fillna('')
df_members_temp[df_members_temp.columns.difference(['Index1'])].astype(str)
df_members_temp = df_members_temp.groupby('Index1').agg(pd.Series.tolist)
df_rock_artist_tags = df_rock_news_subset.iloc[:,0].to_frame().join(df_members_temp)
utils_tpp.return_empty_list_from_nan(df_rock_artist_tags,['Rock_Artist_Tags_Prep','Rock_Artist_Tags_Add','Tags_Rock_Artist_From_Member_Tags','Members_Tags'])
utils_tpp.replace_list_empty_string(df_rock_artist_tags,['Rock_Artist_Tags_Prep','Rock_Artist_Tags_Add','Tags_Rock_Artist_From_Member_Tags','Members_Tags'])
df_rock_artist_tags['Rock_Artist_Tags'] = df_rock_artist_tags['Rock_Artist_Tags_Prep'] + df_rock_artist_tags['Rock_Artist_Tags_Add'] + df_rock_artist_tags['Tags_Rock_Artist_From_Member_Tags']
utils_tpp.remove_dups_sort_lists(df_rock_artist_tags,['Rock_Artist_Tags','Members_Tags'])


#==============================================================================
# 3. SAVE DATA AS CSV FILE
#==============================================================================

### 3.1. IDENTIFIED ROCK ARTISTS AND ROCK ARTIST MEMBERS PER TEXT
df_rock_artist_tags = df_rock_artist_tags.iloc[:,np.r_[0,-1,-3]]
df_rock_artist_tags.to_csv(f'{path_output_csv}/rock_news_nlp_rock_artist_tags.csv', header=True, index=False, encoding='utf-8',sep=';')

### 3.2. DISTINCT IDENTIFIED ROCK ARTISTS AND ROCK ARTIST MEMBERS
identified_rock_artists_temp = df_rock_artist_tags['Rock_Artist_Tags'] + df_rock_artist_tags['Members_Tags']
identified_rock_artists_temp = list(set([i for i in identified_rock_artists_temp.explode() if pd.isnull(i) == False]))
identified_rock_artists_temp = [tpp.remove_punctuation(i.lower()) for i in identified_rock_artists_temp]
identified_rock_artists = pd.DataFrame(identified_rock_artists_temp).rename(columns={0: "Rock_Artist"})
identified_rock_artists.to_csv(f'{path_data_support_files}/support_identified_rock_artists.csv', header=True, index=False, encoding='utf-8',sep=';')

time_2 = datetime.now()
runtime_seconds = (time_2 - time_1).total_seconds()
print('This job has run sucessfully in ' + str(round(runtime_seconds,1)) + " seconds.")


###############################################################################


# test_01 = df_rock_news[df_rock_news["Title"].str.contains("HIM")]
# test_02 = df_rock_artist_tags[df_rock_artist_tags['Rock_Artist_Tags_Prep'].apply(lambda x: "yes" in x)]
# test_03 = df_rock_artist_members[df_rock_artist_members["Description"].str.contains("Peter Jones")]