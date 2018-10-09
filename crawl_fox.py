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
def Fox_crawl(url, i = 10**9, path = os.getcwd(), return_ans = False):
    if re.search('^(([^:/?#]+):)?(//([^/?#]*))?',url).groups()[-1] != 'www.foxnews.com': #check url host matches
        print('Please input url from www.foxnews.com')
        return
    browser = webdriver.Chrome()
    browser.get(url)
    urls = []
    more_pages = True

#%%
    def scrape(url_list):
        innerHTML = browser.execute_script("return document.body.innerHTML") #get html after page laods
        soup = bs4.BeautifulSoup(innerHTML,'html.parser') #parse html
        for aItem in soup.select('h3 > a[href]'): #find all elements containing possible links
            try:
                if 'ng-binding' in aItem['class']: #if class is specified
                    url = aItem['href']
                    url_list.append((url,'FOX')) #add item to list
            except: continue
        
#%%
    while more_pages and len(set(urls)) < i:
        try:
            element = WebDriverWait(browser, 10).until( #wait for element to load for max of 10 seconds
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[ng-click="com(\'next\')"]'))) #for this element
            next_button = browser.find_element_by_css_selector('a[ng-click="com(\'next\')"]') #get pagination arrow
            scrape(urls)
            next_button.click() #go to next page
            browser.refresh()
        except ElementNotVisibleException or StaleElementReferenceException: #if element exists but isn't found
            browser.refresh() #refresh and try again
            sleep(1.5)
        except NoSuchElementException: #if element does not exist
            more_pages = False #no more pages
            continue
        except Exception as e: #any other error
            urls = list(set(urls)) #clean up list
            print('Encountered unexpected problem')
            print(e)
            print(f'Scraped {len(urls)} urls')
            filename = path + f'\\{len(urls)}_fox_urls.json' #emergency save
            with open(filename, 'w') as outfile:  
                json.dump(urls, outfile)
            if return_ans:
                return urls
            else:
                return
        
#%%
    urls = list(set(urls)) #after while loop concludes, clean up list
    browser.close()
    filename = path + '\\fox_urls.json'
    with open(filename, 'w') as outfile:  #save data as json
        json.dump(urls, outfile)
    winsound.PlaySound('ding.wav', winsound.SND_FILENAME) #notify user
    if return_ans:
        return urls