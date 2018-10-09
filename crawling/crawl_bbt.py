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
def Breitbart_crawl(url, i = 10**9, path = os.getcwd(), return_ans = False):
    if re.search('^(([^:/?#]+):)?(//([^/?#]*))?',url).groups()[-1] !=  'www.breitbart.com': #check if url host matches
        print('Please input url from www.breitbart.com')
        return
    browser = webdriver.Chrome()
    browser.get(url)
    urls = []
    more_pages = True

#%%
    def scrape(url_list):
        innerHTML = browser.execute_script("return document.body.innerHTML") #get html after page loads
        soup = bs4.BeautifulSoup(innerHTML,'html.parser') #parse html
        for item in soup.select('div[class="grp-content"] > h2[class="title"] > a'): #search html for urls
            url_list.append((item['href'],'BBT')) #ad urls to list

#%%
    while more_pages and len(set(urls)) < i:
        try:
            element = WebDriverWait(browser, 10).until( #load page for a max of 10 seconds
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="pagination"] > div[class="alignleft"] > a'))) #until element loads
            next_button = browser.find_element_by_css_selector('div[class="pagination"] > div[class="alignleft"] > a') #get next page button
            scrape(urls)
            next_button.click() #go to next page
            sleep(1.5)
            try:
                close_box = browser.find_element_by_css_selector('span[data-fancybox-close=""]') #if ad box pops up, get close button
                close_box.click() #close ad box
            except NoSuchElementException: #if no ad box do nothing
                continue
                
        except ElementNotVisibleException or StaleElementReferenceException: #if button exists but not found
            browser.refresh() #refresh and try again
            sleep(1.5)
        except NoSuchElementException: #if no such element
            more_pages = False #then no more pages
            continue
        except Exception as e: #any other issues
            urls = list(set(urls)) #clean up list
            print('Encountered unexpected problem')
            print(e)
            print(f'Scraped {len(urls)} urls')
            filename = path + f'\\{len(urls)}_bbt_urls.json' #emergency save
            with open(filename, 'w') as outfile:  
                json.dump(urls, outfile)
            if return_ans:
                return urls
            else:
                return
        
#%%
    urls = list(set(urls)) #when done scraping, clean up list
    browser.close() #close browser
    filename = path + '\\breitbart_urls.json' #save to json
    with open(filename, 'w') as outfile:  
        json.dump(urls, outfile)
    winsound.PlaySound('ding.wav', winsound.SND_FILENAME) #notify user
    if return_ans: #if answer wanted, return answer
        return urls