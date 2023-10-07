"""
Rock News NLP: Topic Modeling Sklearn Prediction
Created on Sun Aug  6 17:51:13 2023
@author: IvoBarros
"""

import os
import os.path
import rock_news_nlp_lda_sklearn as lda_sklearn
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
lda_model = utils_tpp.load_py_object('lda_model', path_output_pickled_obj, 'sklearn_train_lda_model.pickle')
count_vec = utils_tpp.load_py_object('count_vec', path_output_pickled_obj, 'sklearn_train_vectorizer.pickle')

#==============================================================================
# 2. EVALUATE THE MODEL
#==============================================================================
text_corpus_clean, word_freq_count_pred, lda_array, dict_topics = lda_sklearn.topic_prediction(text_corpus, lda_model, count_vec)
lda_sklearn_test_subset_output = lda_sklearn.df_output(lda_array, dict_topics)
lda_sklearn_test_subset_output.insert(0,'title',text_corpus)
lda_sklearn_test_subset_output.to_csv(f'{path_output_csv}/rock_news_nlp_lda_sklearn_test_subset_output.csv', header=True, index=False, encoding='utf-8',sep=';')
model_perplexity = lda_model.perplexity(word_freq_count_pred)
log_likelihood_score = lda_model.score(word_freq_count_pred)
utils_tpp.print_lda_model_topics_stats(dict_topics,model_perplexity,log_likelihood_score)
print("...it has been completed sucessfully in %0.1fs." % (time() - t_start))

 
# """
# # https://gist.github.com/ululh/c3edda2497b8ff9d4f70e63b0c9bd78c
# """

# lst = ['Metallica are touring Europe this summer', 
#         'Slash has confirmed a new GNR album',
#         'A new drummer joined Foo Fighters',
#         "New rock bands don't succeed as in the past"]


# clean_lst = tpp.text_preprocessing_to_sklearn(lst)
# vec_data = count_vec.transform(clean_lst)
# predict = lda_model.transform(vec_data)


#     def topic_prediction(unseen_text_corpus, lda_model, word_freq_count):
#         """
#         To predict topics on unseen text corpus
        
#         Args:
#             unseen_text_corpus : list
#             lda_model : decomposition._lda.LatentDirichletAllocation
#             word_freq_count : sparce.csr.csr_matrix
        
#     	Returns:
#     		Array of float64, list
#         """
#         text_corpus_clean = tpp.text_preprocessing_to_sklearn(unseen_text_corpus)    
#         text_corpus_clean = word_freq_count.transform(text_corpus_clean)
#         topic_probability_scores = lda_model.transform(text_corpus_clean)
#         top_words = [[word_freq_count.get_feature_names()[i] for i in j.argsort()[-5:][::-1]] for i, j in enumerate(lda_model.components_)]    
#         return topic_probability_scores, top_words