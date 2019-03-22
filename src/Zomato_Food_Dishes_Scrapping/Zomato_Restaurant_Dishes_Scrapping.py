import src.common.properties as prop
import pandas as pd
from datetime import datetime
from src.common.MongoConnector import connect_to_my_mongo_db,get_mongo_rest_ref_by_url
from src.common.Chrome_Driver import Create_Chrome_browser
from src.common.Proxy_service import random_proxy
from src.Zomato_Food_Dishes_Scrapping.Zomato_Dish_Scrape_Helper import scrape_rest_dishes_from_url



URLS_df = pd.read_csv(prop.Restaurant_master_file_path)
start=datetime.now()
#for url in tqdm(URLS_df[30:50].values):
database=connect_to_my_mongo_db('Restaurants')
mongo_food_master_collection=database.Food_Items_Master

start_index=int(input('Input the Start Index of the Restaurant URLs: '))
stop_index=int(input('Input the Stop Index of the Restaurant URLs: '))

n= start_index
for url in URLS_df[start_index:stop_index].values:
    rest_url=url[0]
    rest_ref=get_mongo_rest_ref_by_url(database,'Restaurants_Info_Master',rest_url)
    order_url=rest_url+'/order'
    print('Scrapping Restaurant Food Items Data of index ',n,': ',order_url)
    proxy=random_proxy()
    scrapped_properly=False
    while not scrapped_properly:
        chrome_browser = Create_Chrome_browser(use_proxy=True, proxy=proxy['http'])
        try:
            food_dict_list=scrape_rest_dishes_from_url(chrome_browser,order_url)
            #food_dict_list = food_items_df.to_dict('records')
            for food_item in food_dict_list:
                food_item['Restaurant_Ref']=rest_ref
                mongo_food_master_collection.insert_one(food_item)
            scrapped_properly=True
        except ConnectionError:
            proxy=random_proxy()
    n+=1
print(f'Time taken to scrape food items of {stop_index-start_index} restaurants: {datetime.now()-start}')