import requests
import os
from dotenv import load_dotenv
load_dotenv()

'''
This class grabs a whole bunch of image urls from google images.
'''

class ImageURLGetter:

    def __init__(self):
        self.KEY = os.getenv('GOOGLE_API_KEY')
        self.ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')
        self.URL = 'https://www.googleapis.com/customsearch/v1?searchType=image&key={}&cx={}&q={}'

    def get_urls_for(self, query: str):
        res = requests.get(self.URL.format(self.KEY, self.ENGINE_ID, query))
        results = res.json()['items']
        for r in results:
            print(r.get('link'))


if __name__ == '__main__':
    url_getter = ImageURLGetter()
    url_getter.get_urls_for('dogs')