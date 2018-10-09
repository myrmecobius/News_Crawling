from selenium import webdriver
import bs4
import os
import re
from time import sleep
import json
import winsound

#%%
def USA_crawl(url, i = 10**9, path = os.getcwd(), return_ans = False):
    if re.search('^(([^:/?#]+):)?(//([^/?#]*))?',url).groups()[-1] != 'www.usatoday.com': #check that url host matches
        print('Please input url from www.usatoday.com')
        return
    browser = webdriver.Chrome()
    browser.get(url)
    urls = []
    target_num = i #target number of articles wanted
    
#%%    
    more_pages = True
    num_article = 0 #initialize counter
    list_button = browser.find_element_by_css_selector('span[class="ui-btn list-btn"]') #view results as list
    list_button.click()
    
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") #scroll to bottom of page
    num_article += 20 #first page holds 20 articles
    sleep(1.5)

#%%        
    try:
        while more_pages and num_article < target_num:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") #keep scrolling
            num_article += 10 #each scroll adds 10 articles
            sleep(1.5)
        
        innerHTML = browser.execute_script("return document.body.innerHTML") #get html after scrolling
        soup = bs4.BeautifulSoup(innerHTML,'html.parser') #parse html
        for item in soup.select('a[class="search-result-item-link"]'): #find urls
            url_link = 'https://www.usatoday.com' + item['href']
            urls.append((url_link,'USA')) #add url to list
    except Exception as e: #in case of any errors
        urls = list(set(urls)) #clean up urls
        print('Encountered unexpected problem')
        print(e)
        print(f'Scraped {len(urls)} urls')
        filename = path + f'\\{len(urls)}_usa_urls.json' #conduct emergency save
        with open(filename, 'w') as outfile:  
            json.dump(urls, outfile)
        if return_ans:
            return urls
        else:
            return


#%%
    urls = list(set(urls)) #clean up list
    browser.close()
    filename = path + '\\usa_urls.json'
    with open(filename, 'w') as outfile:  #save data as json
        json.dump(urls, outfile)
    winsound.PlaySound('ding.wav', winsound.SND_FILENAME) #notify user
    if return_ans: #return answer if wanted
        return urls