'''
Simple Scraper of Fox News Headlines
inspo credit: https://github.com/SethConnell/Fox-News-Web-Scraper
'''
#import requests
import csv
from datetime import datetime
from bs4 import BeautifulSoup
#import urllib

#import time
import schedule

# import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DATA = []


def get_headlines(containers):
    '''
    Retrieves headline, access date, *publish data, url, category
    '''
    global DATA
    for article in containers:
        headline = article.getText()
        url = article.find('a').get('href')
        access_date = datetime.today().strftime('%Y-%m-%d')

        categories = ['/us/', '/politics/', '/auto/', '/money/', '/lifestyle/', '/entertainment/',
                      '/technology/', '/world/', '/sports/', '/real-estate/',
                      '/science/', '/media/', '/opinion/', '/tech/', '/great-outdoors/',
                      '/food-drink/', '/health/']

        for cat in categories:
            if cat in url:
                category = cat.replace('/', '')

        if '/v/' in url or '/watch/' in url:
            video = True
            category = 'video'
        else:
            video = False

        data = {'headline': headline,
                'category': category,
                'access_date': access_date,
                'video': video,
                'url': url}
        DATA.append(data)


def scrape_fox():
    '''
    Scrape FOX News home page, returns soup object
    '''
    global DATA
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Chrome(chrome_options=options)
    url = 'http://www.foxnews.com'
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'lxml')

    headers = soup.find_all('h2', {'class': 'title'})
    sub_headers = soup.find_all('li', {'class': 'related-item'})
    scroll_bar_art = soup.find_all('article', {'class': 'article-ct'})

    containers = headers + sub_headers + scroll_bar_art
    get_headlines(containers)


def write():
    '''
    Write all retrieved data into csv file
    '''
    global DATA
    # write DATA into FOX_scrape.csv file
    keys = ['headline', 'category', 'publish_date',
            'access_date', 'video', 'url']

    with open('FOX_scrape.csv', 'a+', newline='') as out_file:
        dict_writer = csv.DictWriter(out_file, fieldnames=keys)
        # dict_writer.writeheader()
        dict_writer.writerows(DATA)


scrape_fox()
write()

schedule.every(1).day.at('09:00').do(scrape_fox)
schedule.every(1).day.at('09:00').do(write)
