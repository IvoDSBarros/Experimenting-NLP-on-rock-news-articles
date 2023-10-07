"""
Rock News NLP: Rule-based text classification
Created on Sun May 22 17:27:11 2022
@author: IvoBarros
"""

import pandas as pd
import numpy as np
import os
import os.path
from time import time
from rock_news_nlp_class_text_preprocessing import text_preprocessing as tpp
import rock_news_nlp_utilities as utils_tpp

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
df_dict_category = pd.read_csv(f'{path_data_support_files}/support_text_class_news_category_dict.csv',sep=';')
df_add_keywords = pd.read_csv(f'{path_data_support_files}/support_text_class_news_category_add_keywords.csv',sep=';')

## 1.2. PREPARATORY TEXT PREPROCESSING 
## CONVERT THE ROCK NEWS HEADLINES INTO A LIST
df_rock_news_subset = df_rock_news.iloc[0:20000,np.r_[-1,1]].copy()
corpus_title = df_rock_news_subset['title'].to_list()
corpus_title = tpp.text_preprocessing_rule_based_txt_class_prep(corpus_title)

## CREATE EXCEPTIONAL KEY WORD FLAGS ON THE TYPE OF PUBLICATION BEFORE REMOVING STOP WORDS & PUNCTUATION
type_publication = {'story': [], 'musical list': [], 'recall event': [], 'opinion': [],
                    'reaction': [], 'video/audio': [], 'poll/tourney': [], 'birthday reminder': []}
set_is_story = set(['how ','musicians ','why ','who is ','who are ','when ','what ','this ',"here's ",'that time ','opinion |', 'odd couples: '])

type_publication['story'].extend([1 if (i.startswith(tuple([j for j in set_is_story]))) else 0 for i in corpus_title])
type_publication['musical list'].extend([1 if ((((i[:1].isdigit() and i[2]==" ") or (i[0].isdigit() and i[1]==" ")) 
                                              and set([":","-"]).intersection(i.split())==False)
                                              or "best rock + metal songs" in i or "rock + metal bands" in i) else 0 for i in corpus_title])
type_publication['recall event'].extend([1 if "years ago:" in i or "years ago -" in i else 0 for i in corpus_title])
type_publication['birthday reminder'].extend([1 if tpp.word_search('birthdays', i)==True 
                                              and tpp.word_search('celebrating', i)==True else 0 for i in corpus_title])

## 1.3. CORE TEXT PREPROCESSING TASKS
corpus_title_clean = tpp.text_preprocessing_rule_based_txt_class(corpus_title)

#==============================================================================
# 2. TEXT CLASSIFICATION
#==============================================================================

## 2.1. TYPE OF PUBLICATION TAGS
## 2.1.1. REMAINING KEY WORD FLAGS
set_verbs_opinion = set(['reflect','think','say','explain','admit'])
set_verbs_reaction = set(['react','respond'])

type_publication['opinion'].extend([1 if [i for i in set_verbs_opinion if tpp.word_search(i,j)==True] else 0 for j in corpus_title_clean])
type_publication['reaction'].extend([1 if [i for i in set_verbs_reaction if tpp.word_search(i,j)==True] else 0 for j in corpus_title_clean])
type_publication['video/audio'].extend([1 if ([i for i in set(['watch','video']) if tpp.word_search(i,j)==True] or 
                                              j.startswith(tuple([i for i in set(['see ','listen ','hear '])]))) else 0 for j in corpus_title_clean])
type_publication['poll/tourney'].extend([1 if tpp.word_search('poll', i)==True or tpp.word_search('rrhof tourney', i)==True else 0 for i in corpus_title_clean])

df_type_publication_prep = pd.DataFrame(type_publication)
df_type_publication_prep['index_1'] = df_type_publication_prep.index
df_type_publication_prep = pd.melt(df_type_publication_prep, id_vars=['index_1'], var_name = "type_publication", value_name = "count")                                                  
df_type_publication_prep = df_type_publication_prep[(df_type_publication_prep['count']>0)]
df_type_publication = df_type_publication_prep[['index_1','type_publication']].groupby('index_1').agg(pd.Series.tolist)

## 2.2. NEWS ARTICLE TOPIC LABELS
## 2.2.1 CREATE SUPPORT DICTIONARIES AND SETS
df_dict_category['keyword_stem'] = df_dict_category['keyword'].apply(lambda i: ''.join(tpp.stem_word(tpp.token(i))))
set_category_tags = set(df_dict_category['keyword_stem']) 
dict_stem_keywords = df_dict_category.groupby('keyword_stem')['keyword'].agg('first').to_dict()
dict_sub_category_tag_all = df_dict_category[df_dict_category['bool_type']=='all'].groupby('sub_category')['keyword_stem'].agg(set).to_dict()
dict_sub_category_tag_any = df_dict_category[df_dict_category['bool_type']=='any'].groupby('sub_category')['keyword_stem'].agg(set).to_dict()
dict_category_tag = df_dict_category.groupby('sub_category')['category'].agg('first').to_dict()

## 2.2.2. RETURN KEYWORDS AND SUBCATEGORY TOPIC LABELS
sub_category_tags = {'keywords': [], 'sub_category_tags': []}
sub_category_tags['keywords'].extend([[i for i in set_category_tags if tpp.word_search(i,j)==True] for j in corpus_title_clean])
sub_category_tag_all = [[k for k in dict_sub_category_tag_all.keys() if all(i in j for i in dict_sub_category_tag_all[k])] for j in sub_category_tags['keywords']]
sub_category_tag_any = [[k for k in dict_sub_category_tag_any.keys() if any(i in j for i in dict_sub_category_tag_any[k])] for j in sub_category_tags['keywords']]
sub_category_tags['sub_category_tags'].extend([list(i + j) for i, j in zip(sub_category_tag_all, sub_category_tag_any)])
df_sub_category_tags = pd.DataFrame(sub_category_tags)

## 2.2.3. RETURN CATEGORY TOPIC LABELS
keywords_exploded = df_sub_category_tags['keywords'].to_frame().explode('keywords')
keywords_exploded['index_1'] = keywords_exploded.index
sub_category_tags_exploded = df_sub_category_tags['sub_category_tags'].to_frame().explode('sub_category_tags')
sub_category_tags_exploded['index_1'] = sub_category_tags_exploded.index

df_category_tags_prep = keywords_exploded.merge(sub_category_tags_exploded,how="outer",on='index_1')
df_category_tags_prep['keywords'] = df_category_tags_prep['keywords'].map(dict_stem_keywords)
df_category_tags_prep['category_tags'] = df_category_tags_prep['sub_category_tags'].map(dict_category_tag)
df_category_tags_prep = df_category_tags_prep.dropna(subset=['keywords', 'sub_category_tags', 'category_tags'])
df_category_tags_prep = df_category_tags_prep[~(df_category_tags_prep["keywords"].str.contains("new"))]
df_category_tags_prep = df_category_tags_prep.groupby('index_1').agg(pd.Series.tolist)
df_category_tags_prep = df_rock_news_subset.join([df_category_tags_prep,df_type_publication])

utils_tpp.return_empty_list_from_nan(df_category_tags_prep,['keywords','sub_category_tags','category_tags','type_publication'])
utils_tpp.remove_dups_sort_lists(df_category_tags_prep,['keywords','sub_category_tags','category_tags','type_publication'])

df_category_tags_prep['sub_category_tags'] = df_category_tags_prep['sub_category_tags'].apply(lambda j: ['diverse topics'] if bool(j)==False else j)
df_category_tags_prep['category_tags'] = df_category_tags_prep['category_tags'].apply(lambda j: ['diverse topics'] if bool(j)==False else j)
df_category_tags_prep['type_publication'] = df_category_tags_prep['type_publication'].apply(lambda j: ['general'] if bool(j)==False else j)
df_rock_news_category_tags = df_category_tags_prep.drop('title', axis=1)

#==============================================================================
# 3. SAVE DATA AS CSV FILE
#==============================================================================

df_rock_news_category_tags.to_csv(f'{path_output_csv}/rock_news_nlp_rock_news_category_tags.csv', header=True, index=False, encoding='utf-8',sep=';')
print("...it has been completed sucessfully in %0.1fs." % (time() - t_start))
