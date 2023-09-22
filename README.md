# Overview
This repository contains multiple NLP experiments on web rock-based news articles. The text corpus is comprised by 20K rock news headlines and descriptions with unlabelled data (for demonstration purposes, a random subset of 2K articles is available in this repository). The data was retrieved between January 2022 and September 2023 from 6 specialized rock websites: Loudersound, loudwire, Ultimate Classic Rock, Kerrang!, Planet Rock and The New York Times.

<details>
<summary> Table of Contents </summary>

1. [Dictionary-based Named Entity Recognition](#dictionary-based-named-entity-recognition)
2. [Rule-based text classification](#rule-based-text-classification)
3. [Topic modeling experiments](#topic-modeling-experiments)
    + [LDA model using Scikit-learn](#1-lda-model-using-scikit-learn)
    + [LDA model using Gensim](#2-lda-model-using-gensim)
4. [References](#references)

</details>

**Metallica: the monster still lives**
<br>Infographic based on the text corpus

![](https://github.com/IvoDSBarros/Experimenting-NLP-on-rock-news-articles/blob/bbd96d23028682b430b1a392bc1e343436d3deff/output/visuals/metallica_the_monster_still_lives_infographic.png)


## Dictionary-based Named Entity Recognition
### Goals
The purpose of this model is identifying and extracting rock artist/rock artist member names from the headlines and descriptions of the above-mentioned text corpus. A custom dictionary-based named entity recognition (NER) approach is tested. The pre-built dictionary is based on data extracted from Wikipedia lists on rock, metal and punk bands gathered by a web scraper.

### Challenges
+ Single/multiple rock artist name(s) and/or single/multiple rock artist member name(s) might be mentioned in a news headline and/or news description. Hence, the text of the headline and the text of the description were combined to perform the search of the rock artist and the rock artist member. Additionally, only whole/compound words are matched to avoid inaccurate labelling. The pre-built dictionaries of rock artists/artists member names contain 38,663 records. Given the ultimate purpose is assigning lists of identified rock artist/artist member names per every single text of the corpus, performance is a critical issue. Several methods were assessed including Vectorization, Flashtext, Regex and a whole word search approach proposed on Stack Overflow (question 5319922, user200783). The latter, in conjunction with a text preprocessing approach which removes special characters and a set of rock artists/artists member names, demonstrated to be the fastest and most effective.

+ Acronyms are used to mention some rock artists (A7X, RHCP, RATM, GN'R) and the definite article "The" is sometimes excluded to mention artists whose name starts with "The" (a stop word removal approach would perfectly work out for bands like "The Beatles" or "The Rolling Stones" but it is not the case for bands such as "The Who" - it would be completely removed as "The" and "Who" are both stop words - or "The Doors" - "Doors" would be matching both "The Doors" and "Three Doors Down" news articles afterwards). Moreover, popular songs or albums are often mentioned without reference to the rock artist in the headlines and/or descriptions. Misspellings were identified on the rock artist names in the headlines.

+ The words of the news headlines from the websites Loudwire and Ultimate Classic Rock start with capital letter.

+ Bands like "Yes", "HIM", "Sweet" or "The Band" lead to misleading labelling. Additional text preprocessing actions were required to ensure accurate outcomes.
<br>

**Top 50 rock artists and rock artist members** 

![](https://github.com/IvoDSBarros/Experimenting-NLP-on-rock-news-articles/blob/af1d58f87e99b5948ecea46892cd02a096d6de6c/output/visuals/dict_based_ner_viz.png)

<div align = "right">    
  <a href="#overview">(back to top)</a>
</div>

## Rule-based text classification
### Goals
This rule-based text classification model is intended to identify keywords and assign both topic labels and publication type categories across the no labeled rock news headlines. A set of pre-defined rules has been manually created for this purpose. The core of the rock news headlines' semantic landscape consists of the keywords 'album', 'single', 'song', 'show', 'tour' and 'video'. The keywords are the foundation to set up the classification logical rules and assign human-readable contextualized tags.

### Challenges
+ To ensure all semantically relevant keywords in which the set of classification rules is based on are integrated in the cleaned text corpus when performing the extraction of common nouns and verbs. A function was designed in this respect by combining the selection of the mentioned part-of-speech (POS) tags and a list of all relevant keywords. 

+ Taking into account the target POS tags, it was mandatory at first to replace the previously identified rock artists names by a unique word, "Bandname", to mitigate any disrutpion of the POS tagging tasks executed afterwards. The word "Bandname" was later removed from the text corpus. 

+ With regards to text normalization techniques, stemming turned out to be the most effective to prepare the text corpus for further processing. This was particularly significant when dealing with verb tenses. Anyway, as "think" and "say" are relevant keywords and irregular verbs, its past simple form was replaced by the present simple in anticipation. 

+ To ensure synonyms of relevant keywords are accurately standardized, a dictionary has been created in light of the specific semantic field these keywords show in the context of rock news. In fact, the verbs "drop", "unleash", "share", "premier" and "launch" are generally related to music releases, while "unveil" and "reveal" tend to be associated ta annoucements in most cases.
<br>

**Alluvial diagram on the rock news articles** 

![](https://github.com/IvoDSBarros/Experimenting-NLP-on-rock-news-articles/blob/9c8c49fd0a9cb2c7673c1ebf615fa2912af6e914/output/visuals/rule_based_text_%20class_viz.png)


<div align = "right">    
  <a href="#overview">(back to top)</a>
</div>

## Topic modeling experiments
### Goals
Along with the rule-based text classification model, an unsupervised machine learning method for topic modeling has been conducted, specifically, the Latent Dirichlet Allocation (LDA). Two models have been developed using the Python's libraries **(1) Scikit-learn** and **(2) Gensim**. Both models have been trained on 18,000 news articles. The text preprocessing methodological choices have already been detailed in the Rule-based text classification chapter.

#### Challenges
+ As the LDA algorithm is stochastic and the output is different every run, to ensure the reproducibility of the Scikit-learn and Gensim LDA models the random state parameter has been set to 0. 

+ The results obtained through the frequency–inverse document frequency (TF–IDF) were not the expected for both models. Despite its main purpose of scaling down the impact of predominant tokens, the interpretability of topics was not as coherent and comprehensible as raw frequencies of occurence.

+ The hyperparameter optimization of the Scikit-learn LDA model, namely the parameters n_components and learning_decay, has been done through the grid search method.

+ In order to to overcome the instability and non-reproducibility of the sklearn and gensim lda/ldamulticore approaches, a Gensim Ensemble LDA has been implemented.

#### 1. LDA model using Scikit-learn 
#### Results
**LDA evaluation model metrics in Scikit-learn** <br>
Perplexity and likelihood score are conventional performance metrics available in the Scikit-learn library to diagnose a LDA model. These statistiscal measures evaluate the predictive accuracy of a model on unseen texts. According to the available literature, the lower the perplexity, the better the model. On the contrary, a higher likelihood score is indicative of a better fit. However, there's no pre-defined threshold that make clear what is a lower preplexity score or a higher likelihood score. Based on the work of Blei, D. et al. (2003), the perplexity goes in the opposite direction of the number of topics meaning that the first tends to decrease when the second increases. It is noteworthy that a study conducted by Chang J. et al. (2009) suggested no relationship between perplexity and human interpretation.

**Perplexity and Likelihood score over number of topics in the test set**
![](https://github.com/IvoDSBarros/Experimenting-NLP-on-rock-news-articles/blob/38e5a92cefb5455a58aee58bedde8096c9b7b033/output/visuals/lda_sklearn_assessment.png)

+ **Perplexity** =  682.3
+ **Likelihood score** = -105,182.4


**Interactive topic model visualization with pyLDAvis** <br>
To get a visual overview of the lda model, we used the Python library pyLDAvis based on the R package LDAvis developed by Sivert C. & Shirley K. (2014). In agreement with the authors, the left panel of the visualization is intended to clarify both the prevalence of each topic of the model and the interconnection between topics. Being that said, the left-hand side chart shows 6 big bubbles distributed along the quadrants and further away from each other ([click here to access the interactive topic model visualization](https://raw.githack.com/IvoDSBarros/Experimenting-NLP-on-rock-news-articles/main/output/visuals/sklearn_train_lda_model_viz.html)). Such a visual representation is symptomatic of a good model. Actually, the topics generated by the LDA model portray, in some extent, the previously mentioned semantic landscape of the rock news headlines: 
+ Topic 0: single release and opinion;
+ Topic 1: album announcement;
+ Topic 2: tour announcement;
+ Topic 3: video release;
+ Topic 4: video and live performance related;
+ Topic 5: artist death related. <br><br>

#### 2. LDA model using Gensim
Replicability and instability are two major issues of topic modeling. The Ensemble LDA method aims to mitigate these issues by *"finding and generating stable topics from the results of multiple topic models"* and remove topics *"that are noise and are not reproducible"* (Řehůřek, 2022b). On the top of that, there is no *"need to know the exact number of topics ahead of time"* (Řehůřek, 2022a).

#### Results
The Ensemble LDA we performed returned 6 topics that, once again, represent the semantic landscape of the rock news headlines:
+ Topic 0: video and single releases; 
+ Topic 1: tour announcement;
+ Topic 2: album release;
+ Topic 3: song related;
+ Topic 4: live performance related;
+ Topic 5: artist death related;

**Top 10 words per topic**

![]()

**LDA evaluation model metrics in Gensim** <br>
To evaluate the Ensemble LDA model we used the UMass Coherence score and Perplexity. Within the topic modelling context, *"a set of statements or facts is said to be coherent, if they support each other"* (Röder et al., 2015). In simple terms, coherence is the *"humans’ semantic appreciation of a topic represented by its N top words"* (Trenquier, 2018). The UMass coherence score relies on document frequency and takes into account order among the top words of a topic (Röder et al., 2015). It ranges bvetween -14 and 14 and reaches its peak at 0. The UMass has been chosen instead of C_V metric as the last one is not recommended *"when it is used for randomly generated word sets"* (Roeder, 2018). We get a UMass score of -12.29 which indicates topics are not perfectly coherent, however when it comes to human interpretation it was by far the best model obtained through LDA Ensemble.
With regards to Perplexity (formula: 2^(-bound)), its value is once again tolerable.

+ **Perplexity** = -8.17 
+ **Umass coherence score** = -12.29 (doublecheck the value)

**Manual rule-based text classification Vs. Unsupervised Machine Learning Classification**
<br>The alluvial diagram below is based on the test set of 2000 unseen texts.
<br>Sklearn and Gensim LDA main topics <40% have been categorized as "multi-category".

![](https://github.com/IvoDSBarros/Experimenting-NLP-on-rock-news-articles/blob/b161999e27e245a471d5afcb4fcefd7714bd1184/output/visuals/rule_based_vs_%20ml_lda.png)

<div align = "right">    
  <a href="#overview">(back to top)</a>
</div>

## References
+ [Blei, D., Ng, A., Jordan, M. (2003) Latent Dirichlet Allocation. Journal of Machine Learning Research, 3, 993-1022.](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf)
+ [Chang, J., Boyd-Graber, J., Gerrish, S., Wang, C., Blei, D. (2009, December) Reading Tea Leaves: How Humans Interpret Topic Models. NIPS'09: Proceedings of the 22nd International Conference on Neural Information Processing Systems, 288–296.](https://proceedings.neurips.cc/paper/2009/file/f92586a25bb3145facd64ab20fd554ff-Paper.pdf)
+ [Řehůřek, R. (2022a) models.ensembelda – Ensemble Latent Dirichlet Allocation. https://radimrehurek.com/gensim/models/ensemblelda.html](https://radimrehurek.com/gensim/models/ensemblelda.html)
+ [Řehůřek, R. (2022b) Ensemble LDA. https://radimrehurek.com/gensim/auto_examples/tutorials/run_ensemblelda.html](https://radimrehurek.com/gensim/auto_examples/tutorials/run_ensemblelda.html)
+ [Roeder, M., Both, A., Hinneburg, A. (2015, February). Exploring the Space of Topic Coherence Measures. WSDM '15: Proceedings of the Eighth ACM International Conference on Web Search and Data Mining, 399–408. https://doi.org/10.1145/2684822.2685324](http://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf)
+ [Roeder, M. (2018) Not being able to replicate coherence scores from paper #13](https://github.com/dice-group/Palmetto/issues/13)
+ [Sievert, C., Shirley, K. (2014, June) LDAvis: A method for visualizing and interpreting topic. Proceedings of the Workshop on Interactive Language Learning, Visualization, and Interfaces, 63–70.](https://nlp.stanford.edu/events/illvi2014/papers/sievert-illvi2014.pdf) 
+ [Trenquier, H. (2018) Improving Semantic Quality of Topic Models for Forensic Investigations. University of Amsterdam, MSc System and Network Engineering Research Project 2.](https://rp.os3.nl/2017-2018/p76/report.pdf)

<div align = "right">    
  <a href="#overview">(back to top)</a>
</div>
