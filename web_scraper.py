from requests import get
from requests.exceptions import RequestException
from contextlib import closing

#%%
def simple_get(url):
    headers = {'User-Agent': 'Jerry Quan',
    'From': 'hejequan@gmail.com'} #define header to send with requests
    try:
        with closing(get(url, stream=True, headers = headers)) as resp: #send request
            if is_good_response(resp): #check that response is good
                return resp.text
            else: #otherwise return none
                return None

    except RequestException as e: #if error occurs
        log_error('Error during requests to {0} : {1}'.format(url, str(e))) #log error
        return None

#%%
def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 #good response
            and content_type is not None #reponse is not none
            and content_type.find('html') > -1) #response is html

#%%
def log_error(e): #this can be modified to log errors more systematically
    print(e)
    