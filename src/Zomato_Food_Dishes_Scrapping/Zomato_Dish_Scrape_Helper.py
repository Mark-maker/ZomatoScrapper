from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By





def get_food_dict(item,menu_header):
    try:
        food_dict = {}
        item_name = item.findChild('div', {'class': 'header'})
        veg_non_veg_category = item_name.findPreviousSibling('div')
        veg_non_veg = veg_non_veg_category.get_attribute_list('class')[0]
        veg_non_veg = veg_non_veg.split()[0]
        item_price = item.findChild('div', {'class': 'description'})
        item_description = item.findChild('div', {'class': 'meta'})
        # print(item_name.get_text(),item_price.get_text(),item_description.get_text(),'\n')
        food_dict['Menu_Type'] = menu_header
        food_dict['Item_Name'] = item_name.get_text()
        food_dict['Item_price'] = item_price.get_text()
        food_dict['Item_Description'] = 'Not Available'
        if item_description is not None:
            food_dict['Item_Description'] = item_description.get_text()
        food_dict['Food_Category'] = 'VEG' if veg_non_veg == 'veg' else 'NON-VEG'
        return food_dict
    except AttributeError:
        print('Attribute Error..')




def scrape_rest_dishes_from_url(browser,url):

    browser.get(url)
    try:
        print('In there....')
        print(WebDriverWait(browser, 50).until
            (EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[1]/div[2]/div[3]'))))
        print('Done..')
    except:
        print('Nope..')
        raise ConnectionError


    time.sleep(10)
    soup =BeautifulSoup(browser.page_source ,'html.parser')
    # print(soup)
    menu_container =soup.find('div' ,{'class' :'menu-container'})
    # print(menu_container)
    menu_divs =menu_container.findChildren('div' ,recursive=False)
    # print(len(menu_divs))
    print('- ' *50)
    rest_food_info =[]
    for menu in menu_divs[:-2]:
        menu_header =menu.findChild('h3').get_text()
        # print(menu_header)
        categories =menu.findChildren('div' ,recursive=False)
        # print(len(categories))

        for category in categories:

            category_items_div =category.findChildren('div' ,recursive=False)
            if len(category_items_div ) >1:
                category_name =category_items_div[0]
                # print('\n\n',category_name.get_text(),'\n')
                category_items =category_items_div[1].findChildren('div' ,recursive=False)
                for item in category_items:
                    food_dict =get_food_dict(item,menu_header)
                    rest_food_info.append(food_dict)

            else:
                category_items =category_items_div[0].findChildren('div' ,recursive=False)
                for item in category_items:
                    food_dict =get_food_dict(item,menu_header)
                    rest_food_info.append(food_dict)

    return rest_food_info