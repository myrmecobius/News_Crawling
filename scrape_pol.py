import web_scraper
import bs4

def pol_scrape(url):
    html = web_scraper.simple_get(url)
    soup = bs4.BeautifulSoup(html,'html.parser')
    text = []
    for peas in soup.select('div[class="story-text "] > p'):
        text.append(peas.text)

    result = ' '.join(text)
    return result