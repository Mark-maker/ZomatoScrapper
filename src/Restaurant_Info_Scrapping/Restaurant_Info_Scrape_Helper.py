import requests
from bs4 import BeautifulSoup
from src.common.Proxy_service import random_proxy
from requests.exceptions import ConnectionError


def get_img_urls_from(url ,proxy):
    try:
        img_url_list =[]
        headers = \
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        response = requests.get(url, headers=headers, proxies=proxy)
        soup = BeautifulSoup(response.content, 'html.parser')
        images_divs_container = soup.find('div', {'class': 'photos_container_load_more inlineblock w100'})
        image_divs = images_divs_container.findChildren('div', recursive=False)
        if not len(image_divs) > 0:
            return 'Not Available'
        for div in image_divs[:10]:
            image_url_div = div.find('img')
            # print(image_url_div)
            image_url = image_url_div.get_attribute_list('data-original')[0]
            image_url = image_url.split('?')[0]
            # print(image_url)
            img_url_list.append(image_url)
        return ','.join(img_url_list)

    except ConnectionError:
        print('ConnectionError inside get_img_urls_from() method, changing IP')
        return get_img_urls_from(url, random_proxy())




def get_geocode(url, proxy):
    try:

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        r = requests.get(url, proxies=proxy, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        map_container = soup.find('div', {'class': 'ui segment map_container'})
        if map_container is None:
            return 'Not Available'
        geo_link = map_container.find('a')
        geocode = geo_link.get_attribute_list('href')[0].split('/')[-1]
        # print(geocode)
        return geocode

    except ConnectionError:
        print('ConnectionError inside get_geocode() method, changing IP')
        return get_geocode(url, random_proxy())