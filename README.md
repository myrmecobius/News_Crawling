# News_Crawling
A set of python scripts to crawl news websites' search pages and scrape article URLs and text

## Supported Sites
- ABC News
- Breitbart
- CBS News
- CNN
- Fox News
- The Hill
- New York Times
- Politico
- USA Today
- Washington Post

## Getting Started
### Inputs and Outputs
#### Crawling
##### Inputs
Currently all crawling functions take in four parameters:

- URL: website to be scraped.
The script compares the url host with a list of compatible hosts before executing.

- i: target number of articles (defaulted to 10**9)

- path: where the list of scraped urls is to be stored
Default path is current Python directory

- return_ans: should the list be returned in addition to being saved (default False)

##### Outputs
All crawling scripts upon completion will save the resulting list of URLs as a json file in the path specified.
It will then play a sound to alert the user that the process has concluded and terminate.

In case of some error that was not accounted for, the function will save the list of URLs that it has scraped up until that point before terminating.
It will return the length of the URL list and include that number in the name of the saved file.

#### Scraping
##### Input
The generalized scraping function takes in four parameters:

- filename: name of json file (obtained from crawl function) from which to scrape

- path: where to save the data upon scraping completion
Default path is current Python directory

- start: which element in the list to start scraping from (default 0)

- return_ans: should the list be returned in addition to being saved (default False)

Specific scraping functions take only the URL as input.

##### Output
The generalized scraping function will save the resulting list of article text upon completion in the path specified.

If an error arises, it will save all the article text scraped so far before terminating.
Before terminating, it will display the list index that caused the error, so the user can resume from that index or skip it if necessary.
