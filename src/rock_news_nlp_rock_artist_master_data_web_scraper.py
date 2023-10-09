"""
Rock News NLP: rock artist master data web scraper
Created on Thu Apr 28 19:12:33 2022
@author: IvoBarros
"""

#================================================================================
# For proof of concept, this web scraper is restricted to the acid rock subgenre
#================================================================================

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
from time import time, sleep
from random import randint

def get_rock_subgenre_links(website):
    """
    To compile Wikipedia lists of links on rock subgenres
    
    Args:
        website : str
        
    Returns:
 	list
    """
    page = requests.get(website)
    soup = BeautifulSoup(page.content, 'html.parser')
    links_subgenres = []
        
    for i in soup.find_all('div', attrs={'class':'mw-category-group'}):
        for j in i.find_all('a'):
            if '/wiki/Category' not in j['href']:
                links_subgenres.append('https://en.wikipedia.org'+j['href'])
                
    return links_subgenres            

def get_rock_artist_links(links_subgenres):
    """
    To compile a list of Wikipedia links on rock artists
    
    Args:
        links_subgenres : list
        
    Returns:
	list
    """ 
    links_rock_artist = []
    rock_artist_genre = []

    for i in links_subgenres:
        page = requests.get(i)
        soup = BeautifulSoup(page.content, 'html.parser')
        rock_genre = re.search(r'^.+/List_of_(.+)$', i).group(1) 
        
        for j in soup.find_all('div', attrs={'class':'div-col'}):
            for k in j.find_all('a'):
                if '#cite' not in k['href']:
                    links_rock_artist.append('https://en.wikipedia.org'+k['href'])
                    rock_artist_genre.append(rock_genre)                
        sleep(randint(2,5))
        
    return links_rock_artist, rock_artist_genre

def extract_wiki_artist_infobox_attributes(links_rock_artist, rock_artist_genre):
    """
    To extract and store the Wikipedia infobox attributes of rock artists
 
    Args:
        links_rock_artist : list
        rock_artist_genre : list
        
    Returns:
 	DataFrame
    """   
    web_data = {"rock_artist": [], "genre": [], "label": [], "description": []}

    for i,j in zip(links_rock_artist, rock_artist_genre):
        try: 
            page = requests.get(i)
            soup = BeautifulSoup(page.content, 'html.parser')
            infobox = soup.find('table', attrs={'class':'infobox vcard plainlist'})
            
            try: 
                labels = infobox.find_all('th', attrs={'class':'infobox-label'})
                data = infobox.find_all('td', attrs={'class':'infobox-data'})
                artist_name = infobox.find('th', attrs={'class':'infobox-above'}).text.strip()
              
                for k, l in zip(labels,data):           
                    if eval(condition_htlm_list) or eval(condition_html_ul_wo_list):
                        for m in l.find_all('li'):
                            web_data['rock_artist'].append(artist_name)
                            web_data['genre'].append(j)
                            web_data['label'].append(k.text)
                            web_data['description'].append(m.text)         
                    elif eval(condition_html_br):
                        for n in l:
                            if len(n.text)>0:
                                web_data['rock_artist'].append(artist_name)
                                web_data['genre'].append(j)
                                web_data['label'].append(k.text)
                                web_data['description'].append(n.text)           
                    else:
                        web_data['rock_artist'].append(artist_name)
                        web_data['genre'].append(j)
                        web_data['label'].append(k.text)
                        web_data['description'].append(l.text)
                
            except:
                pass 
        except:
            pass 
        sleep(randint(2,5))
        
    wiki_list_rock_artist = pd.DataFrame(web_data)        
    wiki_list_rock_artist = wiki_list_rock_artist.assign(full_pk = [i.replace(" ", "").upper()+j.replace(" ", "").upper()+k.replace(" ", "").upper() 
                                                                    for i,j,k in zip(wiki_list_rock_artist['rock_artist'],
                                                                                     wiki_list_rock_artist ['label'],
                                                                                     wiki_list_rock_artist ['description'])])             
    
    return wiki_list_rock_artist

print("The script is running...")
t_start = time()

#==============================================================================
# WEB SCRAPING TASKS
#==============================================================================
path_parent_dir = os.path.dirname(os.getcwd())
path_data_web_scrapers = f'{path_parent_dir}\data\web_scrapers'

## CREATE RULES TO SUPPORT THE EXTRACTION OF WIKIPEDIA INFOBOX ATTRIBUTES
condition_htlm_list = "(len(l.find_all('div', attrs={'class':'hlist'}))>0)==True \
                      or \
                      (len(l.find_all('div', attrs={'class':'plainlist'}))>0)==True"

condition_html_ul_wo_list = "(((len(l.find_all('div', attrs={'class':'hlist'}))>0)==False \
                                and (len(l.find_all('div', attrs={'class':'plainlist'}))>0)==False) \
                                and (len(l.find_all('ul'))>0)==True)"

condition_html_br = "(len(l.find_all('br'))>0)==True"

## EXCTRACT WEB DATA
links_subgenres = get_rock_subgenre_links("https://en.wikipedia.org/wiki/Category:Lists_of_rock_musicians_by_subgenre")
links_subgenres = [i for i in links_subgenres if "acid" in i]
links_rock_artist, rock_artist_genre = get_rock_artist_links(links_subgenres)
wiki_list_acid_rock_artist = extract_wiki_artist_infobox_attributes(links_rock_artist, rock_artist_genre)
# wiki_list_acid_rock_artist.to_csv(f'{path_data_web_scrapers}/wiki_list_acid_rock_artist.csv', header=True, index=False, encoding='utf-8',sep=';')
print("...it has been completed sucessfully in %0.1fs." % (time() - t_start))
