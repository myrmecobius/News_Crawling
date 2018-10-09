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
def CBS_crawl(url, i = 10**9, path = os.getcwd(), return_ans = False):
    if re.search('^(([^:/?#]+):)?(//([^/?#]*))?',url).groups()[-1] != 'www.cbsnews.com': #check if url host matches
        print('Please input url from www.cbsnews.com')
        return
    browser = webdriver.Chrome()
    browser.get(url)
    urls = []
    more_pages = True
    def scrape(url_list):

        #%%
        innerHTML = browser.execute_script("return document.body.innerHTML") #get html after page loads
        soup = bs4.BeautifulSoup(innerHTML,'html.parser') #parse html
        for item in soup.select('li > a'): #search for elements with urls
            if item.select('h3[class="title"]') and item['href'][:6]=='/news/': #only take news stories, not videos
                url = 'https://www.cbsnews.com' + item['href'] #add url host
                url_list.append((url,'CBS')) #save to list
                
#%%            
    while more_pages and len(set(urls)) < i:
        try:
            element = WebDriverWait(browser, 10).until( #wait for page to load pagination arrow for max of 10 seconds
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="next utilities-pagination-right"]'))) #looking for this element
            next_button = browser.find_element_by_css_selector('div[class="next utilities-pagination-right"]') #get pagination arrow
            scrape(urls)
            next_button.click() #go to next page
            browser.refresh()
        except ElementNotVisibleException or StaleElementReferenceException: #if element exists but is not found
            browser.refresh() #refresh
            sleep(1.5)
        except NoSuchElementException: #if element does not exist
            more_pages = False #no more pages
            continue
        except Exception as e: #any other error
            urls = list(set(urls)) #clean up list
            print('Encountered unexpected problem')
            print(e)
            print(f'Scraped {len(urls)} urls')
            filename = path + f'\\{len(urls)}_cbs_urls.json' #emergency save
            with open(filename, 'w') as outfile:  
                json.dump(urls, outfile)
            if return_ans:
                return urls
            else:
                return
        
#%%
    urls = list(set(urls)) #clean up list
    browser.close()
    filename = path + '\\cbs_urls.json'
    with open(filename, 'w') as outfile: #save data as json 
        json.dump(urls, outfile)
    winsound.PlaySound('ding.wav', winsound.SND_FILENAME) #notify user
    if return_ans: #if answer wanted, return ans
        return urls