#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
from bs4 import BeautifulSoup
import requests
import re
from django.contrib.admin.utils import flatten

kauplused = [ 
{"Maxima": 'scraper\maxima.html', "article" : "col-third", "headline":"title", "discount" : 'discount percents', "price": "discount price", "image" : 'img'}, 
{"Rimi": 'scraper\mrimi.html', "article" : "offer-card__content offer-card__section", "headline":"offer-card__name", "discount" : 'badge_c', "price": "price-badge", "image" : 'offer-card__image-cloudinary'}
]

def find_sales(dict):
    with open(list(dict.values())[0], 'rb') as html_file:
        soup = BeautifulSoup(html_file, 'lxml')

    all_sales = []
    for article in soup.find_all('div', class_=list(dict.values())[1]):
        if article is not None:
            headline = article.find('div', class_=list(dict.values())[2]).text.strip()

            discount = article.find('div', class_=list(dict.values())[3])
            price = article.find('div', class_=list(dict.values())[4])
                       
        if discount is not None:
            discount = discount.text.strip()
            
        if price is not None:
            price = price.text.split()
            
            for key, value in dict.items():
                if key == "Rimi":
                    for i in price:
                        if len(price) == 5:
                            new_price = price[0]+"."+price[1]+price[2] 
                            old_price = price[3] + price[4]
                        elif len(price) == 3:
                            new_price = price[0]+"."+price[1]+price[2]
                            old_price = 0
                        elif len(price) == 2:
                            new_price = price[0]+" "+price[1]
                            old_price = 0
                        else:
                            new_price=price[0]
                            old_price = 0
                elif key == "Maxima":
                    for i in price:
                        if len(price) == 2:
                            new_price = price[0]
                            new_price = new_price[:-3]+"."+new_price[-3:]
                            old_price = price[1]
                        else: 
                            new_price = price[0]
                            new_price = new_price[:-3]+"."+new_price[-3:]
                            old_price = 0

            print('Store - ' + list(dict.keys())[0] + ' New price is: ' + str(new_price) + ' Old prise is: ' + str(old_price) + ' Discount is: ' + str(discount))

        for key, value in dict.items():
            if key == "Maxima":
                image = article.find('div', class_=list(dict.values())[5]).img['src']
                url = f'http://www.maxima.ee{image}'
            elif key == "Rimi":
                regex = re.compile(list(dict.values())[5])
                image = article.find('div', class_= regex)
                url = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",str(image))
                url = str(url)
                while True:
                    if url[-1].isalpha() == False:
                        url = url[:-1]
                    elif url[0].isalpha() == False:
                        url = url[1:]
                    else:
                        break

        sales_dict = {"store": list(dict.keys())[0],"headline": headline, "image": url, "discount": discount, "new_price": new_price, "old_price": old_price}
        all_sales.append(sales_dict)
    
    return all_sales 

new_list = []
for i in kauplused:
    new_list.append(find_sales(i))

all_sales_list = flatten(new_list)

