from selenium import webdriver
from time import sleep


class ImageURLScraper:

    def __init__(self, query: str, max_links_to_fetch: int):
        self.search_url = f'https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={query}&oq={query}&gs_l=img'
        self.max_links_to_fetch = max_links_to_fetch
        self.wd = webdriver.Chrome(executable_path='Driver/chromedriver')
        self.time_to_sleep = 1
        self.image_urls = set()
        self.thumbnails = []

    def load_page(self):
        self.wd.get(self.search_url)

    def get_thumbnails(self, numer_of_times_to_scroll: int):
        '''
        grabs thumbnails from search page and scrolls for given times
        '''
        for _ in range(numer_of_times_to_scroll):
            self.scroll_to_end()
            self.thumbnails.extend(self.wd.find_elements_by_css_selector('img.Q4LuWd'))

    def extract_image_links_from_thumbnails(self):
        for img in self.thumbnails:
            # try clicking every thumbnail so we can get the real image behind it
            try:
                img.click()
                sleep(self.time_to_sleep)
            except Exception:
                continue

            # extract the image urls. Not every element will be able to return a valid link
            actual_images = self.wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    self.image_urls.add(actual_image.get_attribute('src'))

    def scroll_to_end(self):
        self.wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(self.time_to_sleep)

    def write_urls_to_txt_file(self):
        with open('image_urls.txt', 'w') as f:
            for url in self.image_urls:
                f.write(url + '\n')

    def run(self):
        '''
        main method of class that starts the scraping process
        '''
        # first load page
        self.load_page()
        # grab thumbnails
        self.get_thumbnails(1)
        print('number of thumbnails:', len(self.thumbnails))
        # extract image links from thumbnails
        self.extract_image_links_from_thumbnails()
        # write all image urls to a txt file
        self.write_urls_to_txt_file()


if __name__ == '__main__':
    scraper = ImageURLScraper('dogs', 3)
    scraper.run()
