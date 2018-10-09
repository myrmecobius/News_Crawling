import web_scraper
import bs4

def usa_scrape(url):
    html = web_scraper.simple_get(url)
    soup = bs4.BeautifulSoup(html,'html.parser')
    text = []
    
    if soup.select('h2') == []:
        for peas in soup.select('p[class~="p-text"]'):
            try:
                if 'p-text-last' not in peas['class']:
                    text.append(peas.text)
            except: continue
                
        result = ' '.join(text)
        return result
    else:
        for peas in soup.select('p[class~="p-text"]'):
            try:
                if 'p-text-last' not in peas['class']:
                    if 'presto-h2' in peas.previous_element.previous_element['class']:
                        text.append(peas.previous_element.previous_element.text)
                    text.append(peas.text)
            except: continue
                
        result = ' '.join(text)
        return result
