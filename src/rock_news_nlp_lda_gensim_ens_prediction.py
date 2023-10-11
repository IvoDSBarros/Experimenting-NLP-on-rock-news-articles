"""
Rock News NLP: Topic Modelling LDA Gensim Ensemble Prediction
Created on Sun Aug  6 19:37:55 2023
@author: IvoBarros
"""

import os
import os.path
import rock_news_nlp_lda_gensim_ens as lda_gens
from rock_news_nlp_class_text_preprocessing import text_preprocessing as tpp
import rock_news_nlp_utilities as utils_tpp
from time import time

print("The script is running...")
t_start = time()

#==============================================================================
# 1. LOAD DATA AND THE PICKLED OBJECTS
#==============================================================================
path_parent_dir = os.path.dirname(os.getcwd())
path_data_data_subsets = f'{path_parent_dir}\\data\\data_subsets'
path_output = f'{path_parent_dir}\\output'
path_output_pickled_obj = f'{path_output}\\pickled_objects'
path_output_csv = f'{path_output}\\csv'

text_corpus = utils_tpp.load_text_corpus(path_data_data_subsets, 'rock_news_test_set.csv', ';', None, 'title')
dictionary_train = lda_gens.load_dictionary(f'{path_output_pickled_obj}/gensim_ens_train_dict_lda')
ens_lda_train = lda_gens.load_gens_lda_model(path_output_pickled_obj, 'gensim_ens_train_lda_model', 'ens_lda_train')
dict_ens_lda_topics_p = utils_tpp.load_py_object('dict_ens_lda_topics_p', path_output_pickled_obj, 'gensim_ens_train_topics_lda.pickle')
dict_ens_lda_top_5_words = utils_tpp.load_py_object('dict_ens_lda_top_5_words', path_output_pickled_obj, 'gensim_ens_train_topics_top_5_words_lda.pickle')

#==============================================================================
# 2. EVALUATE THE MODEL
#==============================================================================
text_corpus_clean = tpp.text_preprocessing_to_gensim(text_corpus)
corpus, corpus_tfidf = lda_gens.corpus_bow(text_corpus_clean, dictionary_train)
lda_gensim_test_subset_output = lda_gens.df_output(ens_lda_train, dictionary_train, corpus, dict_ens_lda_topics_p, dict_ens_lda_top_5_words)
lda_gensim_test_subset_output.insert(0,'title',text_corpus)
lda_gensim_test_subset_output.to_csv(f'{path_output_csv}/rock_news_nlp_lda_gensim_test_subset_output.csv', header=True, index=False, encoding='utf-8',sep=';')
test_model_perplexity = lda_gens.metric_perplexity(ens_lda_train, corpus)
test_coherence_score = lda_gens.metric_coherence(model=ens_lda_train, texts=text_corpus_clean, dictionary=dictionary_train, coherence='u_mass')
utils_tpp.print_lda_model_topics_stats(dict_ens_lda_top_5_words,test_model_perplexity,test_coherence_score )
print("...it has been successfully executed in %0.1fs." % (time() - t_start))
