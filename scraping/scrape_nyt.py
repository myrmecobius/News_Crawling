import web_scraper
import bs4

def nyt_scrape(url):
    html = web_scraper.simple_get(url)
    soup = bs4.BeautifulSoup(html)
    text = []
    for peas in soup.find_all('p'):
        try:
            if 'css-1i0edl6' in peas['class']:
                text.append(peas.text)
        except: continue

    result = ' '.join(text)
    return result