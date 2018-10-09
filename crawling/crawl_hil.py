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
def Hill_crawl(url, i = 10**9, path = os.getcwd(), return_ans = False):
    if re.search('^(([^:/?#]+):)?(//([^/?#]*))?',url).groups()[-1] != 'thehill.com': #check if url host matches
        print('Please input url from thehill.com')
        return
    browser = webdriver.Chrome()
    browser.get(url)
    urls = []
    more_pages = True

#%%
    def scrape(url_list):
        innerHTML = browser.execute_script("return document.body.innerHTML") #get html after page loads
        soup = bs4.BeautifulSoup(innerHTML,'html.parser') #parse html
        for item in soup.select('span[class="social-share-count"]'): #find elements that contain urls
            url_list.append((item['data-href'],'HIL')) #add urls to list

#%%    
    while more_pages and len(set(urls)) < i:
        try:
            element = WebDriverWait(browser, 10).until( #wait for element to load for max of 10 seconds
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[title="Go to next page"]'))) #waiting for this element
            next_button = browser.find_element_by_css_selector('a[title="Go to next page"]') #get pagination arrow
            scrape(urls)
            next_button.click() #go to next page
            sleep(1.5)
        except ElementNotVisibleException or StaleElementReferenceException: #if element exists but isn't found
            browser.refresh() #refresh and try again
            sleep(1.5)
        except NoSuchElementException: #if element does not exist
            more_pages = False #no more pages
        except Exception as e: #any other errors
            urls = list(set(urls)) #clean up urls
            print('Encountered unexpected problem')
            print(e)
            print(f'Scraped {len(urls)} urls')
            filename = path + f'\\{len(urls)}_hill_urls.json' #conduct emergency save
            with open(filename, 'w') as outfile:  
                json.dump(urls, outfile)
            if return_ans:
                return urls
            else:
                return

#%%
    urls = list(set(urls)) #after while loop, clean up list
    browser.close()
    filename = path + '\\hill_urls.json'
    with open(filename, 'w') as outfile:  #save data as json file
        json.dump(urls, outfile)
    winsound.PlaySound('ding.wav', winsound.SND_FILENAME) #notify user
    if return_ans: #return answers if wanted
        return urls