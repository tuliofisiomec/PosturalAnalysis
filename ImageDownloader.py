# import io
# import requests
# import wget
import urllib.request

if __name__ == '__main__':

    opener = urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
    num = 0
    with open('image_urls.txt', 'r') as f:
        for url in f.readlines():
            file_name = f'dogs/dog_{num}.jpeg'
            urllib.request.urlretrieve(url, file_name)
            num += 1
            


        