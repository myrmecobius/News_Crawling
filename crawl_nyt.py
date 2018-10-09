from selenium import webdriver
import bs4
import os
import re
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import json
import winsound
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#%%
def NYT_crawl(url, i = 10**9, path = os.getcwd(), return_ans = False):
    if re.search('^(([^:/?#]+):)?(//([^/?#]*))?',url).groups()[-1] != 'www.nytimes.com': #check url host matches
        print('Please input url from www.nytimes.com')
        return
    browser = webdriver.Chrome()
    browser.get(url)
    urls = []
    more_pages = True
    clicks = (i - 10)//10 #calculate number of times page needs to be extended
    j = 0 #initiate counter

#%%
    while more_pages and j < clicks:
        try:
            next_button = browser.find_element_by_css_selector('div.Search-showMoreWrapper--1Z88y') #get show more wrapper
            next_button.click() #click to show more urls
            j += 1 #incrment counter
            sleep(2.5)
        except NoSuchElementException: #if no button
            more_pages = False #no more pages
        except Exception as e: #any other errors
            innerHTML = browser.execute_script("return document.body.innerHTML") #get html
            soup = bs4.BeautifulSoup(innerHTML,'html.parser') #parse html
            for item in soup.select('div[class*="Item-wrapper--2ba8L"]'): #find elements with urls
                url_link = 'https://www.nytimes.com' + item.find_all('a')[0]['href'] #construct urls
                urls.append((url_link,'NYT')) #add url to list
            urls = list(set(urls)) #clean up urls
            print('Encountered unexpected problem')
            print(e)
            print(f'Scraped {len(urls)} urls')
            filename = path + f'\\{len(urls)}_nyt_urls.json' #conduct emergency save
            with open(filename, 'w') as outfile:  
                json.dump(urls, outfile)
            if return_ans:
                return urls
            else:
                return

#%%    
    innerHTML = browser.execute_script("return document.body.innerHTML") #get html
    soup = bs4.BeautifulSoup(innerHTML,'html.parser') #parse html
    for item in soup.select('div[class*="Item-wrapper--2ba8L"]'): #find elements with urls
        url_link = 'https://www.nytimes.com' + item.find_all('a')[0]['href'] #construct urls
        urls.append((url_link,'NYT')) #add url to list
        
#%%
    urls = list(set(urls)) #clean list
    browser.close()
    filename = path + '\\nyt_urls.json'
    with open(filename, 'w') as outfile:  #save data as json
        json.dump(urls, outfile)
    winsound.PlaySound('ding.wav', winsound.SND_FILENAME) #notify user
    if return_ans: #return answer if wanted
        return urls
    