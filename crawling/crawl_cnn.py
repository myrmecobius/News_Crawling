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
def CNN_crawl(url, i = 10**9, path = os.getcwd(), return_ans = False):
    if re.search('^(([^:/?#]+):)?(//([^/?#]*))?',url).groups()[-1] != 'www.cnn.com': #check if url host matches
        print('Please input url from www.cnn.com')
        return
    browser = webdriver.Chrome()
    browser.get(url)
    close_bottom_banner = browser.find_element_by_css_selector('a.optanon-alert-box-close') #find alert box
    close_bottom_banner.click() #close alert box
    sleep(1)
    urls = []
    more_pages = True

#%%
    def scrape(url_list):
        innerHTML = browser.execute_script("return document.body.innerHTML") #get html after page loads
        soup = bs4.BeautifulSoup(innerHTML,'html.parser') #parse html
        for item in soup.find_all('div[class*="cnn-search__result"]'): #find element
                url = item.find_all('h3')[0].find_all('a')[0]['href']
                url = 'https:' + url
                #date = datetime.strptime(date, '%b %d, %Y') #this gets the date
                #date = divy.find_all('span')[1].text #commented out because functionality assigned to scraping code
                url_list.append((url,'CNN')) #add url to list

#%%        
    while more_pages and len(set(urls)) < i:
        try:
            element = WebDriverWait(browser, 10).until( #wait for element to load for max of 10 seconds
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.pagination-arrow-right'))) #find this element
            next_button = browser.find_element_by_css_selector('div.pagination-arrow-right') #get pagination arrow
            scrape(urls)
            next_button.click() #go to next page
            sleep(1)
        except StaleElementReferenceException or ElementNotVisibleException: #if element exists but is not found
            browser.refresh() #refresh and try again
            sleep(2)
        except NoSuchElementException: #if element doesn't exist
            more_pages = False #no more pages
        except Exception as e: #any other error
            urls = list(set(urls)) #clean up list
            print('Encountered unexpected problem')
            print(e)
            print(f'Scraped {len(urls)} urls')
            filename = path + f'\\{len(urls)}_cnn_urls.json' #emergency save
            with open(filename, 'w') as outfile:  
                json.dump(urls, outfile)
            if return_ans:
                return urls
            else:
                return
        
#%%
    urls = list(set(urls)) #after while loop finishes, clean up list
    browser.close()
    filename = path + '\\cnn_urls.json'
    with open(filename, 'w') as outfile:   #save data as json
        json.dump(urls, outfile)
    winsound.PlaySound('ding.wav', winsound.SND_FILENAME) #notify user
    if return_ans: #return answer if wanted
        return urls
