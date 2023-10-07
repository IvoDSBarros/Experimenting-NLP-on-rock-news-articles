"""
Rock News NLP: Text Preprocessing Class
Created on Mon Jun 19 16:50:11 2023
@author: IvoBarros
"""

import pandas as pd
import re
from unidecode import unidecode
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from flashtext import KeywordProcessor
from gensim.models import Phrases
from gensim.models.phrases import Phraser
import os
import os.path

global df_unique_rock_artists, df_dict_category, df_add_keywords

path_parent_dir = os.path.dirname(os.getcwd())
path_data_support_files = f'{path_parent_dir}\data\support_files'
df_unique_rock_artists = pd.read_csv(f'{path_data_support_files}/support_identified_rock_artists.csv',sep=';')
df_dict_category = pd.read_csv(f'{path_data_support_files}/support_text_class_news_category_dict.csv',sep=';')
df_add_keywords = pd.read_csv(f'{path_data_support_files}/support_text_class_news_category_add_keywords.csv',sep=';')

class text_preprocessing:     
    stop_words = set(stopwords.words('english'))
    additional_stop_words = set(['kerrang','2022','2023','rock','roll','metal','years','ago','london','time'])
    dict_keyword = {'releas': ['drop','unleash','share','premier','launch'],
                    'announc': ['unveil','reveal'],
                    'show': ['gig','concert'],
                    'festiv': ['fest'],
                    'song': ['track']}
    dict_synonym_replacement = {'lineup': ['line-up'], 
                                'say': ['said'], 
                                'think': ['thought'], 
                                'rrhof': ['rock hall', 'rock and roll hall of fame', 'roll hall of fame'],
                                'death': ['dead', 'die', 'dies', 'died']}
    set_keyword = set(df_dict_category['keyword']) | set(df_add_keywords['keyword'])
    set_keyword_lda = set(i for i in set_keyword if i!='new')
    set_rock_artist_name = set(df_unique_rock_artists['rock_artist'])  
    keyword_processor = KeywordProcessor(case_sensitive=True)
    ps = PorterStemmer()
       
    def __init__(self, text):
        self.text = text

    def remove_punctuation(self):
        """
        To remove punctuatiom from the text corpus and replace non-ASCII 
        characters within it      
        
        Args:
            text : str         
		
		Returns:
			str
        """
        txt_temp = unidecode(self)
        txt_temp = re.sub(r'[^a-zA-Z0-9\s]+', ' ', txt_temp) 
        return ' '.join(txt_temp.split())
        
    def remove_stopwords(self,additional_stop_words):
        """
        To remove stop words from the text corpus
        
        Args:
            text : str
            additional_stop_words : set
		
		Returns:
			str
        """
        words = word_tokenize(self)
        stop_words_extended = text_preprocessing.stop_words | text_preprocessing.additional_stop_words
        return ' '.join([x for x in words if x not in stop_words_extended])
    
    def word_search(word, self):
        """
        To search keywords across the text corpus        
        Approach proposed on Stack Overflow (question: 28860440; user: user200783)
        
        Args:
            word : str
            text : str
		
		Returns:
			bool
        """
        return f' {word} ' in f' {self} '
          
    def replace_keywords(self, dict_keyword):
        """
        To replace keywords contained in the text corpus based on flashtext API   
        
        Args:
            text : str
            dict_key_words : dict
		
		Returns:
			str
        """      
        text_preprocessing.keyword_processor.add_keywords_from_dict(dict_keyword)
        return text_preprocessing.keyword_processor.replace_keywords(self)
    
    def remove_keywords(self, new_text, words_to_remove):
        """
        To remove keywords from the text corpus 
        
        Args:
            text : str
            new_text : str
            words_to_remove : set
		
		Returns:
			str
        """              
        pat = r'\b(?:{})\b'.format('|'.join(words_to_remove))
        return re.sub(pat, new_text, self)
        
    def token(self):
        """
        To create tokens from the text corpus (lists of substrings originated 
        by breaking a given text by each space)       
        
        Args:
            text : str          
		
		Returns:
			list of substrings			
        """
        return word_tokenize(self)
    
    @staticmethod
    def get_noun_verb(tokens, set_keyword):
        """
        To extract common nouns and verbs and ensure all keywords are 
        integrated in the text corpus      
        
        Args:
            tokens : list
            set_keyword : set
		
		Returns:
			list of substrings			
        """
        tags = pos_tag(tokens)
        return [i for (i,j) in tags if ((j in ('NN','NNS') or j.startswith('V')) and i!='Bandname') or i in set_keyword]
    
    @staticmethod    
    def stem_word(tokens):
        """
        To stem the text corpus (remove morphological affixes from words)
        
        Args:
            tokens : list
		
		Returns:
			list of substrings			
        """
        stem_tokens = [text_preprocessing.ps.stem(word) for word in tokens if len(text_preprocessing.ps.stem(word))>2]
        return stem_tokens

    @staticmethod        
    def make_bigrams(tokens):
        """
        To create bigram model (sequence of two adjacent words)
        
        Args:
            tokens : list
		
		Returns:
			list of substrings	
        """
        bigram = Phrases(tokens, min_count=20, threshold=100)
        bigram_model = Phraser(bigram)
        return [bigram_model[i] for i in tokens]

    def text_preprocessing_prep(lst):
        """
        To execute preliminary text preprocessing tasks regarding the LDA models
        
        Args:
            lst : list         
    		
    	Returns:
    		list
        """     
        lst_txt_temp = [i.lower() for i in lst]
        lst_txt_temp = [text_preprocessing.replace_keywords(i,text_preprocessing.dict_synonym_replacement) 
                        for i in lst_txt_temp]
        lst_txt_temp = [text_preprocessing.remove_punctuation(i) for i in lst_txt_temp]
        lst_txt_temp = [text_preprocessing.remove_keywords(i,'Bandname',text_preprocessing.set_rock_artist_name) for i in lst_txt_temp]
        lst_txt_temp = [text_preprocessing.remove_stopwords(i,text_preprocessing.additional_stop_words) for i in lst_txt_temp]
        return [text_preprocessing.token(i) for i in lst_txt_temp]   

    def text_preprocessing_to_sklearn(lst):
        """
        To execute the remaining text preprocessing techniques for the Sklearn
        LDA model
        
        Args:
            lst : list         
    		
     	Returns:
    		list
        """
        lst_txt_temp = text_preprocessing.text_preprocessing_prep(lst)
        lst_txt_temp = [text_preprocessing.get_noun_verb(i, text_preprocessing.set_keyword_lda) for i in  lst_txt_temp]
        lst_txt_temp = [text_preprocessing.stem_word(i) for i in lst_txt_temp]
        return [text_preprocessing.replace_keywords(' '.join(i), text_preprocessing.dict_keyword) for i in lst_txt_temp]

    def text_preprocessing_to_gensim(lst):
        """
        To execute the remaining text preprocessing techniques for the Gensim
        LDA model
        
        Args:
            lst : list         
    		
     	Returns:
    		list
        """
        lst_txt_temp = text_preprocessing.text_preprocessing_prep(lst)
        lst_txt_temp = text_preprocessing.make_bigrams(lst_txt_temp) 
        lst_txt_temp = [text_preprocessing.get_noun_verb(i, text_preprocessing.set_keyword_lda) for i in lst_txt_temp]
        lst_txt_temp = [text_preprocessing.stem_word(i) for i in lst_txt_temp]
        lst_txt_temp = [text_preprocessing.replace_keywords(' '.join(i), text_preprocessing.dict_keyword) for i in lst_txt_temp]
        return [text_preprocessing.token(i) for i in lst_txt_temp]
       
    def text_preprocessing_rule_based_txt_class_prep(lst):
        """
        To execute preliminary text preprocessing tasks 
        
        Because stop words and punctuation marks are necessary to perform 
        preparatory classification rules on the type of publication, a biphasic text 
        preprocessing has been set.      
        
        Args:
            lst : list         
    		
    	Returns:
    		list
        """  
        lst_txt_temp = [i.lower() for i in lst]
        lst_txt_temp = [re.sub("’", "'", i) for i in lst_txt_temp]
        lst_txt = [text_preprocessing.replace_keywords(i,text_preprocessing.dict_synonym_replacement) for i in lst_txt_temp]
        return lst_txt

    def text_preprocessing_rule_based_txt_class(lst):
        """
        To execute the essential text preprocessing techniques      
        
        Args:
            lst : list         
    		
    	Returns:
    		list
        """
        lst_txt_temp = [text_preprocessing.remove_punctuation(i) for i in lst]
        lst_txt_temp = [text_preprocessing.remove_keywords(i,'Bandname',text_preprocessing.set_rock_artist_name) for i in lst_txt_temp]
        lst_txt_temp = [text_preprocessing.remove_stopwords(i,text_preprocessing.additional_stop_words) for i in lst_txt_temp]
        lst_txt_temp = [text_preprocessing.token(i) for i in lst_txt_temp]   
        lst_txt_temp = [text_preprocessing.get_noun_verb(i, text_preprocessing.set_keyword) for i in lst_txt_temp]
        lst_txt_temp = [text_preprocessing.stem_word(i) for i in lst_txt_temp]
        lst_txt = [text_preprocessing.replace_keywords(' '.join(i), text_preprocessing.dict_keyword) for i in lst_txt_temp]
        return lst_txt 