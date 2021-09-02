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
        engine = sqlalchemy.create_engine(self.DB_CONNECTION_STRING.format(
            username=self.DB_USERNAME, 
            password=self.DB_PASSWORD,
            db_url=self.DB_URL,
            db_name=self.DB_NAME
        ))
        conn = engine.connect()
        res = conn.execute("SELECT VERSION()")
        for r in res:
            print(r)


class URLGetter:
    '''
    Pass in how many urls you want to fetch in constructor.
    Use .search_query() to search for images.
    '''
    def __init__(self, num_urls: int, query: str):
        self.query = query
        self.num_urls = num_urls
        self.urls = []
        self.KEY = os.getenv('GOOGLE_API_KEY')
        self.ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')
        self.URL = 'https://www.googleapis.com/customsearch/v1?searchType=image&key={key}&cx={engine_id}&q={query}&start={start_index}'

    def fetch_next_10_urls(self, request_url: str):
        '''
        fetches 10 urls, puts each url into a dict and puts dicts into self.urls list
        '''
        res = requests.get(request_url)
        results = res.json()['items']
        for r in results:
            self.urls.append({
                'search_query': self.query,
                'url': r.get('link'),
                'downloaded': False
            })

    def get_urls(self):
        '''
        fetches urls in batches of 10 and returns a list of dicts with format:
        {
            'search_query': <query>,
            'url': <url>,
            'downloaded': False
        }
        '''
        start_index = 1
        end = ((self.num_urls // 10) + 1) # api fetches results in batches of 10
        for _ in range(0, end):
            print(f'Batch count: {start_index} - {start_index + 10}')
            request_url = self.URL.format(key=self.KEY, engine_id=self.ENGINE_ID, query=self.query, start_index=start_index)
            self.fetch_next_10_urls(request_url)
            start_index += 10
        return self.urls


if __name__ == '__main__':
    # current limit is around 200 images
    # url_getter = URLGetter(190, 'rounded shoulder posture vs normal')
    # urls = url_getter.get_urls()
    # print(urls)
    url_dumper = URLDumper([])
    url_dumper.run()