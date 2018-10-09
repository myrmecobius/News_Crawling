# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 13:07:40 2018

@author: theor
"""

from selenium import webdriver
import bs4
import os
import re
from selenium.common.exceptions import NoSuchElementException,ElementNotVisibleException,StaleElementReferenceException
from time import sleep
import json
import winsound
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#%%
def WashPost_crawl(url, i = 10**9, path = os.getcwd(), return_ans = False):
    if re.search('^(([^:/?#]+):)?(//([^/?#]*))?',url).groups()[-1] != 'www.washingtonpost.com': #check host url matches
        print('Please input url from www.washingtonpost.com')
        return
    browser = webdriver.Chrome()
    browser.get(url)
    urls = []
    more_pages = True

#%%
    def scrape(url_list):
        innerHTML = browser.execute_script("return document.body.innerHTML") #get html after page loads
        soup = bs4.BeautifulSoup(innerHTML,'html.parser') #parse html
        for item in soup.select('a[data-ng-bind-html="doc.headline"]'): #find elements with urls
            url = item['data-ng-href']
            url_list.append((url,'WPT')) #add urls to list

#%%        
    while more_pages and len(set(urls)) < i:
        try:
            element = WebDriverWait(browser, 10).until( #wait for element to load for max of 10 seconds
            EC.presence_of_element_located((By.CSS_SELECTOR, 'li[class="pagination-next ng-scope"] > a'))) #this element
            next_button = browser.find_element_by_css_selector('li[class="pagination-next ng-scope"] > a') #get pagination arrow
            scrape(urls)
            next_button.click() #go to next page
            sleep(1.5)
        except ElementNotVisibleException or StaleElementReferenceException: #if element exists but is not found
            browser.refresh() #refresh and try again
            sleep(1.5)
        except NoSuchElementException: #if element does not exist
            more_pages = False #no more pages
            continue
        except Exception as e: #any other errors
            broken = True
            urls = list(set(urls)) #clean up urls
            print('Encountered unexpected problem')
            print(e)
            print(f'Scraped {len(urls)} urls')
            filename = path + f'\\{len(urls)}_wpt_urls.json' #conduct emergency save
            with open(filename, 'w') as outfile:  
                json.dump(urls, outfile)
            if return_ans:
                return urls
            else:
                return

#%%
    urls = list(set(urls)) #after while loop, clean up list
    browser.close()
    filename = path + '\\wpt_urls.json'
    with open(filename, 'w') as outfile:  #save data as json file
        json.dump(urls, outfile)
    winsound.PlaySound('ding.wav', winsound.SND_FILENAME) #notify user
    if return_ans:
        return urls