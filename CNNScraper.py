import requests
from bs4 import BeautifulSoup
import csv
import urllib
from datetime import datetime

import time
import schedule

# import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

data = []


def scrapeCNN():
    global data
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Chrome(chrome_options=options)
    url = 'http://www.cnn.com'
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    containers = soup.find_all('h3', {'class': 'cd__headline'})
    getHeadlines(containers)


def getHeadlines(containers):
    global data
    data = []

    for article in containers:
        headline = article.find(class_='cd__headline-text').getText()
        url = article.find('a').get('href')
        access_date = datetime.today().strftime('%Y-%m-%d')

        categories = ['/us/', '/weather/', '/tech/', '/health/', '/politics/', '/travel/',
                      '/opinions/', '/business/', '/entertainment/', '/investing/',
                      '/india/', '/success/', '/celebrities/', '/mark/', '/europe/',
                      '/americas/', '/asia/', '/style/', '/uk/', '/cnn-underscored/', 'foodanddrink']

        if 'bleacherreport' in url:
            category = 'sports'

        try:
            for cat in categories:
                if cat in url:
                    category = cat.replace('/', '')

        except:
            pass

        try:
            if '/videos' in url:
                video = True
                publish_date = '-'.join(url.split('/')[3:6])
            else:
                video = False
                publish_date = '-'.join(url.split('/')[1:4])

        except:
            pass

        d = {'headline': headline,
             'category': category,
             'publish_date': publish_date,
             'access_date': access_date,
             'video': video,
             'url': url}
        data.append(d)


def write():
    global data
    scrapeCNN()
    # write data into CNN_scrape.csv file
    keys = ['headline', 'category', 'publish_date',
            'access_date', 'video', 'url']

    with open('CNN_scrape.csv', 'a+', newline='') as write_obj:
        # create writer object
        dict_writer = csv.DictWriter(write_obj, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


# scrapeCNN()
# write()

schedule.every(1).day.at('09:00').do(scrapeCNN)
schedule.every(1).day.at('09:00').do(write)
