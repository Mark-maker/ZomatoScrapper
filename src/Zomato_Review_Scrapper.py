#!/usr/bin/env python
# coding: utf-8

# In[42]:


import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException
import os

import numpy as np





def pull_restaurant_reviews(browser,url):    
    
    print('Hitting the URL: ',url)
    browser.get(url)
    time.sleep(5)
    
    try:
    
        All_reviews_link=browser.find_element_by_xpath('//*[@id="selectors"]/a[2]')
        all_reviews_text = All_reviews_link.text
        #print(all_reviews_text)
        #print('All Reviews ' in all_reviews_text)

        if not 'All Reviews ' in all_reviews_text:
            All_reviews_link=browser.find_element_by_xpath('//*[@id="selectors"]/a[1]')
            all_reviews_text = All_reviews_link.text
            print('Clicked on All_reviews button ..')
            load_more_x_path='//*[@id="reviews-container"]/div[1]/div[3]/div[2]/div/div'
            all_reviews_container_div='zs-following-list'
        else:
            All_reviews_link.click()
            print('Clicked on All_reviews button ..')
            load_more_x_path = '//*[@id="reviews-container"]/div[1]/div[3]/div/div/div[2]/div[1]'
            all_reviews_container_div='zs-following-list pbot'

        Total_Restaurant_Reviews=all_reviews_text.split('\n')[1]
        time.sleep(5)


        #print('124125215')
        time.sleep(3)
        #print('Before Load More..')
        #print(load_more_x_path)

        Load_More = browser.find_element_by_xpath(load_more_x_path)

    #
    except NoSuchElementException as e:
        print('NoSuchElementException encountered before clicking load more..')
        return None
    except StaleElementReferenceException:
        print('StaleElementReferenceException encountered')
    
    clicks=1
    StaleElementCount=0
    while clicks<60:

        try:    
            Load_More.click()
            if clicks%10==0:
                print('Load More Button Clicked ',clicks,' times')
            #print('Load More Button Clicked ',review_count,' times')
            time.sleep(3)
        
        except NoSuchElementException or WebDriverException:
            
            print('Loaded all reviews ..')
            break
            
        except StaleElementReferenceException as e:
            
            print('StaleElementReferenceException encountered, Scrapping reviews will begin... ' )
            #time.sleep(5)
            break

        
        clicks+=1
        

    #print(browser.page_source)zs-following-list
    soup = BeautifulSoup(browser.page_source,'html.parser')
    review_list_containers=soup.findAll('div',{'class':all_reviews_container_div}) # All Reviews Container Div
    #print(review_list_containers)
    for review_list_container in review_list_containers:
        #print(review_list_container)
        review_divs=review_list_container.findChildren('div',recursive=False) #finds direct children of review_list_container
        #print(review_divs)
    #https://stackoverflow.com/questions/48045298/how-to-get-all-direct-children-of-a-beautifulsoup-tag
    customer_reviews=[]
    ID=0
    for review_div in review_divs:   
        #print(review_div)
        ID+=1
        review_dict={}
        review_dict['ID']=str(ID)
        try: 
            user=review_div.find('div',{'class':'header nowrap ui left'})
            user=user.find('a').get_text().strip()
            #print(user)
            profile=review_div.find('span',{'class':'grey-text fontsize5 nowrap'})
            if not profile==None:
                profile=' '.join(profile.get_text().strip().split())
            #print(profile)
            review_dict['user_name']=user
            review_dict['user_importance']=profile
            
        except AttributeError:
            print('Attribute Error: At User/Profile, ')
            pass   
        
            
            
        try:
            review=review_div.find('div',{'class':'rev-text mbot0 hidden'}) #Div for reviews with read_more button.. This Div has the total review text
            if review==None:
                review=review_div.find('div',{'class':'rev-text mbot0'})
            rating_div=review.find('div')
            #print(rating_div)
            #print(rating_div.get_attribute_list('aria-label'))
            rating=rating_div.get_attribute_list('aria-label')
            #print(rating)
            rating=rating[0].split()[1] if len(rating[0].split())==2 else None
            #print(rating)
            #review_dict['user_total_followers']=profile
            review_dict['user_rating']=rating[0]
            #print(rating)
            title=rating_div.get_attribute_list('title')[0]
            #print(title)
            review_dict['review_title']=title
            #print(reviews.find('div',{'class':'rev-text mbot0 '}))
            review_text=review.get_text()
            review_text=" ".join(review_text.split()[1:])    
            review_dict['user_review']=review_text

        except AttributeError:
            print('Attribute Error: Skipping the current review')
            continue


        customer_reviews.append(review_dict)
    
    print(len(customer_reviews),'reviews scrapped from a total of:',Total_Restaurant_Reviews)
    reviews_df=pd.DataFrame(customer_reviews)
    browser.close()
    return reviews_df


# In[46]:


def scrape_reviews_from_url(browser,url):
    try:
        reviews_df=pull_restaurant_reviews(browser,url)
        return reviews_df,True
    except:
        print('Current IP is not working.. Switching to another proxy IP...')
        browser.quit()
        return None,False



