from src.Restaurant_Info_Scrapping.Restaurant_Info_Scrapper import get_restaurant_info,Zomato_Scrape_info
from tqdm import tqdm
from src.common.Proxy_service import random_proxy
import pandas as pd
import src.common.properties as prop
from datetime import datetime
from src.common.MongoConnector import connect_to_my_mongo_db,disconnect


rest_info_list = []


URLS_df = pd.read_csv(prop.Restaurant_master_file_path)
# os.chdir('E:\\DSA Internship\\Web Scrapping\\Zomato Restaurants Web Scrapping\\Cities\\Hyderabad\\Error Urls\\')
# Error_URLS=[]
# with open('ErrorURLs.txt','r') as f:
#     for URL in f.read().splitlines():
#         Error_URLS.append(URL)

# rest_urls_list = ['https://www.zomato.com/hyderabad/kebab-e-bahar-taj-banjara-banjara-hills',
#                    'https://www.zomato.com/hyderabad/36-downtown-brew-pub-jubilee-hills',
#                    'https://www.zomato.com/hyderabad/huber-holly-banjara-hills',
#                   'https://www.zomato.com/hyderabad/behrouz-biryani-banjara-hills',
#                   'https://www.zomato.com/hyderabad/seasonal-tastes-the-westin-hitech-city',
#                   'https://www.zomato.com/rolling-stove-food-truck']  # list of Restaurant URLs

proxy = random_proxy()

start=datetime.now()
#for url in tqdm(URLS_df[30:50].values):
database=connect_to_my_mongo_db('Restaurants')
restaurant_mongo_master_collection=database.Restaurants_Info_Master

start_index=int(input('Input the Start Index of the URLs: '))
stop_index=int(input('Input the Stop Index of the URLs: '))

n= start_index
for url in URLS_df[start_index:stop_index].values:
    Not_properly_scrapped = True
    print('Scrapping Restaurant Data of index ',n,': ',url[0])

    while Not_properly_scrapped:
        # print(url)
        rest_info = Zomato_Scrape_info(url[0], proxy)
        if not rest_info == None:
            Not_properly_scrapped = False
        else:
            proxy = random_proxy()

    # print(rest_info,'\n')
    # print(rest_info)
    restaurant_mongo_master_collection.insert_one(rest_info)
    rest_info_list.append(rest_info)
    # Every 10 requests, generate a new proxy
    if n % 40 == 0:
        proxy = random_proxy()
        # proxy = proxies[proxy_index]

    n += 1
print('Total time taken to scrape info of {} restaurants: '.format(stop_index-start_index),datetime.now()-start)

#pd.DataFrame(rest_info_list).to_csv('E:/sample1.csv',index=False)
