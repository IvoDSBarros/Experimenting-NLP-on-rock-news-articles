# Overview
This repository is made up of multiple NLP experiments on web rock news articles. The text corpus is comprised by 20 000 rock news headlines and descriptions with no labeled data. The data was retrieved from 6 rock specialized websites: Loudersound, loudwire, Ultimate Classic Rock (UCR), Kerrang!, Planet Rock and The New York Times (NYT). 

<details>
<summary> Table of Contents </summary>

1. [Dictionary-based Named Entity Recognition](#dictionary-based-named-entity-recognition)
2. [Rule-based text classification](##-rule-based-text-classification)

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
