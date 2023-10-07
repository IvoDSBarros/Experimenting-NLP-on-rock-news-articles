"""
Rock News NLP: LDA Sklearn
Created on Sun Jul 2 11:56:31 2023
@author: IvoBarros
"""
 
import pandas as pd
import numpy as np
import os
import os.path
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer 
from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
import pyLDAvis.lda_model
from rock_news_nlp_class_text_preprocessing import text_preprocessing as tpp
import rock_news_nlp_utilities as utils_tpp
 
path_parent_dir = os.path.dirname(os.getcwd())
path_data_data_subsets = f'{path_parent_dir}\\data\\data_subsets'
path_output = f'{path_parent_dir}\\output'
path_output_pickled_obj = f'{path_output}\\pickled_objects'
path_output_viz = f'{path_output}\\visuals'

dict_grid_search = {'n_components': [5,6,7], 'learning_decay': [.5,.7,.9], 'learning_method': ['online'], 
                    'max_iter': [150], 'n_jobs': [1], 'random_state': [0]}

def pipeline(text_corpus, *args, **kwargs):
    """
    To apply a list of transforms namely the vectorizer and the tfidf transformer
    
    Args:
        text_corpus : list
        analyzer : str
        min_df : float in range [0.0, 1.0] or int
        ngram_range : tuple
        
    Returns:
        sparce.csr.csr_matrix
    """
    return Pipeline([('count', CountVectorizer(*args, **kwargs)),
                      ('tfid', TfidfTransformer())]).fit(text_corpus)
    
def lda(n_components, learning_method, learning_decay, max_iter, random_state):
    """
    To perform the Latent Dirichlet Allocation statistical model
    
    Args:
        n_components : int
        learning_method : str
        learning_decay : float
        max_iter : int
        random_state : int
        
    Returns:
        decomposition._lda.LatentDirichletAllocation
    """
    return LDA(
                n_components=n_components, 
                learning_method=learning_method,
                learning_decay=learning_decay,
                max_iter=max_iter,
                n_jobs=1,
                random_state=random_state
                )

def topics(lda, counts):
    """
    To get the most relevant words per topic 
    
    Args:
        lda : decomposition._lda.LatentDirichletAllocation
        counts : sparce.csr.csr_matrix
        
    Returns:
        dict
    """
    topic_id = [i for i in range(lda.n_components)]
    top_words = [[counts.get_feature_names_out()[i] for i in j.argsort()[-5:][::-1]] for i, j in enumerate(lda.components_)]
    return dict(zip(topic_id, top_words))
    
def df_output(lda_array, dict_topics):
    """
    To get the most relevant topics per text of the corpus
    
    Args:
        text_corpus : list
        lda_array : Array of float64
        dict_topics : dict
    
    Returns:
        DataFrame
    """
    df_lda_output = pd.DataFrame(np.round(lda_array, 2))
    df_lda_output['main_topic'] = np.argmax(df_lda_output.values, axis=1)
    df_lda_output = df_lda_output.rename(columns= {i: "topic_" + str(i) for i in df_lda_output.select_dtypes([np.float64]).columns})
    df_lda_output['main_topic_%'] = df_lda_output.iloc[:,0:len(df_lda_output.columns)-1].max(axis=1)
    df_lda_output['main_topic_words'] = df_lda_output['main_topic'].map(dict_topics)
    return df_lda_output
    
def grid_search(dict_grid_search, word_freq_count):
    """
    To search optimal hyperparameters
    
    Args:
        dict_grid_search : dict
        word_freq_count : sparce.csr.csr_matrix
    
    Returns:
        model_selection._search.GridSearchCV
    """
    lda = LDA()
    gs_model = GridSearchCV(lda, param_grid=dict_grid_search)
    gs_model.fit(word_freq_count)
    return gs_model

def topic_prediction(unseen_text_corpus, lda_model, word_freq_count):
    """
    To predict topics on unseen text corpus
    
    Args:
        unseen_text_corpus : list
        lda_model : decomposition._lda.LatentDirichletAllocation
        word_freq_count : sparce.csr.csr_matrix
    
    Returns:
        Array of float64, list
    """
    text_corpus_clean = tpp.text_preprocessing_to_sklearn(unseen_text_corpus)    
    word_freq_count_pred = word_freq_count.transform(text_corpus_clean)
    lda_array = lda_model.transform(word_freq_count_pred)
    dict_topics = topics(lda_model, word_freq_count)
    return text_corpus_clean, word_freq_count_pred, lda_array, dict_topics 

def model_viz(text_corpus, lda_model, vectorizer, path, filename):
    """
    To bring out a visual overview of the lda model
    
    Args:
        text_corpus : list
        lda_model : decomposition._lda.LatentDirichletAllocation
        vectorizer : sparce.csr.csr_matrix
        word_freq_count : sparce.csr.csr_matrix
        path : str
        filename : str
        
    Returns:
        Save an embedded visualization to file
    """
    lda_visual = pyLDAvis.lda_model.prepare(
                                            lda_model, 
                                            vectorizer.fit_transform(text_corpus),
                                            vectorizer, 
                                            mds='tsne'
                                            )   
    pyLDAvis.display(lda_visual)
    return pyLDAvis.save_html(lda_visual, f'{path}/{filename}.html')

def main():
    global path_data_web_scrapers, path_output, dict_grid_search
     
    text_corpus = utils_tpp.load_text_corpus(path_data_data_subsets, 'rock_news_train_set.csv', ';', None, 'title')
    text_corpus_clean = tpp.text_preprocessing_to_sklearn(text_corpus)
    pipe = pipeline(text_corpus_clean,analyzer='word', min_df=10, ngram_range=(1, 2))
    x_counts = pipe['count'].transform(text_corpus_clean)
    gs_model = grid_search(dict_grid_search,x_counts)
    best_lda_model = gs_model.best_estimator_
    model_perplexity = best_lda_model.perplexity(x_counts)
    best_log_likelihood_score = gs_model.best_score_
    topics_lda = topics(best_lda_model, pipe['count'])
    # utils_tpp.save_py_object(best_lda_model, path_output_pickled_obj, 'sklearn_train_lda_model.pickle')
    # utils_tpp.save_py_object(pipe['count'], path_output_pickled_obj, 'sklearn_train_vectorizer.pickle')
    # model_viz(text_corpus_clean, best_lda_model, pipe['count'], path_output_viz, 'sklearn_train_lda_model_viz')
    utils_tpp.print_lda_model_topics_stats(topics_lda,model_perplexity,best_log_likelihood_score)

if __name__ == "__main__":
    main()
