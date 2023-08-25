# Overview
This repository is made up of multiple NLP experiments on web rock news articles. The text corpus is comprised by 20 000 rock news headlines and descriptions with no labeled data. The data was retrieved from 6 rock specialized websites: Loudersound, loudwire, Ultimate Classic Rock (UCR), Kerrang!, Planet Rock and The New York Times (NYT). 

<details>
<summary> Table of Contents </summary>

1. [Dictionary-based Named Entity Recognition](#-dictionary-based-named-entity-recognition)
2. [Rule-based text classification](#-rule-based-text-classification)

</details>

## Dictionary-based Named Entity Recognition
### Goals
The purpose of this script is identifying and extracting rock artist/rock artist member names from a text corpus comprised by rock news headlines and descriptions with no labeled data. With this end in view a dictionary-based named entity recognition (NER) approach has been implemented. The pre-built dictionary is made up of data from multiple wikipedia lists on rock, metal and punk bands gathered by a web scraper.

### Challenges
1. Single/multiple rock artist name(s) and/or single/multiple rock artist member name(s) might be mentioned in a news headline and/or news description. Hence the text of the headline and the text of the description were combined to perform the search of the rock artist and rock artist member. Additionally, only whole words/compound words should be matched to avoid wrong labelling. On the other hand, the pre-built dictianaries of rock artists/rock artists member names contain 38 663 records. Given this particular context and taking into account that the end goal is assigning lists of identified rock artist/rock artist member names per every single text of the corpus, performance has become a critical issue. Several methods were evaluated including vectorization, flashtext, regex and a whole word search approcah proposed on Stack Overflow (question 5319922, user200783). The last one, when combined with a previous text preprocessing by removing special characters and a set of rock artists/rock artists member names, has proved to be the fastest and most effective.

2. Acronyms are used to mention some rock artists (A7X, RHCP, RATM, GN'R) and the definite article "The" is sometimes excluded to mention artists whose name starts with "The" (a stop word removal approach would perfectly work out for  bands like The Beatles or The Rolling Stones but it is not the case for bands such as The Who - it would be completely removed as "The" and "Who" are both  stop words - or The Doors - "Doors" would be matching both The Doors and Three Doors Down news articles afterwards). Moreover, popular songs or albums are often mentioned with no reference to the rock artist across the headlines and the descriptions. Some misspellings were identified on the rock artist names through the headlines.            

3. The words of the news headlines from the websites Loudwire and Ultimate Classic Rock start with capital letter.

4. Bands like "Yes", "HIM", "Sweet" or "The Band" lead to misleading labelling so additional text preprocessing actions were required.

<div align = "right">    
  <a href="#overview">(back to top)</a>
</div>

## Rule-based text classification
### Goals
This rule-based text classification model is intended to identify keywords and assign both topic labels and publication type categories across a text corpus comprised by rock news headlines with no labeled data. A set of pre-defined rules has been manually created for this purpose. The core of the rock news headlines' semantic landscape consists of the keywords 'album', 'single', 'song', 'show', 'tour' and 'video'. The keywords are the foundation to set up the classification logical rules and assign human-readable contextualized tags.

### Challenges
1. To ensure all semantically relevant keywords in which the set of classification rules is based on are integrated in the cleaned text corpus when performing the extraction of common nouns and verbs. A function was designed in this respect by combining the selection of the mentioned part-of-speech (POS) tags and a list of all relevant keywords. 

2. Taking into account the target POS tags, it was mandatory at first to replace  the previously identified rock artists names by a unique word, "Bandname", to mitigate any disrutpion of the POS tagging tasks executed afterwards. The word "Bandname" was later removed from the text corpus. 

3. With regards to text normalization techniques, stemming turned out to be the most effective to prepare the text corpus for further processing. This was particularly significant when dealing with verb tenses. Anyway, as "think" and "say" are relevant keywords and irregular verbs, its past simple form was replaced by the present simple in anticipation. 

4. To ensure synonyms of relevant keywords are accurately standardized, a dictionary has been created in light of the specific semantic field these keywords show in the context of rock news. In fact, the verbs "drop", "unleash", "share", "premier" and "launch" are generally related to music releases, while "unveil" and "reveal" tend to be associated ta annoucements in most cases.

<div align = "right">    
  <a href="#overview">(back to top)</a>
</div>



# Topic Modeling of BBC News Articles
This project is a Capstone Project done as part of Unsupervised Machine Learning. A set of 2225 BBC News Articles are analysed to identify the underlying themes and topics within them.

<details>
<summary>Table of Contents</summary>

1. [About the Project](#about-the-project)
2. [Data Reading and Description](#data-reading-and-description)
3. [Data Pre-Processing](#data-pre-processing)
4. [Model Implementation](#model-implementation)
    + [LDA Model](#1-lda-model)
    + [LSA Model](#2-lsa-model)
5. [Model Evaluation](#model-evaluation)
6. [Results](#results)
7. [Conlusion](#conclusion)
8. [Challenges Faced](#challenges-faced)
9. [Libraries Used](#libraries-used)
10. [Contact](#contact)
</details>

## About The Project

Topic modelling is a widely used technique in natural language processing that helps to extract latent topics from a large collection of documents. In the context of News Articles, it categorises these documents into various categories of requirement, which is very helpful for organisations to manage their content and for the readers as well, to easily find articles of interest.

It can also help in content summarisation by breaking down the lengthy articles into keywords and themes to briefly summarise the content in a concise manner, without loss of information.

This Project focuses on the former application, to determine the underlying topics within the corpus of News Articles. The original category of each article is provided as an input for evaluation of the topic modeling algorithm. It should be noted that these original categories are not considered as an input for modeling and is in no way influences the algorithm metholody.
<div align = "right">    
  <a href="#topic-modeling-of-bbc-news-articles">(back to top)</a>
</div>

## Data Reading and Description

The Dataset was available as individual txt files for each article, with their original category/topic provided as an input. It was read into the Python Notebook using **re** and **glob** libraries and converted into a single DataFrame with the following columns:
*   **Title**: Title of the article
*   **Description**: Content of the article
*   **Category**: Original Category of the article

<div align = "right">    
  <a href="#topic-modeling-of-bbc-news-articles">(back to top)</a>
</div>

## Data Pre-Processing

Before applying the topic modeling algorithms, the textual data was preprocessed to expand contractions, remove punctuations, digits, whitespaces and stop words, and to lemmatize the remaining words. The resulting corpus was then vectorized using both the Count and TFIDF vectorizers, with each row in the vectorized data representing a document and each column representing a unique term in the corpus

<div align = "right">    
  <a href="#topic-modeling-of-bbc-news-articles">(back to top)</a>
</div>

## Model Implementation

Three models were applied on the vectorized data, with the first two being variations of **Latent Dirichlet Allocation (LDA)** algorithm and the third one using the **Latent Semantic Analysis (LSA)**.
### 1. LDA Model

The Latent Dirichlet Allocation (LDA) model was trained on the preprocessed data using the Scikit-learn library. The model was optimized using GridSearchCV to determine the optimal number of topics. The model was trained on two different vectorized data inputs - one in which the vectorization method was using CountVectorizer, and the other with TFIDF-Vectorizer.

### 2. LSA Model

The LSA model was trained on the pre-processed data using the TruncatedSVD class in sciki-learn library. Similar to LDA model, both TFIDF and CountVectorized inputs were given to the model, and each topic was analysed.

<div align = "right">    
  <a href="#topic-modeling-of-bbc-news-articles">(back to top)</a>
</div>

## Model Evaluation

The Log-Likelihood and Perplexity scores were evaluated for each of the models. Since the original category of each article is provided as an input, the metrics of evaluation for a Classification problem - Precision, Recall and F1 Score - are utilised here. F1 Score is given priority because of the equality and non-hierarchy between each topic.

<div align = "right">    
  <a href="#topic-modeling-of-bbc-news-articles">(back to top)</a>
</div>

## Results

It was found that the LDA models outperformed the LSA models. The LSA model identified primarily only two topics, with it over-predicting on one of them. In contrast, the LDA models identified all the five topics corresponding closely with the original article categories.

Comparing the two LDA models, the model with CountVectorized data as the input well outperformed the other model. The model accuracy was close to 93%, with the latter only scoring about 85%. It fared better in the other metrics as well, except in Log-likelihood score.

<div align = "right">    
  <a href="#topic-modeling-of-bbc-news-articles">(back to top)</a>
</div>

## Conclusion

Overall, the LDA model with CountVectorizer proved to be a more effective approach to topic modeling of the BBC News articles dataset, producing results which closely corresponded with the original article categories. This project demonstrates the usefulness of topic modeling techniques for understanding large text datasets and the importance of selecting an appropriate algorithm for the task at hand.

<div align = "right">    
  <a href="#topic-modeling-of-bbc-news-articles">(back to top)</a>
</div>

## Challenges Faced

*   The first challenge faced in the project was right at the start: reading the text files to form a consolidated, tabular dataset. It took some bit of searching and reading of documentations to attain the knowledge and apply it to code. Some encoding errors also needed to be tackled in the process.
*   While pre-processing was mostly a breeze, the choice of vectorization methods for specific models was another challenge. It was (rightly) expected that the CountVectorizer would be suitable for LDA, so the same was considered a Hypothesis which was tested by deploying the LDA on both the Bag-of-Words model and TFIDF Vectorized dataset. The Hypotheses statement finally turned to be true, atleast in this context.
*   Finally, the choice of evaluation metrics: Apart from Perplexity and Log-Likelihood, another set of metrics were needed which is more interpretable to evaluate the models. So, the metrics usually used for Classification Problems - Precision, Recall and F1 Score, was chosen. It seemed unconventional at first, but proved very fruitful.

<div align = "right">    
  <a href="#topic-modeling-of-bbc-news-articles">(back to top)</a>
</div>

## Libraries Used

For reading, handling and manipulating data

* |[glob](https://docs.python.org/3/library/glob.html)|
  |---|
* |[re](https://docs.python.org/3/library/re.html)|
  |---|
* |[pandas](https://pandas.pydata.org)|
  |---|
* |[numpy](https://numpy.org)|
  |---|
* |[random](https://docs.python.org/3/library/random.html)|
  |---|

For Visualisation
* |[matplotlib](https://matplotlib.org)|
  |---|
* |[seaborn](https://seaborn.pydata.org)|
  |---|
* |[pyLDAvis](https://pyldavis.readthedocs.io/en/latest/readme.html)|
  |---|
* |[wordcloud](https://pypi.org/project/wordcloud/)|
  |---|

For Textual Pre-processing and Model Building
* |[string](https://docs.python.org/3/library/string.html)|
  |---|
* |[nltk](https://nltk.org)|
  |---|
* |[contractions](https://pypi.org/project/pycontractions/)|
  |---|
* |[sklearn](https://scikit-learn.org/stable/)|
  |---|

<div align = "right">    
  <a href="#topic-modeling-of-bbc-news-articles">(back to top)</a>
</div>

## Contact

|[Gmail](mailto:apaditya96@gmail.com)|[Linkedin](https://www.linkedin.com/in/aditya-a-p-507b1b239)|
|---|---|

<div align = "right">    
  <a href="#topic-modeling-of-bbc-news-articles">(back to top)</a>
</div>
