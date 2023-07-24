from bs4 import BeautifulSoup
import requests
import csv

with open('scraper\maxima.html', 'rb') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

csv_file = open('maxima_scrape.csv', 'w')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['headline', 'image', 'discount', 'new_price'])


for article in soup.find_all('div', class_='col-third'):
    if article is not None:
        headline = article.find('div', class_='title').text
        print(headline)

        discount = article.find('div', class_='discount percents')
        price = article.find("div", {"class":'discount price'})
        
        
        if discount is not None:
            discount = discount.text
        
        if price is not None:
            print(price.text.split())

        image = article.find('div', class_='img').img['src']
        img_link = f'http://www.maxima.ee{image}'

        print(img_link)

        print('  ')

        csv_writer.writerow([headline, img_link, discount])



csv_file.close()
