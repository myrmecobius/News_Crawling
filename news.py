#%% Load packages
import os
import re
import json
import winsound
import sys

#%%
def get_site(url):
    match = re.search('^(([^:/?#]+):)?(//([^/?#]*))?',url) #gets url base
    return match.groups()[-1] #removes https://

#%%
def crawl(url, i = 10**9, path = os.getcwd(), return_ans = False): #scrapes some number i of urls from supported news pages
    if 'crawling' not in sys.path: #if crawling folder is not accessible
        sys.path.append('crawling') #add crawling folder to current path
    siteDict = {'abcnews.go.com':('abc','ABC_crawl'), #dictionary of child functions and file paths
        'www.breitbart.com':('bbt','Breitbart_crawl'),
        'www.cbsnews.com':('cbs','CBS_crawl'),
        'www.cnn.com':('cnn','CNN_crawl'),
        'www.foxnews.com':('fox','Fox_crawl'),
        'thehill.com':('hil','Hill_crawl'),
        'www.nytimes.com':('nyt','NYT_crawl'),
        'www.politico.com':('pol','Politico_crawl'),
        'www.usatoday.com':('usa','USA_crawl'),
        'www.washingtonpost.com':('wpt','WashPost_crawl')}
    if not siteDict.get(get_site(url)): #if site not defined in dict
        print('Website not supported') #currently not supported
        return
    load_cmd = f'from crawl_{siteDict[get_site(url)][0]} import {siteDict[get_site(url)][1]}' #construct load module command
    exec(load_cmd) #execute load module command
    command = f'{siteDict[get_site(url)][1]}("{url}",i = {i},path = {path},return_ans = {return_ans})' #construct function command
    urls = eval(command) #call function command
    if return_ans: #if want answer returned
        return urls #return answers

#%%
def scrape(filename, path = os.getcwd(), start = 0, return_ans = False): #scrapes urls for article given a json file
    if 'scraping' not in sys.path: #if scraping folder is not accessible
        sys.path.append('scraping') #add scraping folder to current path
    with open(filename) as file:
        urls = json.load(file)
    article_text = []
    codeDict = {'ABC':'abc',
                 'BBT':'bbt',
                 'CBS':'cbs',
                 'CNN':'cnn',
                 'FOX':'fox',
                 'HIL':'hil',
                 'NYT':'nyt',
                 'POL':'pol',
                 'USA':'usa',
                 'WPT':'wpt'}
    try:
        for i in range(0,len(urls)):
            url = urls[i][0]
            code = urls[i][1]
            if not codeDict.get(code):
                print('Website not supported')
                return
            load_cmd = f'from scrape_{codeDict[code]} import {codeDict[code]}_scrape'
            exec(load_cmd)
            command = f'{codeDict[code]}_scrape("url",path = "{path}", start = {start}, return_ans = {return_ans})'
            text = eval(command)
            article_text.append(text)
    except: #if something goes wrong
        filename = path + f'\\{code}_text_to_{i}.json' #define filename
        with open(filename, 'w') as outfile: #save data as json 
            json.dump(article_text, outfile)
        print(f'Terminated at {i} articles') #note progress
        if return_ans: #if answer wanted, return ans
            return urls
        
    filename = path + f'\\{code}_text.json' #if nothing goes wrong
    with open(filename, 'w') as outfile: #save data as json 
        json.dump(article_text, outfile)
    winsound.PlaySound('ding.wav', winsound.SND_FILENAME) #notify user
    if return_ans: #if answer wanted, return ans
        return urls







