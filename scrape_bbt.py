import web_scraper
import bs4

def bbt_scrape(url):
    html = web_scraper.simple_get(url)
    soup = bs4.BeautifulSoup(html,'html.parser')
    text = []
    for peas in soup.select('div[class="entry-content"] > h2'):
        text.append(peas.text)
    for peas in soup.select('div[class="entry-content"] > p'):
        text.append(peas.text)
            
    result = ' '.join(text)
    return result
