# News-Front-Page-Scraper
Web scraping the front pages of news sites.

Webscraping project for Foxnews.com and cnn.com front pages \n
Scraper auto scrapes everyday at 9:00 am.
Returns results in csv file. 

COLUMNS:
- headline: headline
- category: news category
- publish_date: article publish date
- access_date: date article was scraped on 
- video: indicates if article is a video 
- url: article url

Future Improvements:
- need to find a way to get publish_date for FOXnews articles
- fixes on publish_date for subset of CNNnews articles
- may have some bugs in the category encodings
- add author names into scrapes
