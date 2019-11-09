# Doctissimo: A Multilingual Dialogue Dataset Technical Description of Corpus
# Applied Machine Learning, Dr. Joelle Pineau

## Authors:
  * Amanda Boatswain Jacques
  * Taha Ghassemi
  * AhmadReza GodarvandChegini

### Abstract:

### I.    INTRODUCTION

   We assembled a corpus of conversations on the French-language health forum on Doctissimo.fr using data from the year of 2015. 

Forum URL: http://forum.doctissimo.fr/
Corpus URL: https://drive.google.com/open?id=0B7z3HM2_6X-LVzVnT0hpRm5LaVE

### II.    DATASET DESCRIPTION 

#### Website Content 
   Our language corpus was created by compiling a set of French conversations retrieved from the medical forum Doctissimo. These conversations correspond to threads, posts, and discussions between users of the website over the two years. The Doctissimo forum is a website where thousands of users can discuss various health-related topics such as medication, nutrition, psychology, family, animals and more. Messages and replies on the forum consist primarily of people who are either seeking medical advice from online doctors, seeking opinions and recommendations from other users, or who would like to pursue conversations centered around a shared topic of interest. This allows for a certain degree of formality and minimal structure in the utterances of each user, and reduces the occasional collection of random and nonsensical conversation that is commonly found in online chat rooms. Moreover, the site has a directory of threads that are dated from the year 2000 to this very day, and some individual categories contain over 4 million user replies, showing potential for the creation of a dataset rich in diversity, length and complexity.  

#### Code Architecture 
   To generate our corpus, we used a method known as web scraping. Web scraping is done by programmatically accessing a webpage, downloading it and extracting information from it [1].
 A custom-made web crawler was designed for the Doctissimo site to fetch each page selected to create our corpus. The crawler follows all the links of the provided webpage until it has explored all the required links [2]. 
   Our scraping software was built in the Python language (ver 3.0) using a library named Scrapy. First, we create an object of the scrapy.Spider class which will proceed to collect information from the entire forum. The forum is organized into individual topics which each correspond to a single URL or request. This master list is passed to a Spider which will download the corresponding webpage. A URL detection pattern for the webpage is created so the scraper can retrieve pages related to a specific category within a given year and month. Once the information is retrieved, we continue by parsing the content of the page, and then search for all recorded thread topics and the posts related to them [3].
   The Scrapy architecture has multiple components that interact with each other to provide a steady and rapid flow of data.  These components include the Scrapy Engine, the Scheduler, the Downloader, the Spider, the Item Pipeline. The Engine controls the overall data flow, and sends requests to the Scheduler which will enqueue these webpages before they are fed to the Downloader. The Downloader will then call on the Spider to parse and extract information from the webpage. Once this is completed, the data is sent to the Item Pipeline, which will format it and then save it. The process will continue until all the requests stored by the Scheduler have been scraped. Figure below represents a flow diagram of the Scrapy architecture [3]:


<p align="center">
  <img src="Scrapy_arch.png?raw=true" alt="Architecture of a Scrapy Engine" title="Architecture of a Scrapy Engine" width=500 />
</p>

   After creating our Scrapy architecture, we proceeded 
by filtering the raw data from the webpages. The pages searched were dated from the entire year of 2015, some of the specifics of our corpus are reported in table below. 


Utterances | Words | turn | Conversations
--- | --- | --- | ---
291643 | 19643940 | 291479 | 9185
  
   To guarantee an appropriate number of utterances per conversation, we limited our search to all threads that had at least 3 replies. Replies which consisted of images or “emojis” were removed to restrict our corpus to French text. As a result, comments which consisted of only these things were omitted.   
    Utterances were separated between users using a system of UUIDs or universally unique identifiers. These were 16-byte character strings which were derived using the SHA-1 hash function. This was done to guarantee anonymity between users while keeping them traceable. Thus, if a user posted a message in more than one thread, they would have the same UUID in the corpus [4]. Users which had a generic tag of “deleted account” were omitted from the dataset to avoid appearing to be the same person. Utterances that spanned over multiple paragraphs were separated with the help of a special token for paragraph breaks, `<br>`. This allowed our dataset to gain another interesting dimension for testing. By keeping the users retraceable, researches could study conversation patterns of various users (whether they utter one-line sentences, or prefer longer, more complete replies).

### III.    DISCUSSION  
  
   Our corpus is primarily composed of French human-human conversations corresponding to casual spoken language.  As stated by Serban et al., written and spoken language show difference in their individual structures [5]. Therefore, it has many unique properties such as the presence of abbreviations and slang. It is almost completely organic, with little processing performed on the content. The forum is mostly centered around medical advice, but there is a breath of topics, and conversations range from serious to lighthearted. This could be an appropriate dataset for training a model that would aim to recognize and mimic everyday French language. A full list of all the topics on the Doctissimo site can be found below, and it is important to note that these topics are further divided into sub-topics or categories ranging from 10 to 100 per topic:
   
1. Health
2. Pregnancy and Babies 3. Fashion
4. Beauty
5. Nutrition
6. Psychology
7. Sexuality
8. Leisure
9. People
10. Medication
11. Fitness and Sports
12. Practical Life
13. Animals
14. Family
15. Cooking

   Many existing French corpuses are composed of individual words, such as Lexique3, developed by the University of Savoie Mont-Blanc (150 000 words) [6]. Another French Corpus known as the Corpus Frantext, which was developed by the University of Nancy, contains 500 pieces of French literature from the 18th to 20th centuries [7]. Our corpus differs from these two for it is mostly composed of common French sentences, and it is more complex than individual words but less formal than literature. 

### IV.    STATEMENT OF CONTRIBUTIONS   

   Amanda Boatswain Jacques wrote a generous portion of the report and made minor contributions to the code. Mr. Godarzvand Chegini wrote most of the Python program. Mr. Ghassemi contributed to the code and writing/proofreading the report. We hereby state that all the work presented in this report is that of the authors.






### V.    REFERENCES  

1.	Web Scraping. (n.d.). In Wikipedia. Retrieved September 23rd, 2017. From: https://en.wikipedia.org/wiki/-Web_scraping

2.	Import.io. “How to Crawl a Website the Right Way.” Retrieved September 23rd, 2017. From: https://www.import.io/post/how-to-crawl-a-website-the-right-way/

3.	Scrapy Documentation. “Architecture Structure.” Retrieved September 23rd, 2017. From: https://doc.scrapy.org/en/latest/topics/-architecture.html

4.	The Python Standard Library. “ 20.15. uuid -  UUID objects according to RFC 4122”. Retrieved   September 24th, 2017.	  
From:https://docs.python.org/2/-library/uuid.html

5.	I. Serban, R. Lowe, P. Henderson, L. Charlin, J. Pineau. “A Survey of Available Corpora for Building Data-Driven Dialogue Systems.” Cornell University Library. arXiv:1512.05742 [cs.CL] March 2017. 

6.	Université de Savoie Mont-Blanc. “Lexique.” Retrieved September 27th, 2017, From: http://www.lexique.org/telLexique.php

7.	Ortolang. “Corpus Frantext.” Retrieved September 27th, 2017. From: http://www.cnrtl.fr/corpus/frantext/




