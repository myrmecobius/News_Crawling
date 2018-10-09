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
def ABC_crawl(url, i = 10**9, path = os.getcwd(), return_ans = False):
    if re.search('^(([^:/?#]+):)?(//([^/?#]*))?',url).groups()[-1] != 'abcnews.go.com': #check if url host matches
        print('Please input url from abcnews.go.com')
        return
    browser = webdriver.Chrome()
    browser.get(url)
    urls = []
    more_pages = True

#%%
    def scrape(url_list):
        innerHTML = browser.execute_script("return document.body.innerHTML") #get html after everything has loaded
        soup = bs4.BeautifulSoup(innerHTML,'html.parser') #parse html to make it easier to search
        for item in soup.select('div[class*="result"] > a[class="title"]'): #find the tags corresponding to urls
            url_list.append((item['href'],'ABC')) #and add them all to list
    

    element = WebDriverWait(browser, 10).until( #waits for page to load for a max of ten seconds
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="pager"] > a[class="page"]'))) #or until we find the next page button
    next_button = browser.find_element_by_css_selector('div[class="pager"] > a[class="page"]') #save reference to next page button
    scrape(urls)
    next_button.click() #click next page button
    sleep(1) #give page one second to load just in case

#%%
    while more_pages and len(set(urls)) < i:
        try:
            element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="pager"] > a + a'))) #for any page that has a previous page button
            next_button = browser.find_element_by_css_selector('div[class="pager"] > a + a') #choose button after previous, which should be next
            scrape(urls)
            next_button.click()
            sleep(1.5)
                
        except ElementNotVisibleException or StaleElementReferenceException: #if element not visible but exists or link is stale
            browser.refresh() #refresh and try again
            sleep(1.5)
        except NoSuchElementException: #if no such element
            more_pages = False #then assume no more pages, while loop terminates
            continue
        except Exception as e: #any other errors
            urls = list(set(urls)) #clean up urls
            print('Encountered unexpected problem')
            print(e)
            print(f'Scraped {len(urls)} urls')
            filename = path + f'\\{len(urls)}_abc_urls.json' #conduct emergency save
            with open(filename, 'w') as outfile:  
                json.dump(urls, outfile)
            if return_ans:
                return urls
            else:
                return
        
#%%
    urls = list(set(urls)) #clean up url list
    browser.close()
    filename = path + '\\abc_urls.json'
    with open(filename, 'w') as outfile: #save urls as json
        json.dump(urls, outfile)
    winsound.PlaySound('ding.wav', winsound.SND_FILENAME) #play sound to notify user
    if return_ans: #if answer wanted, return it
        return urls
    
    