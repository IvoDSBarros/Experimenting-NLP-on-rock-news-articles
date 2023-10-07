"""
Rock News NLP: Utilities
Created on Sun Jun 25 17:09:49 2023
@author: IvoBarros
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split 
import os
import os.path

path_parent_dir = os.path.dirname(os.getcwd())
path_data_web_scrapers = f'{path_parent_dir}\data\web_scrapers'
path_data_data_subsets = f'{path_parent_dir}\data\data_subsets'

def return_empty_list_from_nan(df,df_column_list):
    """
    To replace NaN values with an empty list across a dataframe
    Approach proposed on Stack Overflow (question: 33199193; user: PlasmaBinturong)

    Args:
        df : DataFrame
        df_column_list : list
    
	Returns:
		list
	"""  
    for i in df_column_list:
        isnull_flag = df[i].isnull()
        df.loc[isnull_flag, i] = pd.Series([[]] * isnull_flag.sum()).values

def replace_list_empty_string(df,df_column_list):
    """
    To replace list with an empty string by an empty list across a dataframe

    Args:
        df : DataFrame
        df_column_list : list
		
	Returns:
		list
	"""
    for i in df_column_list:
        df[i] = df[i].apply(lambda j: [] if len(j)>0 and j[0]=='' else j)
        
def remove_dups_sort_lists(df,df_column_list):
    """
    To remove duplicates and sort lists across dataframe columns

    Args:
        df : DataFrame
        df_column_list : list
    
	Returns:
		list
	"""
    for i in df_column_list:
        df[i] = df[i].map(lambda j: sorted(set(j)))
        
def load_text_corpus(file_path,file_name,sep,converter,col_name):
    """
    To read tabular data in CSV format and convert a column of texts into a 
    list

    Args:
        file_path : str
        file_name : str
        sep : str
        converter : dictionary
        col_name : str
    
	Returns:
		dataframe
    """
    df_temp = pd.read_csv(f'{file_path}/{file_name}',sep=sep,converters=converter)
    df_temp = df_temp.loc[:, [col_name]]
    return df_temp[col_name].to_list()

def save_py_object(py_object, path, py_object_file_name):
    """
    To save a Python object to file
    
    Args:
        lda_object : obj
        lda_object_file_name : str
    
    Returns:
     	Write the pickled representation of the object obj to the open file 
        object file
    """  
    return pickle.dump(py_object, open(f'{path}/{py_object_file_name}', "wb"))

def load_py_object(py_object, path, py_object_file_name):
    """
    To load a Python object
    
    Args:
        lda_object : obj
        lda_object_file_name : str
    
    Returns:
     	decomposition._lda.LatentDirichletAllocation
    """
    with open(f'{path}/{py_object_file_name}', 'rb') as py_object:
        py_object_name = pickle.load(py_object)    
    return py_object_name 

def split_train_test(dataset, strat_field_name):
    """
    To create random train and test subsets

    Args:
        dataset : *arrays
        strat_field_name : str
    
    Returns:
     	list, length=2 * len(arrays) 
    """
    train, test = train_test_split(dataset, test_size=0.2, random_state=42, shuffle=True,stratify=dataset[strat_field_name])
    return train, test

def print_lda_model_topics_stats(dict_topics,perplexity,lda_model_specific_stat):
    """
    To display the 5 most relevant words per topic of an lda model and its
    performance stats
    
    Args:
        dict_topics : dict
        perplexity : float64
        lda_model_specific_stat : float64
        
 	Returns:
		Displays a formatted message on the topics and performance stats 
        of an LDA model 
    """
    str_topics = ""  
    for k, v in dict_topics.items():
        str_topics = f"{str_topics}{str(k)}: {str(v)}\n"
    return print('-'*60,'\n\n# Topics: Top 5 words',f"""\n{str_topics}""",
                 '\n# Performance metrics\nPerplexity =',round(perplexity,1), 
                 '\nLda model specific stat =',round(lda_model_specific_stat,1),f"""\n\n{'-'*60}""")

def main():
    df_rock_news = pd.read_csv(f'{path_data_web_scrapers}/rock_news.csv',sep=';')
    dataset = df_rock_news.iloc[0:20000,np.r_[0:2,-1]].copy()
    rock_news_train_set, rock_news_test_set = split_train_test(dataset, 'website')
    # rock_news_train_set.to_csv(f'{path_data_data_subsets}/rock_news_train_set.csv', header=True, index=False, encoding='utf-8',sep=';')
    # rock_news_test_set.to_csv(f'{path_data_data_subsets}/rock_news_test_set.csv', header=True, index=False, encoding='utf-8',sep=';')
    
if __name__ == "__main__":
    main()
