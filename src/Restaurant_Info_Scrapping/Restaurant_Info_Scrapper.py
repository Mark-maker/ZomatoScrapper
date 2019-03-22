import requests
from bs4 import BeautifulSoup
from src.common.Proxy_service import random_proxy
import re
from src.Restaurant_Info_Scrapping.Restaurant_Info_Scrape_Helper import get_geocode,get_img_urls_from
from requests.exceptions import ConnectionError



def get_restaurant_info(url, proxy):

    try:

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        r = requests.get(url, headers=headers, proxies=proxy)
        # print(r.content)
        # time.sleep(5)
        soup = BeautifulSoup(r.content, 'html.parser')
        # print(soup)
        #BeautifulSoup()
        rest_info_div = soup.find('div', {'class': 'row ui segment'})  # Info Container

    except AttributeError:
        print('Error at: Loading Restarant\'s info Container Div', url)



                                                # RESTAURANT NAME

    rest_info = {}
    try:
        rest_name_div = soup.find('h1', {'class': 'res-name left mb0'})
        rest_name = rest_name_div.get_text().strip()
        # print(rest_name)
        rest_info['Rest_Name'] = rest_name

    except AttributeError:

        print('AttributeError while scrapping Restaurant Name: ', url)

    #     name= url.split('/')[-1]
    #     rest_info['Rest_Name']= ' '.join(name.split('-')).capitalize()
    # print(rest_info['Rest_Name'])

                                                  # GOLD OFFFER

    try:

        gold_flag_div = soup.find('div', {'class': 'red_res_tag'})
        if gold_flag_div is not None:
            offer_img_url_tag = gold_flag_div.find('img')
            offer_img_url = offer_img_url_tag.get_attribute_list('src')[0]
            offer_code = offer_img_url[-8]
            # print(offer_code)
            if offer_code == '1':
                gold_offer = '1+1 ON FOOD'
            else:
                gold_offer = '2+2 ON DRINKS'
        else:
            #print('Gold Offer - Not Available for this Restaurant')
            gold_offer = 'Not available'
        rest_info['GOLD_OFFER'] = gold_offer

    except AttributeError:

        print('AttributeError at GOLD: ', url)

                                              # RESTAURANT PHONE NUMBERS

    try:
        Phone_div = rest_info_div.find('div', {'class': 'phone'})
        Phones = rest_info_div.findAll('span', {'class': 'fontsize2 bold zgreen'})
        rest_info['Phone'] = 'Not Available'
        # print(Phones)
        if not len(Phones) == 0:
            rest_info['Phone'] = ','.join(Phone.get_text() for Phone in Phones)

    except AttributeError:
        print('AttributeError: Phone Number', url)
        pass

                                           # RESTAURANT TIMINGS
    try:
        # print(rest_info['Phone'])
        openings_time_div = soup.find('div', {'class': 'res-info-timings'})
        timings = 'Not Available'
        if not openings_time_div == None:
            timings = openings_time_div.find('div', {'class': 'medium'}).get_text()
            timings = ' '.join(timings.split()[1:])  # Removes extra spaces

        # print(timings)
        rest_info['Timings'] = timings

    except AttributeError:
        print('AttributeError: Timings', url)
        pass

                                             # Buffet Menu and Timings

    try:
        buffet_info_container = soup.find('div', {'class': 'res-info-detail buffet-details-resinfo-qv'})
        buffet_details = 'Not Available'
        if buffet_info_container is not None:
            table = buffet_info_container.findChild('table')
            buffet_list = table.findAll('tr')
            buffet_info_list = []
            for buffet_item in buffet_list:
                item = buffet_item.findChildren('td', recursive=False)
                details = item[0].findAll('span')
                details_text = ' '.join(item.get_text() for item in details)
                price = item[1].get_text()
                Buffet_Info = details_text + price
                buffet_info_list.append(Buffet_Info.strip())
                # print(Buffet_Info.strip())
            buffet_details = ','.join(buffet_info_list)
        # print(buffet_details)
        rest_info['Buffet_Info'] = buffet_details

    except AttributeError:
        print('AttributeError: Buffer', url)
        pass

                                             # Restaurant Photos

    try:

        rest_info['Food_Images'] = get_img_urls_from(url + '/photos?category=food', proxy)
        rest_info['Ambience_Images'] = get_img_urls_from(url + '/photos?category=ambience', proxy)

    except AttributeError:
        print('AttributeError: Photos', url)
        pass

        # AVG COST FOR TWO
    try:
        avg_cost_div = rest_info_div.select_one("div[class='mbot mtop']")
        rest_info['Avg_Cost_for_Two_People'] = 'Not Available'
        #     rest_info['Avg_Cost_for_1_Pint_of_Beer']='Not Available'

        if not avg_cost_div == None:
            avg_cost_span = avg_cost_div.find('span', {'tabindex': '0'})
            # print(avg_cost_span.get_attribute_list('aria-label')[0])
            avg_cost = avg_cost_span.get_attribute_list('aria-label')[0]
            avg_cost = avg_cost.split()[0]
            # print(avg_cost)
            rest_info['Avg_Cost_for_Two_People'] = avg_cost

    except AttributeError:
        print('AttributeError: Avg Cost', url)
        pass

        # RESTAURANT FEATURED IN

    try:
        featured_in_div = soup.select_one("div[class='ln24']")
        # print(featured_in_div)
        if not featured_in_div == None:
            featured_in_list_divs = featured_in_div.findAll('a', {'class': 'zred'})
            featured_in_list = []
            for featured_in in featured_in_list_divs:
                # print(featured_in.get_text())
                featured_in_list.append(featured_in.get_text())
            rest_info['Featured_in_Zomato_Collections_of'] = ','.join(featured_in_list)

    except AttributeError:
        print('AttributeError: Restauarant\'s Featured in Collections', url)
        pass

        # RESTAURANT CUISINES

    try:
        # zred is the class of a, which has cuisines text
        cuisines_a_tags = rest_info_div.select(
            "a[class='zred']")  # https://stackoverflow.com/questions/14496860/how-to-beautiful-soup-bs4-match-just-one-and-only-one-css-class
        # print(all_zreds_with_cuisines)
        # to_be_removed=['Add a Zomato spoonback to your blog. ›','Live Sports Screenings','hygiene@zomato.com','visit our FAQs','terms of use...']
        # #print(to_be_removed)
        rest_info['Cuisines'] = ', '.join([i.get_text().strip() for i in cuisines_a_tags])
        # print(rest_info['Cuisines'])
    except:
        print('AttributeError: Cusines', url)
        pass

        # RESTAURANT ADDRESS
    try:
        Address_div = soup.find('div', {'class': 'borderless res-main-address'})
        # print(Address_div)
        Address = Address_div.find('span').get_text()
        # print(Address)
        # rest_info['Address']=soup.findChild('div',{'class':'resinfo-icon'}).get_text().strip()
        # print(rest_info_div.find('div',{'class':'resinfo-icon'}))
        # print(rest_info['Address'])
        rest_info['Address'] = Address
    except:
        print('AttributeError: Address', url)
        pass

        # RESTAURANT GEOCODE

    try:

        rest_info['GEOCODE'] = get_geocode(url + '/maps#tabtop', proxy)
        # print(rest_info['GEOCODE'])

    except AttributeError:

        print('AttributeError: GEOCODE', url)
        pass

        # OTHER INFO/FEATURES
    try:
        other_info_list = soup.findAll('div', {'class': 'res-info-feature-text'})  # .get_text()
        rest_info['Other'] = ",".join([x.get_text() for x in other_info_list])
    except:
        print('AttributeError: Other information', url)
        pass

        # RESTAURANT KNOWN FOR
    try:
        rest_known_for_div = soup.find('div', {'class': 'res-info-known-for-text mr5'})
        rest_info['Known_For'] = 'Not Available'
        if not rest_known_for_div == None:
            rest_known_for = ' '.join(rest_known_for_div.get_text().split())
            # print(rest_known_for)
            rest_info['Known_For'] = rest_known_for
    except:
        print('AttributeError At: Restaurant Known for', url)
        pass

        # RESTAURANT'S RATING AND VOTED
    try:
        # print(cost.findChildren('span'))
        rating_div = soup.find('div', {'class': 'rate_agg'})
        #print(rating_div)
        if not rating_div == None:
            rest_info['Rest_Rating'] = ''.join(rating_div.get_text().split())
            if not rest_info['Rest_Rating'] == 'NEW':
                rest_info['Voted'] = soup.find('span', {'itemprop': 'ratingCount'}).get_text()
        #print(rest_info['Rest_Rating'],rest_info['Voted'])
    except AttributeError:
        print('AttributeError At: Rating and Voted ', url)
        pass

        # RESTAURANT'S HYGIENE RATING
    try:
        Hygiene_rating = soup.find('div', {'class': 'mr10 mt0 all_web_jumbo_click_track'})
        rest_info['Hygiene_Rating'] = 'Not Available'
        if not Hygiene_rating == None:
            Hyg_rating_img_src = Hygiene_rating.find('img').get_attribute_list('src')[0]
            # print(Hyg_rating_img_src.split('/')[-1])
            Hyg = Hyg_rating_img_src.split('/')[-1]
            Hyg = Hyg.replace('.', '-')
            # print(Hyg)
            # print(Hyg.split('-')[-2].upper())
            Hyg_rating = Hyg.split('-')[-2].upper()
            rest_info['Hygiene_Rating'] = Hyg_rating
    except AttributeError:
        print('AttributeError At: Hygiene Rating', url)
        pass

        # HOW/WHAT CUSTOMERS RATED ABOUT RESTAURANT'S OFFERINGS
    try:
        segment2 = soup.select_one("div[class='ui segment']")  # Favourite foods, service, Look&Feel Container
        # print(segment2)
        rating_and_fav_list = segment2.find('div', {'class': 'rv_highlights__wrapper mtop0'})
        if not rating_and_fav_list == None:
            # nested=segment2.find('div',{'class':'rv_highlights__wrapper mtop0'})
            sections = rating_and_fav_list.findChildren('div', recursive=False)

            if not sections == None:
                # END
                # return
                sections_info = []
                for section in sections:
                    section_info_dict = {}
                    section_info_dict['sect_name'] = section.find('div', {'class': 'grey-text'}).get_text()
                    # print(section_info_dict['sect_name'])
                    # sections_info['']
                    items_div = section.findAll('div', {'class': 'fontsize13 ln18'})
                    # print(items_div)
                    if len(items_div) > 0:
                        items_div = section.find('div', {'class': 'fontsize13 ln18'})
                        # print(items_div)
                        # print([item.get_text().strip() for item in items_div.findAll('span')])
                        section_info_dict['item_list'] = ' '.join(
                            [item.get_text().strip() for item in items_div.findAll('span')])
                    else:
                        section_info_dict['item_list'] = 'Not Available'

                    # print(section_info_dict['item_list'])
                    blocks_div = section.find('div', {'class': 'rv_highlights__score_bar mt5 mb5'})
                    block = blocks_div.find('div')
                    # print(block.get_attribute_list('class')[1],'\n\n')
                    sect_rating_level = block.get_attribute_list('class')[1]
                    rest_info[section_info_dict['sect_name']] = section_info_dict['item_list']
                    rest_info[section_info_dict['sect_name'] + '- Rating'] = sect_rating_level

    except AttributeError:
        print('AttributeError At: Restaurant\'s services rating', url)
        pass

                                            # Restaurant DISCLAIMER FLAG

    try:

        desclaimer_tag = soup.find('div', {'class': 'row res-disclaimer'})
        #print(desclaimer_tag)
        desclaimer_Flag_text = desclaimer_tag.get_text().strip()
        desclaimer_Flag_text = re.sub(r'[^\w\s]', '', desclaimer_Flag_text)
        rest_info['Is_Active'] = 'Active'
        rest_info['Delivery_Only'] = 0
        if not desclaimer_Flag_text:
            pass

        elif 'Delivery' in desclaimer_Flag_text:
            rest_info['Delivery_Only'] = 1
            print('This one is a cloud kitchen..')
        elif 'closed' in desclaimer_Flag_text:
            rest_info['Is_Active'] = desclaimer_Flag_text
            print('This restaurant is closed :',url)
        else:
            print(desclaimer_Flag_text)

        #print(desclaimer_Flag_text)
        #print(rest_info['Is_Active'])
    except AttributeError:
        print('AttributeError: Restaurant\'s Disclaimer Flag', url)
        pass

        # print(rest_info)
    rest_info['URL'] = url
    # print(url)
    return rest_info


def Zomato_Scrape_info(URL, proxy):
    try:

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        ip_text=requests.get('http://icanhazip.com',proxies=proxy,headers=headers)
        print('Browsing from - ',ip_text.content.decode('utf-8'))
        rest_info = get_restaurant_info(URL, proxy)
        # print('Inside Function: ',rest_info)
        return rest_info

    except ConnectionError:  # If error, find another proxy

        proxy = random_proxy()
        return Zomato_Scrape_info(URL, proxy)

