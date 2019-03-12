from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.common.properties import Chrome_driver_path




def Create_Chrome_browser(headless=True, use_proxy=False, proxy=None):
    chrome_options = Options()
    if use_proxy:
        print('Browsing with ip: ', proxy)
        chrome_options.add_argument('--proxy-server=' + proxy)

    if headless:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')
        browser = webdriver.Chrome(executable_path=Chrome_driver_path, options=chrome_options)
        print('Using Headless Chrome Browser...')
        return browser

    browser = webdriver.Chrome(executable_path=Chrome_driver_path, options=chrome_options)
    print('A Chrome Browser will be opened...')
    return browser
