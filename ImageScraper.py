from selenium import webdriver

DRIVER_PATH = 'Driver/chromedriver'

wd = webdriver.Chrome(executable_path=DRIVER_PATH)

wd.get('https://google.com')

search_box = wd.find_element_by_css_selector('input.gLFyf')

search_box.send_keys('dogs')