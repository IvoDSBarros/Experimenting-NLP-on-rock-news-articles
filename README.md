# Overview
This repository is made up of multiple NLP experiments on web rock news articles. The text corpus is comprised by 20 000 article news retrieved from 6 rock specialized websites: Loudersound, loudwire, Ultimate Classic Rock (UCR), Kerrang!, Planet Rock and The New York Times (NYT). 

<details>
<summary>**Table of Contents**</summary>
[Rule based text classification](#-rule-based-text-classification)
</details>

# Rule based text classification
## Goals
This rule-based text classification model is intended to identify keywords and assign both topic labels and publication type categories across a text corpus comprised by rock news headlines with no labeled data. A set of pre-defined rules has been manually created for this purpose. The core of the rock news headlines' semantic landscape consists of the keywords 'album', 'single', 'song', 'show', 'tour' and 'video'. The keywords are the foundation to set up the classification logical rules and assign human-readable contextualized tags.
<div align = "right">    
  <a href="#overview">(back to top)</a>


# test

Getting started with Markdown
=============================


- [Getting started with Markdown](#getting-started-with-markdown)
- [Titles](#titles)
- [Paragraph](#paragraph)
- [List](#list)
	- [List CheckBox](#list-checkbox)
- [Link](#link)
	- [Anchor links](#anchor-links)
- [Blockquote](#blockquote)
- [Image | GIF](#image--gif)
- [Style Text](#style-text)
	- [Italic](#italic)
	- [Bold](#bold)
	- [Strikethrough](#strikethrough)
- [Code](#code)
- [Email](#email)
- [Table](#table)
	- [Table Align](#table-align)
    	- [Align Center](#align-center)
    	- [Align Left](#align-left)
    	- [Align Right](#align-right)
- [Escape Characters](#escape-characters)
- [Emoji](#emoji)
- [Shields Badges](#Shields-Badges)
- [Markdown Editor](#markdown-editor)
- [Some links for more in depth learning](#some-links-for-more-in-depth-learning)

----------------------------------

# Titles 

### Title 1
### Title 2

	Title 1
	========================
	Title 2 
	------------------------

# Title 1
## Title 2
### Title 3
#### Title 4
##### Title 5
###### Title 6

    # Title 1
    ## Title 2
    ### Title 3    
    #### Title 4
    ##### Title 5
    ###### Title 6    

# Paragraph
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed dictum, nibh eu commodo posuere, ligula ante dictum neque, vitae pharetra mauris mi a velit. Phasellus eleifend egestas diam, id tincidunt arcu dictum quis. Pellentesque eu dui tempus, tempus massa sed, eleifend tortor. Donec in sem in erat iaculis tincidunt. Fusce condimentum hendrerit turpis nec vehicula. Aliquam finibus nisi vel eros lobortis dictum. Etiam congue tortor libero, quis faucibus ligula gravida a. Suspendisse non pulvinar nisl. Sed malesuada, felis vitae consequat gravida, dui ligula suscipit ligula, nec elementum nulla sem vel dolor. Vivamus augue elit, venenatis non lorem in, volutpat placerat turpis. Nullam et libero at eros vulputate auctor. Duis sed pharetra lacus. Sed egestas ligula vitae libero aliquet, ac imperdiet est ullamcorper. Sed dapibus sem tempus eros dignissim, ac suscipit lectus dapibus. Proin sagittis diam vel urna volutpat, vel ullamcorper urna lobortis. Suspendisse potenti.

Nulla varius risus sapien, nec fringilla massa facilisis sed. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nunc vel ornare erat, eget rhoncus lectus. Suspendisse interdum scelerisque molestie. Aliquam convallis consectetur lorem ut consectetur. Nullam massa libero, cursus et porta ac, consequat eget nibh. Sed faucibus nisl augue, non viverra justo sagittis venenatis.

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed dictum, nibh eu commodo posuere, ligula ante dictum neque, vitae pharetra mauris mi a velit. 
    
    Phasellus eleifend egestas diam, id tincidunt arcu dictum quis.

# List 
* Item 1;
	* Item 1.1;
* Item 2;
	* Item 2.1;
	* Item 2.2;
* Item 3
	* Item 3.1;
		* Item 3.1.1;
    
>      * Item 1;
>	      * Item 1.1;
>	    * Item 2;
>	     * Item 2.1;
>	     * Item 2.2;
>	    * Item 3
>		   * Item 3.1;
>			  * Item 3.1.1;

## List CheckBox

 - [ ] Item A
 - [x] Item B
 - [x] Item C
 
>     - [ ] Item A
>     - [x] Item B
>     - [x] Item C


# Link
[Google](https://www.google.com) - _Google | Youtube | Gmail | Maps | PlayStore | GoogleDrive_

[Youtube](https://www.youtube.com) - _Enjoy videos and music you love, upload original content, and share it with friends, family, and the world on YouTube._

[GitHub](https://github.com/fefong/markdown_readme#getting-started-with-markdown) - _Project_

		[Google](https://www.google.com) - _Google | Youtube | Gmail | Maps | PlayStore | GoogleDrive_

## Anchor links

[Markdown - Summary](#Getting-started-with-Markdown)

[Markdown - Markdown Editor](#Markdown-Editor)

		[Markdown - Link](#Link)

# Blockquote
> Lebenslangerschicksalsschatz: Lifelong Treasure of Destiny

    > Lebenslangerschicksalsschatz: Lifelong Treasure of Destiny 

# Image | GIF
![myImage](https://media.giphy.com/media/XRB1uf2F9bGOA/giphy.gif)
    
    ![myImage](https://media.giphy.com/media/XRB1uf2F9bGOA/giphy.gif)
    
See more [Markdown Extras - Image Align](https://github.com/fefong/markdown_readme/blob/master/markdown-extras.md#image-align)    

# Style Text
### Italic

*Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed dictum, nibh eu commodo posuere, ligula ante dictum neque, vitae pharetra mauris mi a velit.*

     *Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed dictum, nibh eu commodo posuere, ligula ante dictum neque, vitae pharetra mauris mi a velit.*

### Bold
**Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed dictum, nibh eu commodo posuere, ligula ante dictum neque, vitae pharetra mauris mi a velit.**

    **Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed dictum, nibh eu commodo posuere, ligula ante dictum neque, vitae pharetra mauris mi a velit.**
    
### Strikethrough
~~strikethrough text~~

    ~~strikethrough text~~
    
# Code

```java
public static void main(String[] args) {
	//TODO
}
```

>   \`\`\`java <br>
>   public static void main(String[] args) {<br>
>	    //TODO<br>
>	}<br>
>   \`\`\`<br>

See more [Markdown Extras - Style Text](https://github.com/fefong/markdown_readme/blob/master/markdown-extras.md#style-text)

# Email
<email@email.com>

    <email@email.com>

# Table

|Column 1|Column 2|Column 3|
|---|---|---|
|Row 1 Column1| Row 1 Column 2| Row 1 Column 3|
|Row 2 Column1| Row 2 Column 2| Row 2 Column 3|

>\|Column 1|Column 2|Column 3|<br>
>\|---|---|---|<br>
>\|Row 1 Column1| Row 1 Column 2| Row 1 Column 3|<br>
>\|Row 2 Column1| Row 2 Column 2| Row 2 Column 3|<br>

## Table Align

## Align Center

|Column 1|Column 2|Column 3|
|:---:|:---:|:---:|
|Row 1 Column1| Row 1 Column 2| Row 1 Column 3|
|Row 2 Column1| Row 2 Column 2| Row 2 Column 3|

>\|Column 1|Column 2|Column 3|<br>
>\|:---:|:---:|:---:|<br>
>\|Row 1 Column1| Row 1 Column 2| Row 1 Column 3|<br>
>\|Row 2 Column1| Row 2 Column 2| Row 2 Column 3|<br>

## Align Left

|Column 1|Column 2|Column 3|
|:---|:---|:---|
|Row 1 Column1| Row 1 Column 2| Row 1 Column 3|
|Row 2 Column1| Row 2 Column 2| Row 2 Column 3|

>\|Column 1|Column 2|Column 3|<br>
>\|:---|:---|:---|<br>
>\|Row 1 Column1| Row 1 Column 2| Row 1 Column 3|<br>
>\|Row 2 Column1| Row 2 Column 2| Row 2 Column 3|<br>

## Align Right

|Column 1|Column 2|Column 3|
|---:|---:|---:|
|Row 1 Column1| Row 1 Column 2| Row 1 Column 3|
|Row 2 Column1| Row 2 Column 2| Row 2 Column 3|

>\|Column 1|Column 2|Column 3|<br>
>\|---:|---:|---:|<br>
>\|Row 1 Column1| Row 1 Column 2| Row 1 Column 3|<br>
>\|Row 2 Column1| Row 2 Column 2| Row 2 Column 3|<br>

See more [Markdown Extras - Table](https://github.com/fefong/markdown_readme/blob/master/markdown-extras.md#table)
* [Rownspan](https://github.com/fefong/markdown_readme/blob/master/markdown-extras.md#table---rowspan)
* [Colspan](https://github.com/fefong/markdown_readme/blob/master/markdown-extras.md#table---colspan)

# Escape Characters

```
\   backslash
`   backtick
*   asterisk
_   underscore
{}  curly braces
[]  square brackets
()  parentheses
#   hash mark
+   plus sign
-   minus sign (hyphen)
.   dot
!   exclamation mark
```

# Emoji

* [Emoji](emoji.md#emoji);
	* [People](emoji.md#people) - (:blush: ; :hushed: ; :shit:);
	* [Nature](emoji.md#nature) - (:sunny: ; :snowman: ; :dog:);
	* [Objects](emoji.md#objects) - (:file_folder: ; :computer: ; :bell:);
	* [Places](emoji.md#places) - (:rainbow: ; :warning: ; :statue_of_liberty:);
	* [Symbols](emoji.md#symbols) - (:cancer: ; :x: ; :shipit:);
* [Kaomoji](emoji.md#kaomoji);
* [Special-Symbols](emoji.md#special-symbols);
	

# Shields Badges

:warning: _We are not responsible for this site_

See more: [https://shields.io/](https://shields.io/)

[![GitHub forks](https://img.shields.io/github/forks/fefong/markdown_readme)](https://github.com/fefong/markdown_readme/network)
![Markdown](https://img.shields.io/badge/markdown-project-red)

# Markdown Editor

[StackEdit](https://stackedit.io) - _StackEdit’s Markdown syntax highlighting is unique. The refined text formatting of the editor helps you visualize the final rendering of your files._

# Some links for more in depth learning

:page_facing_up: [Markdown Extras](https://github.com/fefong/markdown_readme/blob/master/markdown-extras.md#markdown---extras)

:page_facing_up: [Wikipedia - Markdown](https://pt.wikipedia.org/wiki/Markdown)

:page_facing_up: [Oficial](https://daringfireball.net/projects/markdown/)



Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

</details>

<details><summary>Cool Dropdown #2</summary>

More cool text hiding in my dropdown

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

## test

Getting started with Markdown
=============================


- [Getting started with Markdown](#getting-started-with-markdown)
- [Titles](#titles)
- [Paragraph](#paragraph)
- [List](#list)
	- [List CheckBox](#list-checkbox)
- [Link](#link)
	- [Anchor links](#anchor-links)
- [Blockquote](#blockquote)
- [Image | GIF](#image--gif)
- [Style Text](#style-text)
	- [Italic](#italic)
	- [Bold](#bold)
	- [Strikethrough](#strikethrough)
- [Code](#code)
- [Email](#email)
- [Table](#table)
	- [Table Align](#table-align)
    	- [Align Center](#align-center)
    	- [Align Left](#align-left)
    	- [Align Right](#align-right)
- [Escape Characters](#escape-characters)
- [Emoji](#emoji)
- [Shields Badges](#Shields-Badges)
- [Markdown Editor](#markdown-editor)
- [Some links for more in depth learning](#some-links-for-more-in-depth-learning)

----------------------------------

# Titles 

### Title 1
### Title 2

	Title 1
	========================
	Title 2 
	------------------------

# Title 1
## Title 2
### Title 3
#### Title 4
##### Title 5
###### Title 6

    # Title 1
    ## Title 2
    ### Title 3    
    #### Title 4
    ##### Title 5
    ###### Title 6    

# Paragraph
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed dictum, nibh eu commodo posuere, ligula ante dictum neque, vitae pharetra mauris mi a velit. Phasellus eleifend egestas diam, id tincidunt arcu dictum quis. Pellentesque eu dui tempus, tempus massa sed, eleifend tortor. Donec in sem in erat iaculis tincidunt. Fusce condimentum hendrerit turpis nec vehicula. Aliquam finibus nisi vel eros lobortis dictum. Etiam congue tortor libero, quis faucibus ligula gravida a. Suspendisse non pulvinar nisl. Sed malesuada, felis vitae consequat gravida, dui ligula suscipit ligula, nec elementum nulla sem vel dolor. Vivamus augue elit, venenatis non lorem in, volutpat placerat turpis. Nullam et libero at eros vulputate auctor. Duis sed pharetra lacus. Sed egestas ligula vitae libero aliquet, ac imperdiet est ullamcorper. Sed dapibus sem tempus eros dignissim, ac suscipit lectus dapibus. Proin sagittis diam vel urna volutpat, vel ullamcorper urna lobortis. Suspendisse potenti.

Nulla varius risus sapien, nec fringilla massa facilisis sed. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nunc vel ornare erat, eget rhoncus lectus. Suspendisse interdum scelerisque molestie. Aliquam convallis consectetur lorem ut consectetur. Nullam massa libero, cursus et porta ac, consequat eget nibh. Sed faucibus nisl augue, non viverra justo sagittis venenatis.

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed dictum, nibh eu commodo posuere, ligula ante dictum neque, vitae pharetra mauris mi a velit. 
    
    Phasellus eleifend egestas diam, id tincidunt arcu dictum quis.

# List 
* Item 1;
	* Item 1.1;
* Item 2;
	* Item 2.1;
	* Item 2.2;
* Item 3
	* Item 3.1;
		* Item 3.1.1;
    
>      * Item 1;
>	      * Item 1.1;
>	    * Item 2;
>	     * Item 2.1;
>	     * Item 2.2;
>	    * Item 3
>		   * Item 3.1;
>			  * Item 3.1.1;

## List CheckBox

 - [ ] Item A
 - [x] Item B
 - [x] Item C
 
>     - [ ] Item A
>     - [x] Item B
>     - [x] Item C


# Link
[Google](https://www.google.com) - _Google | Youtube | Gmail | Maps | PlayStore | GoogleDrive_

[Youtube](https://www.youtube.com) - _Enjoy videos and music you love, upload original content, and share it with friends, family, and the world on YouTube._

[GitHub](https://github.com/fefong/markdown_readme#getting-started-with-markdown) - _Project_

		[Google](https://www.google.com) - _Google | Youtube | Gmail | Maps | PlayStore | GoogleDrive_

## Anchor links

[Markdown - Summary](#Getting-started-with-Markdown)

[Markdown - Markdown Editor](#Markdown-Editor)

		[Markdown - Link](#Link)

# Blockquote
> Lebenslangerschicksalsschatz: Lifelong Treasure of Destiny

    > Lebenslangerschicksalsschatz: Lifelong Treasure of Destiny 

# Image | GIF
![myImage](https://media.giphy.com/media/XRB1uf2F9bGOA/giphy.gif)
    
    ![myImage](https://media.giphy.com/media/XRB1uf2F9bGOA/giphy.gif)
    
See more [Markdown Extras - Image Align](https://github.com/fefong/markdown_readme/blob/master/markdown-extras.md#image-align)    

# Style Text
### Italic

*Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed dictum, nibh eu commodo posuere, ligula ante dictum neque, vitae pharetra mauris mi a velit.*

     *Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed dictum, nibh eu commodo posuere, ligula ante dictum neque, vitae pharetra mauris mi a velit.*

### Bold
**Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed dictum, nibh eu commodo posuere, ligula ante dictum neque, vitae pharetra mauris mi a velit.**

    **Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed dictum, nibh eu commodo posuere, ligula ante dictum neque, vitae pharetra mauris mi a velit.**
    
### Strikethrough
~~strikethrough text~~

    ~~strikethrough text~~
    
# Code

```java
public static void main(String[] args) {
	//TODO
}
```

>   \`\`\`java <br>
>   public static void main(String[] args) {<br>
>	    //TODO<br>
>	}<br>
>   \`\`\`<br>

See more [Markdown Extras - Style Text](https://github.com/fefong/markdown_readme/blob/master/markdown-extras.md#style-text)

# Email
<email@email.com>

    <email@email.com>

# Table

|Column 1|Column 2|Column 3|
|---|---|---|
|Row 1 Column1| Row 1 Column 2| Row 1 Column 3|
|Row 2 Column1| Row 2 Column 2| Row 2 Column 3|

>\|Column 1|Column 2|Column 3|<br>
>\|---|---|---|<br>
>\|Row 1 Column1| Row 1 Column 2| Row 1 Column 3|<br>
>\|Row 2 Column1| Row 2 Column 2| Row 2 Column 3|<br>

## Table Align

## Align Center

|Column 1|Column 2|Column 3|
|:---:|:---:|:---:|
|Row 1 Column1| Row 1 Column 2| Row 1 Column 3|
|Row 2 Column1| Row 2 Column 2| Row 2 Column 3|

>\|Column 1|Column 2|Column 3|<br>
>\|:---:|:---:|:---:|<br>
>\|Row 1 Column1| Row 1 Column 2| Row 1 Column 3|<br>
>\|Row 2 Column1| Row 2 Column 2| Row 2 Column 3|<br>

## Align Left

|Column 1|Column 2|Column 3|
|:---|:---|:---|
|Row 1 Column1| Row 1 Column 2| Row 1 Column 3|
|Row 2 Column1| Row 2 Column 2| Row 2 Column 3|

>\|Column 1|Column 2|Column 3|<br>
>\|:---|:---|:---|<br>
>\|Row 1 Column1| Row 1 Column 2| Row 1 Column 3|<br>
>\|Row 2 Column1| Row 2 Column 2| Row 2 Column 3|<br>

## Align Right

|Column 1|Column 2|Column 3|
|---:|---:|---:|
|Row 1 Column1| Row 1 Column 2| Row 1 Column 3|
|Row 2 Column1| Row 2 Column 2| Row 2 Column 3|

>\|Column 1|Column 2|Column 3|<br>
>\|---:|---:|---:|<br>
>\|Row 1 Column1| Row 1 Column 2| Row 1 Column 3|<br>
>\|Row 2 Column1| Row 2 Column 2| Row 2 Column 3|<br>

See more [Markdown Extras - Table](https://github.com/fefong/markdown_readme/blob/master/markdown-extras.md#table)
* [Rownspan](https://github.com/fefong/markdown_readme/blob/master/markdown-extras.md#table---rowspan)
* [Colspan](https://github.com/fefong/markdown_readme/blob/master/markdown-extras.md#table---colspan)

# Escape Characters

```
\   backslash
`   backtick
*   asterisk
_   underscore
{}  curly braces
[]  square brackets
()  parentheses
#   hash mark
+   plus sign
-   minus sign (hyphen)
.   dot
!   exclamation mark
```

# Emoji

* [Emoji](emoji.md#emoji);
	* [People](emoji.md#people) - (:blush: ; :hushed: ; :shit:);
	* [Nature](emoji.md#nature) - (:sunny: ; :snowman: ; :dog:);
	* [Objects](emoji.md#objects) - (:file_folder: ; :computer: ; :bell:);
	* [Places](emoji.md#places) - (:rainbow: ; :warning: ; :statue_of_liberty:);
	* [Symbols](emoji.md#symbols) - (:cancer: ; :x: ; :shipit:);
* [Kaomoji](emoji.md#kaomoji);
* [Special-Symbols](emoji.md#special-symbols);
	

# Shields Badges

:warning: _We are not responsible for this site_

See more: [https://shields.io/](https://shields.io/)

[![GitHub forks](https://img.shields.io/github/forks/fefong/markdown_readme)](https://github.com/fefong/markdown_readme/network)
![Markdown](https://img.shields.io/badge/markdown-project-red)

# Markdown Editor

[StackEdit](https://stackedit.io) - _StackEdit’s Markdown syntax highlighting is unique. The refined text formatting of the editor helps you visualize the final rendering of your files._

# Some links for more in depth learning

:page_facing_up: [Markdown Extras](https://github.com/fefong/markdown_readme/blob/master/markdown-extras.md#markdown---extras)

:page_facing_up: [Wikipedia - Markdown](https://pt.wikipedia.org/wiki/Markdown)

:page_facing_up: [Oficial](https://daringfireball.net/projects/markdown/)


