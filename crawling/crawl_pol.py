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
def Politico_crawl(url, i = 10**9, path = os.getcwd(), return_ans = False):
    if re.search('^(([^:/?#]+):)?(//([^/?#]*))?',url).groups()[-1] != 'www.politico.com': #check url host matches
        print('Please input url from www.politico.com')
        return
    browser = webdriver.Chrome()
    browser.get(url)
    urls = []
    close_cookies = browser.find_element_by_css_selector('button[class="js-accept-cookie-close cookie-modal__close"]') #find cookie agreement box close button
    close_cookies.click() #close cookie agreement box
    more_pages = True
    
#%%
    def scrape(url_list):
        innerHTML = browser.execute_script("return document.body.innerHTML") #get html after page loads
        soup = bs4.BeautifulSoup(innerHTML,'html.parser') #parse html
        for item in soup.select('header > h3 > a'): #find elements with urls
            url = item['href']
            url_list.append((url,'POL')) #add url to list

#%%
    element = WebDriverWait(browser, 10).until( #wait for element to load for 10 seconds
    EC.presence_of_element_located((By.CSS_SELECTOR, 'nav[class="content-nav"] > div[class="contextual"] > a'))) #waiting for this element
    next_button = browser.find_element_by_css_selector('nav[class="content-nav"] > div[class="contextual"] > a') #get pagination button
    scrape(urls)
    next_button.click() #go to next page
    browser.refresh()
            
    while more_pages and len(set(urls)) < i:
        try:
            element = WebDriverWait(browser, 10).until( #same as above
            EC.presence_of_element_located((By.CSS_SELECTOR, 'nav[class="content-nav"] > div[class="contextual"] > a + a'))) #except get second pagination button
            next_button = browser.find_element_by_css_selector('nav[class="content-nav"] > div[class="contextual"] > a + a') #corresponding to next instead of previous
            scrape(urls)
            next_button.click()
            browser.refresh()
        except ElementNotVisibleException or StaleElementReferenceException: #if next button exists but cannot be found
            browser.refresh() #refresh and try again
            sleep(1.5)
        except NoSuchElementException: #if next button does not exist
            more_pages = False #no more pages
            continue
        except Exception as e: #any other errors
            urls = list(set(urls)) #clean up urls
            print('Encountered unexpected problem')
            print(e)
            print(f'Scraped {len(urls)} urls')
            filename = path + f'\\{len(urls)}_pol_urls.json' #conduct emergency save
            with open(filename, 'w') as outfile:  
                json.dump(urls, outfile)
            if return_ans:
                return urls
            else:
                return

#%%
    urls = list(set(urls)) #after while loop, clean up urls
    browser.close()
    filename = path + '\\Politico_urls.json'
    with open(filename, 'w') as outfile:  #save data as json file
        json.dump(urls, outfile)
    winsound.PlaySound('ding.wav', winsound.SND_FILENAME) #notify user
    if return_ans: #return answer if wanted
        return urls