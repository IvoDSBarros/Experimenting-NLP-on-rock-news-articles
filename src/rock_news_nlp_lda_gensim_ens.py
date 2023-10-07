"""
Rock News NLP: Topic Modelling LDA Gensim Ensemble
Created on Sun May 29 18:27:15 2023
@author: IvoBarros
"""

import pandas as pd
import numpy as np
import re
import os
import os.path
from gensim import models
import gensim.corpora as corpora
from gensim.corpora import Dictionary
from gensim.models import CoherenceModel
from gensim.models import EnsembleLda
from gensim.models import LdaModel
from gensim.test.utils import datapath
from rock_news_nlp_class_text_preprocessing import text_preprocessing as tpp
import rock_news_nlp_utilities as utils_tpp

path_parent_dir = os.path.dirname(os.getcwd())
path_data_data_subsets = f'{path_parent_dir}\\data\\data_subsets'
path_output = f'{path_parent_dir}\\output'
path_output_pickled_obj = f'{path_output}\\pickled_objects'

num_topics = 20
num_models = 16
ens_workers = 4 
dist_workers = 4
passes = 15
topic_model_class = LdaModel
no_below = 15
no_above = 0.5
keep_n = 100000

def dictionary(text_corpus, *args, **kwargs):
    """
    To create a gensim dictionary and filter its extremes 
    
    Args:
        text_corpus : list
        no_below  : int
        no_above : float
        keep_n : int
        
    Returns:
        corpora.dictionary.Dictionary
    """
    dictionary = corpora.Dictionary(text_corpus)
    dictionary.filter_extremes(*args, **kwargs)
    return dictionary

def save_dictionary(path, dictionary, dictionary_name):
    """
    To save a gensim dictionary to file
    
    Args:
        dictionary : corpora.dictionary.Dictionary
        dictionary_name : str
        
    Returns:
        Write the representation of the gensim dictionary to a file
    """
    temp_file = datapath(f'{path}/{dictionary_name}')
    dictionary.save(temp_file)

def load_dictionary(dictionary_name):
    """
    To load a gensim dictionary from a file
    
    Args:
        dictionary_name : str
        
    Returns:
        corpora.dictionary.Dictionary
    """
    dictionary = Dictionary.load(dictionary_name)
    return dictionary

def corpus_bow(text_corpus,dictionary):
    """
    To create a gensim bag of words corpus
    
    Args:
        text_corpus : list
        dictionary : corpora.dictionary.Dictionary
        
    Returns:
        list, interfaces.TransformedCorpus
    """
    corpus = [dictionary.doc2bow(i) for i in text_corpus]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    return corpus, corpus_tfidf

def ens_lda_model(corpus, dictionary):
    """
    To perform the Gensim Ensemble Latent Dirichlet Allocation statistical model
    
    Args:
        corpus : list
        dictionary : corpora.dictionary.Dictionary
        num_topics : int
        num_models : int
        ens_workers : int 
        dist_workers : int
        passes : int
        topic_model_class : str
        
    Returns:
        models.ensemblelda.EnsembleLda
    """ 
    return EnsembleLda(
                        corpus=corpus, 
                        id2word=dictionary, 
                        num_topics=num_topics, 
                        num_models=num_models,
                        passes=passes,
                        iterations=200,
                        ensemble_workers=ens_workers,
                        distance_workers=dist_workers,
                        topic_model_class=topic_model_class,                    
                        random_state=0
                        )
    
def topics_ens_lda(ens_lda_model):
    """
    To get the most relevant words per topic 
    
    Args:
        ens_lda_model : models.ensemblelda.EnsembleLda
        
    Returns:
	dict
    """
    dict_ens_lda_topics_p = dict(ens_lda_model.print_topics())
    dict_ens_lda_top_5_words = {i: re.sub('[^A-Za-z ]+', ' ', x).split() for i, x in ens_lda_model.print_topics(num_words=5)}
    return dict_ens_lda_topics_p, dict_ens_lda_top_5_words
    
def df_output(ens_lda_model, dictionary, text_corpus, dict_ens_lda_topics_p, dict_ens_lda_top_5_words):
    """
    To get the most relevant topics per text of the corpus
    
    Args:
        ens_lda_model : models.ensemblelda.EnsembleLda
        dictionary : corpora.dictionary.Dictionary
        text_corpus : list
        dict_ens_lda_topics_p : dict
        dict_ens_lda_top_5_words : dict
        
    Returns:
    	DataFrame
    """
    list_ens_lda_prob = [[j[1] for j in i] for i in ens_lda_model[text_corpus]]
    df_ens_lda_output = pd.DataFrame(list_ens_lda_prob)
    df_ens_lda_output['main_topic'] = np.argmax(df_ens_lda_output.values, axis=1)
    df_ens_lda_output['main_topic_%'] = df_ens_lda_output.iloc[:,0:len(df_ens_lda_output.columns)-1].max(axis=1)
    df_ens_lda_output['main_topic_top_5_words'] = df_ens_lda_output['main_topic'].map(dict_ens_lda_top_5_words)
    df_ens_lda_output['main_topic_words_p'] = df_ens_lda_output['main_topic'].map(dict_ens_lda_topics_p)
    df_ens_lda_output = df_ens_lda_output.rename(columns= {i: "topic_" + str(i) for i in df_ens_lda_output.columns if str(i).isdigit()==True})
    return df_ens_lda_output.round(2)

def save_gens_lda_model(path, lda_object, lda_object_file_name):
    """
    To save a gensim lda model to file
    
    Args:
        lda_object : models.ensemblelda.EnsembleLda
        lda_object_file_name : str
    
    Returns:
    	Write the representation of the object to a file
    """
    temp_file = datapath(f'{path}/{lda_object_file_name}')
    lda_object.save(temp_file)

def load_gens_lda_model(path, lda_object_file_name, lda_object_name):
    """
    To load the gensim ensemble lda object
    
    Args:
        lda_object : obj
        lda_object_file_name : str
    
    Returns:
    	models.ensemblelda.EnsembleLda
    """ 
    temp_file = datapath(f'{path}/{lda_object_file_name}')
    lda_object_name = EnsembleLda.load(temp_file)
    return lda_object_name

def metric_perplexity(lda_model, text_corpus):
    """
    To compute the perplexity of the LDA model
    
    Args:
        lda_model : models.ensemblelda.EnsembleLda
        text_corpus : list
    
    Returns:
    	float64
    """ 
    return np.exp2(-lda_model.log_perplexity(text_corpus))

def metric_coherence(*args, **kwargs):
    """
    To compute the coherence score of the LDA model
    
    Args:
        model : models.ensemblelda.EnsembleLda
        texts : list
        dictionary : corpora.dictionary.Dictionary
        
    Returns:
    	float64
    """ 
    coherence_model_ens_lda = CoherenceModel(*args, **kwargs)
    return coherence_model_ens_lda.get_coherence()

def main():
    global num_topics
    global num_models
    global ens_workers
    global dist_workers
    global passes
    global topic_model_class
    global no_below
    global no_above
    global keep_n
    global path_data_web_scrapers 
    global path_output

    text_corpus = utils_tpp.load_text_corpus(path_data_data_subsets, 'rock_news_train_set.csv', ';', None, 'title')
    text_corpus_clean = tpp.text_preprocessing_to_gensim(text_corpus)    
    dictionary_lda = dictionary(text_corpus_clean, no_below=no_below, no_above=no_above, keep_n=keep_n)
    # save_dictionary(path_output_pickled_obj, dictionary_lda, 'gensim_ens_train_dict_lda')
    corpus, corpus_tfidf = corpus_bow(text_corpus_clean,dictionary_lda)
    lda_model = ens_lda_model(corpus, dictionary_lda)
    # save_gens_lda_model(path_output_pickled_obj, lda_model, 'gensim_ens_train_lda_model')
    dict_ens_lda_topics_p, dict_ens_lda_top_5_words = topics_ens_lda(lda_model)
    # utils_tpp.save_py_object(dict_ens_lda_topics_p, path_output_pickled_obj, 'gensim_ens_train_topics_lda.pickle')
    # utils_tpp.save_py_object(dict_ens_lda_top_5_words, path_output_pickled_obj, 'gensim_ens_train_topics_top_5_words_lda.pickle')
    model_perplexity = metric_perplexity(lda_model, corpus)
    coherence_score = metric_coherence(model=lda_model, texts=text_corpus_clean, dictionary=dictionary_lda, coherence='u_mass')
    utils_tpp.print_lda_model_topics_stats(dict_ens_lda_top_5_words,model_perplexity,coherence_score )

if __name__ == "__main__":
    main()
