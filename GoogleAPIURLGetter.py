import requests
import os
import sqlalchemy
from dotenv import load_dotenv
load_dotenv()


class URLDumper:
    '''
    Pass in list of objects to dump to postgres database in constructor
    '''
    def __init__(self, url_objects: list):
        self.url_objects = url_objects
        self.DB_USERNAME = os.getenv('DB_USERNAME')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD')
        self.DB_URL = os.getenv('DB_URL')
        self.DB_NAME = os.getenv('DB_NAME')
        self.DB_CONNECTION_STRING = 'postgresql://{username}:{password}@{db_url}/{db_name}'
    
    def run(self):
        # first create db engine
        # engine = sqlalchemy.create_engine(connection_string)
        pass


class URLGetter:
    '''
    Pass in how many urls you want to fetch in constructor.
    Use .search_query() to search for images.
    '''
    def __init__(self, num_urls: int):
        self.num_urls = num_urls
        self.urls = []
        self.KEY = os.getenv('GOOGLE_API_KEY')
        self.ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')
        self.URL = 'https://www.googleapis.com/customsearch/v1?searchType=image&key={}&cx={}&q={}&start={}'

    def fetch_urls(self, query: str):
        '''
        fetches 10 urls and puts into self.urls list
        '''
        print('++++++++')
        print(query)
        print('++++++++')
        res = requests.get(query)
        results = res.json()['items']
        for r in results:
            print(r.get('link'))
        print('--------------')

    def search_query(self, query: str):
        start_index = 1
        end = ((self.num_urls // 10) + 1) + 1 # api fetches results in batches of 10
        for _ in range(1, end):
            query = self.URL.format(self.KEY, self.ENGINE_ID, query, start_index)
            self.fetch_urls(query)
            start_index += 10


if __name__ == '__main__':
    url_getter = URLGetter(40)
    url_getter.search_query('dogs')