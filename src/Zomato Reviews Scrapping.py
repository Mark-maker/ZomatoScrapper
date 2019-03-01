
from datetime import datetime
import pandas as pd
import src.properties as prop
from src.Random_Proxy import random_proxy
from src.Chrome_Driver import Create_Chrome_browser
from src.Zomato_Review_Scrapper import scrape_reviews_from_url
import os


def scrape_reviews(start_index,stop_index):
    # input the path in which Rest URLs csv is stored


    # os.chdir(folder_path)
    URLS_df = pd.read_csv(prop.Restaurant_master_file_path)
    # URLS=URLS_df['URLS'].tolist()
    reviews_folder_path = prop.Reviews_folder_path


    start = datetime.now()
    proxy = random_proxy()
    for row in URLS_df[start_index:stop_index].values:
        begin = datetime.now()
        url = row[0]  # url[0] for url and url[1] for Rest_ID
        rest_review_url = url + '/reviews'
        not_scrapped = True
        while not_scrapped:  # loop repeats till a working proxy IP is caught
            chrome_browser = Create_Chrome_browser(use_proxy=True,proxy=proxy)
            # print(url)
            reviews_df, success = scrape_reviews_from_url(chrome_browser, rest_review_url)
            if success:
                file_name = url.split('/')[-1]
                #print(file_name)
                csv_file_name = reviews_folder_path + file_name + '.csv'
                #print(row[1])
                print('Restaurant ID:',str(row[1]))
                reviews_df['Restaurant_ID'] = str(row[1])  # Copying the string values of IDs
                reviews_df['Review_ID'] = reviews_df['Restaurant_ID'] + '-' + reviews_df['ID']
                reviews_df=reviews_df[['Review_ID','Restaurant_ID','ID','review_title','user_importance','user_name','user_rating','user_review']]
                reviews_df.to_csv(csv_file_name, index=False)
                reviews_df.to_csv(prop.Reviews_master_file_path, mode='a', header=False,
                                  index=False)  # https://stackoverflow.com/questions/17530542/how-to-add-pandas-data-to-an-existing-csv-file

                # chrome_browser.quit()
                not_scrapped = False
                print('-' * 100)
                print('{} has been created'.format(file_name + '.csv'))
                print('Time taken to scrape and create the the above file: ', datetime.now() - begin)
                print('\n\n')
            else:
                proxy=random_proxy()

        # with open('review_master.csv',mode='a',headers=False) as master:

    print('Time taken to scrape all the reviews: ', datetime.now() - start)
    chrome_browser.quit()
    # reviews_df
#print(os.getcwd())
start_index = int(input('Input the URLs start index: '))  # Input the start index
end_index = int(input('Input the URLs start index: '))  # Input the end index
scrape_reviews(start_index,end_index)
