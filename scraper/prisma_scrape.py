#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
import csv

urls = ['scraper\juust.html', 'scraper\kala.html', 'scraper\leib.html', 'scraper\liha.html', 'scraper\piim.html']
csv_file = open('prisma_scrape.csv', 'a')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['headline', 'image', 'kampaania', 'new_price'])

for i in urls:
    with open(i, 'rb') as html_file:
        soup = BeautifulSoup(html_file, 'lxml')

        

        for article in soup.find_all('li', class_='relative item effect fade-shadow js-shelf-item'):
            
            headline = article.find('div', class_='name').text.strip()
            subname = article.find('span', class_='subname').text.strip()
            print(headline + ' ' + subname)

            kampaania = article.find('div', class_='offer-info')
            price = article.find('div', class_='price-and-quantity')
                
                
            if kampaania is not None:
                kampaania = kampaania.text.strip()
                print(kampaania)
                
            if price is not None:
                price = price.text.split()
                for i in price:
                    if len(price) == 5:
                        new_price = price[0]+"."+price[1]+price[2] + ' , ' + price[3] + price[4]
                    elif len(price) == 3:
                        new_price = price[0]+"."+price[1]+price[2]
                    elif len(price) == 2:
                        new_price = price[0]+" "+price[1]
                    else:
                        new_price=price[0]

            
            image = article.find('div', class_= 'image-wrapper relative js-image-wrapper clearfix').img['src']

            print(image)


            print('  ')

            csv_writer.writerow([headline, image, kampaania, new_price])


csv_file.close()