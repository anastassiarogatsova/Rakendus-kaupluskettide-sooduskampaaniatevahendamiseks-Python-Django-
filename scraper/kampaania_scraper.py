from bs4 import BeautifulSoup
import requests
import csv
import re

kampaaniad = [
    {"Maxima": 'scraper/maxima_kamp.html'},
    {"Rimi": 'scraper/rimi_kamp.html'}
    ]


for item in kampaaniad:
    with open(list(item.values())[0], 'rb') as html_file:
        soup = BeautifulSoup(html_file, 'lxml')
        if list(item.keys())[0] == "Rimi":
            for article in soup.find_all('a', class_='gtm lottery-card js-slick-slide lottery-card--loyalty'):
                if article is not None:  
                    url = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",str (article))
                    kmp_url = url[0]
                    print(kmp_url)
                    bg_image = url[1]
                    description = article.find('div', class_='title')
                    period_date = article.find('div', class_='date')
                    if description and period_date is not None:
                        desc = description.text.strip()
                        date = period_date.text.strip()
                        wholedesc = desc + " " + date
                

        if list(item.keys())[0] == "Maxima":
            for article in soup.find_all('div', class_='col col-5'):
                if article is not None:
                    bg_image = article.find('div', class_='coverc')
                    url = re.findall("/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+g",str(bg_image))
                    listToString = ' '.join(map(str, url))
                    kmp_url = 'www.maxima.ee' + listToString
                    url = article.find('a', class_="item", href=True)
                    bg_image = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",str(url))
                    description = article.find('div', class_='title')
                    if description is not None:
                        wholedesc = description.text.strip()
                        

                
                



