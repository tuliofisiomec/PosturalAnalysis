from ImageDownloader import ImageDownloader
from ImageScraper import ImageURLScraper


if __name__ == '__main__':

    # first scrape for urls and write to txt file
    scraper = ImageURLScraper('rounded shoulder posture vs normal')
    scraper.run()
    # now download files 
    downloader = ImageDownloader()
    downloader.run()
