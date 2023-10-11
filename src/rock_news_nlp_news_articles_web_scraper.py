"""
Rock News NLP: news articles web scraper
Created on Sat Feb 19 18:12:13 2022
@author: IvoBarros
"""

#==============================================================================
# For proof of concept, this web scraper is restricted to the loudwire website
#==============================================================================

import requests
from bs4 import BeautifulSoup 
import pandas as pd 
import numpy as np 
import os
from datetime import datetime
from time import time, sleep
from random import randint

def get_links_loudwire(nr_pages, links_web_data_source):
    """
    To compile a list of news articles links from the loudwire website pages 
    
    Args:
        nr_pages : int
        links_web_data_source : list
        
    Returns:
        list
    """
    website = 'https://loudwire.com/category/news/'
    links_pages = []
    multiple_links = []
    
    for i in range(2,nr_pages):  
        links_pages.append(f'{website}/page/{str(i)}/')
    
    links_pages.append(website)
 
    for i in links_pages:
        try:
            page = requests.get(i)
            soup = BeautifulSoup(page.content, 'html.parser')    
            newslinksection = soup.find_all('a',attrs={'class':'theframe'}, href=True)
            for j in newslinksection:
                if j['href'].count('/')==4:
                    multiple_links.append("https:" + j['href'])
        except:
            pass   
        sleep(randint(2,5))
        
    multiple_links = list(set(multiple_links))
    
    return [i for i in multiple_links if i not in links_web_data_source]  

def extract_news_articles_attributes(links):
    """
    To extract and store the attributes of every single news article
 
    Args:
        links : list
        
    Returns:
        DataFrame
    """   
    web_data = {"website": [], "title": [], "description": [], "body": [], "date": [], "link": []}
    
    for i in links:
        try:
            page = requests.get(i)
            soup = BeautifulSoup(page.content, 'html.parser')
            web_data['website'].append(soup.find('meta', attrs={'property':'og:site_name'})['content'])
            web_data['title'].append(soup.find('meta', attrs={'property':'og:title'})['content'])                
            web_data['description'].append(soup.find('meta', attrs={'property':'og:description'})['content'])
            web_data['body'].append(soup.find('div',attrs={'class':'content'}).text.strip())
            web_data['date'].append(soup.find('meta', attrs={'name':'sailthru.date'})['content'])
            web_data['link'].append(i)
        except:
            pass
        sleep(randint(2,5))
        
    return  pd.DataFrame(web_data)

def incremental_load(source_web_data, destination_web_data, last_date):
    """
    To perform an incremental load of the last retrieved web data into the
    rock news data source
 
    Args:
        source_web_data : DataFrame
        destination_web_data : DataFrame
        last_date : date
        
    Returns:
        DataFrame
    """   
    source_web_data['date'] = pd.to_datetime(source_web_data['date']).dt.date

    source_web_data = source_web_data.loc[(source_web_data.title != '') 
                                          & (source_web_data.description != '') 
                                          & (source_web_data.body != '') 
                                          & (source_web_data.date != '') 
                                          & (source_web_data.date >= last_date)]
       
    source_web_data = source_web_data.assign(valid_from = datetime.today().strftime('%Y-%m-%d'),
                                             valid_to = "9999-12-31",
                                             status = 1,
                                             full_pk = [i.replace(" ", "").upper()+j.replace(" ", "").upper() 
                                                        for i,j in zip(source_web_data['website'],source_web_data['title'])]) 

    return pd.concat([destination_web_data, source_web_data], ignore_index=True)

print("The script is running...")
t_start = time()

#==============================================================================
# 1. LOAD AND PREPARE DATA
#==============================================================================
path_parent_dir = os.path.dirname(os.getcwd())
path_data_web_scrapers = f'{path_parent_dir}\data\web_scrapers'
df_rock_news = pd.read_csv(f'{path_data_web_scrapers}/rock_news.csv',sep=';')
df_rock_news['date'] = pd.to_datetime(df_rock_news['date']).dt.date
max_date_bysite = df_rock_news.groupby(['website']).agg({'date': np.max})
last_date = max_date_bysite['date'].min()
list_links = df_rock_news['link'].tolist()                                    

#==============================================================================
# 2. WEB SCRAPING TASKS AND INCREMENTAL LOAD
#==============================================================================
multiple_links = get_links_loudwire(4, list_links)                                              
df_rock_news_delta = extract_news_articles_attributes(multiple_links)  
df_rock_news_updated = incremental_load(df_rock_news_delta, df_rock_news, last_date)
# df_rock_news_updated.to_csv(f'{path_data_web_scrapers}/rock_news.csv', header=True, index=False, encoding='utf-8',sep=';')
print("...it has been successfully executed in %0.1fs." % (time() - t_start))
