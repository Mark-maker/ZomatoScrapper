
from datetime import datetime
import pandas as pd
import src.common.properties as prop
from src.common.Proxy_service import random_proxy
from src.common.Chrome_Driver import Create_Chrome_browser
from src.Restaurant_Reviews_Scrapping.Zomato_Review_Scrapper import scrape_reviews_from_url
from src.common.MongoConnector import get_mongo_client,connect_to_my_mongo_db,get_mongo_rest_ref_by_url

def scrape_reviews(start_index,stop_index):

    URLS_df = pd.read_csv(prop.Restaurant_master_file_path)
    # URLS=URLS_df['URLS'].tolist()
    ErrorURLs=pd.read_csv(prop.ErrorURLs_file_path)
    error_url_list=ErrorURLs['Error_URLS'].tolist()
    reviews_folder_path = prop.Reviews_folder_path


    start = datetime.now()
    proxy = random_proxy()
    total_reviews_count=0

    #Mongo_DB Connection...
    db = connect_to_my_mongo_db('Restaurants')
    mongo_reviews = db['Reviews_Master']

    for row in URLS_df[start_index:stop_index].values:
        begin = datetime.now()
        url = row[0]  # row[0] for url and row[1] for Rest_ID
        if url in error_url_list:
            print('The current URL had errors while scrapping its restuarant info, Hence skipping this url: ',url)
            continue


        Mongo_ref=get_mongo_rest_ref_by_url(db,'Restaurants_Info_Master',url)
        rest_review_url = url + '/reviews'
        not_scrapped = True
        while not_scrapped:  # loop repeats till a working proxy IP is caught
            chrome_browser = Create_Chrome_browser(use_proxy=True,proxy=proxy['http'])
            # print(url)
            reviews_df, success = scrape_reviews_from_url(chrome_browser, rest_review_url)

            if success:

                if len(reviews_df)==0:
                    print('CSV file will not be generated...')
                    print('-'*100,'\n')
                    not_scrapped = False
                    continue
                Rest_ID = str(row[1])
                file_name = url.split('/')[-1]
                #print(file_name)
                #https://stackoverflow.com/questions/29815129/pandas-dataframe-to-list-of-dictionaries

                reviews_dict_list=reviews_df.to_dict('records')
                for review in reviews_dict_list:
                    review['Restaurant_Ref']=Mongo_ref
                    mongo_reviews.insert_one(review)

                csv_file_name = reviews_folder_path + Rest_ID + '-' + file_name + '.csv'
                #print(row[1])
                print('Restaurant ID:',Rest_ID)
                reviews_df['Restaurant_ID'] = Rest_ID  # Copying the string values of IDs
                reviews_df['Review_ID'] = reviews_df['Restaurant_ID'] + '000' + reviews_df['ID']
                reviews_df=reviews_df[['Review_ID','Restaurant_ID','ID','review_title','user_importance','user_name','user_rating','user_review']]

                reviews_df.to_csv(csv_file_name, index=False)
                reviews_df.to_csv(prop.Reviews_master_file_path, mode='a', header=False,
                                  index=False)  # https://stackoverflow.com/questions/17530542/how-to-add-pandas-data-to-an-existing-csv-file
                chrome_browser.quit()
                not_scrapped = False
                print('-' * 100)
                print('{} has been created'.format(file_name + '.csv'))
                print('Time taken to scrape and create the the above file: ', datetime.now() - begin)
                print('\n\n')
                total_reviews_count+=len(reviews_df)
            else:
                proxy=random_proxy()

        # with open('review_master.csv',mode='a',headers=False) as master:
    print('Total reviews scrapped: ',total_reviews_count)
    print('Time taken to scrape all the reviews: ', datetime.now() - start)
    chrome_browser.quit()
    # reviews_df
#print(os.getcwd())
start_index = int(input('Input the URLs start index: '))  # Input the start index
end_index = int(input('Input the URLs Stop index: '))  # Input the end index
scrape_reviews(start_index,end_index)
