from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.properties import Chrome_driver_path




def Create_Chrome_browser(headless=True, use_proxy=False, proxy=None):
    chrome_options = Options()
    if use_proxy:
        proxy_text = proxy['ip'] + ':' + proxy['port']
        proxy_text = 'http://' + str(proxy_text)
        print('Browsing with ip: ', proxy_text)
        chrome_options.add_argument('--proxy-server=' + proxy_text)

    if headless:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')
        browser = webdriver.Chrome(executable_path=Chrome_driver_path, options=chrome_options)
        print('Using Headless Chrome Browser...')
        return browser

    browser = webdriver.Chrome(executable_path=Chrome_driver_path, options=chrome_options)
    print('A Chrome Browser will be opened...')
    return browser
