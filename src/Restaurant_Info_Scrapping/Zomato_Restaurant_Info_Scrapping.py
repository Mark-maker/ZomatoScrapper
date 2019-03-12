from src.Restaurant_Info_Scrapping.Restaurant_Info_Scrapper import get_restaurant_info,Zomato_Scrape_info
from tqdm import tqdm
from src.common.Proxy_service import random_proxy
import pandas as pd
import src.common.properties as prop


n= 6000
rest_info_list = []


URLS_df = pd.read_csv(prop.Restaurant_master_file_path)
# os.chdir('E:\\DSA Internship\\Web Scrapping\\Zomato Restaurants Web Scrapping\\Cities\\Hyderabad\\Error Urls\\')
# Error_URLS=[]
# with open('ErrorURLs.txt','r') as f:
#     for URL in f.read().splitlines():
#         Error_URLS.append(URL)

rest_urls_list = ['https://www.zomato.com/hyderabad/kebab-e-bahar-taj-banjara-banjara-hills',
                  'https://www.zomato.com/hyderabad/36-downtown-brew-pub-jubilee-hills',
                  'https://www.zomato.com/hyderabad/huber-holly-banjara-hills']  # list of Restaurant URLs

proxy = random_proxy()

for url in tqdm(URLS_df[1:10].values):


    Not_properly_scrapped = True
    #print(n)
    while Not_properly_scrapped:
        # print(url)
        rest_info = Zomato_Scrape_info(url[0], proxy)
        if not rest_info == None:
            Not_properly_scrapped = False
        else:
            proxy = random_proxy()

    # print(rest_info,'\n')
    # print(rest_info)
    rest_info_list.append(rest_info)
    # Every 10 requests, generate a new proxy
    if n % 40 == 0:
        proxy = random_proxy()
        # proxy = proxies[proxy_index]

    n += 1
pd.DataFrame(rest_info_list).to_csv('E:/sample1.csv',index=False)
print(pd.DataFrame(rest_info_list))