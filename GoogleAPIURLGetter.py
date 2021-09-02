import requests
import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
load_dotenv()
Base = declarative_base()


class ImageURLRecord(Base):

    __tablename__ = 'image_urls'
    id = Column(Integer, primary_key=True)
    search_query = Column(String)
    image_url = Column(String)
    downloaded = Column(Boolean)


class URLDumper:
    '''
    Pass in list of objects to dump to postgres database in constructor
    '''
    def __init__(self, url_objects: list):
        ''' each url_obj will be formated as such:
        {
            'search_query': <query>,
            'url': <url>,
            'downloaded': False
        }
        '''
        self.url_objects = url_objects
        self.DB_CONNECTION_STRING = 'postgresql://{username}:{password}@{db_url}/{db_name}'
        self.engine = create_engine(
            self.DB_CONNECTION_STRING.format(
            username=os.getenv('DB_USERNAME'), 
            password=os.getenv('DB_PASSWORD'),
            db_url=os.getenv('DB_URL'),
            db_name=os.getenv('DB_NAME')
        ))
        
    
    def run(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        count = 1
        for obj in self.url_objects:
            print('inserting record number:', count)
            count += 1
            img_url_rec = ImageURLRecord(
                search_query=obj['search_query'], 
                image_url=obj['image_url'], 
                downloaded=obj['downloaded']
            )
            session.add(img_url_rec)
        session.commit()


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
    url_getter = URLGetter(190, 'rounded shoulder posture vs normal')
    urls = url_getter.get_urls()
    print(urls[:3])
    # url_dumper = URLDumper([
    #     {'image_url': 'hellothere', 'search_query': 'spongebob', 'downloaded': False},
    #     {'image_url': 'hellothere', 'search_query': 'spongebob', 'downloaded': False},
    #     {'image_url': 'hellothere', 'search_query': 'spongebob', 'downloaded': False},
    #     {'image_url': 'hellothere', 'search_query': 'spongebob', 'downloaded': False}
    # ])
    url_dumper = URLDumper(urls)
    url_dumper.run()