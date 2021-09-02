from selenium import webdriver
from time import sleep

'''
This is a google image web scraper developed using selenium.
It turns out that all of this scraping is actualy pointless lol.
Google offers an api to search for their images.
'''


class ImageURLScraper:

    def __init__(self, query: str, number_of_times_to_scroll: int = 1):
        self.search_url = f'https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={query}&oq={query}&gs_l=img'
        self.wd = webdriver.Chrome(executable_path='Driver/chromedriver')
        self.time_to_sleep = .5
        self.image_urls = set()
        self.thumbnails = []
        self.number_of_times_to_scroll = number_of_times_to_scroll

    def load_page(self):
        self.wd.get(self.search_url)

    def get_thumbnails(self):
        '''
        grabs thumbnails from search page and scrolls for given times
        '''
        for _ in range(self.number_of_times_to_scroll):
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
        self.get_thumbnails()
        print('number of thumbnails:', len(self.thumbnails))
        # extract image links from thumbnails
        self.extract_image_links_from_thumbnails()
        # write all image urls to a txt file
        self.write_urls_to_txt_file()
        # quit when done
        self.wd.quit()


if __name__ == '__main__':
    # pass in query and how many times bot should scroll down on the results page (this results in more data)
    scraper = ImageURLScraper('rounded shoulder posture vs normal')
    scraper.run()
