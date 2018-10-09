import web_scraper
import bs4

def cnn_scrape(url):
    html = web_scraper.simple_get(url)
    soup = bs4.BeautifulSoup(html)
    text = []
    for peas in soup.find_all('meta'):
        try:
            if 'description' in peas['itemprop']:
                text.append(peas['content'])
        except: continue

    for peas in soup.find_all('div'):
        try:
            if 'zn-body__paragraph' in peas['class']:
                text.append(peas.text)
        except: continue    

    result = ' '.join(text)
    return result