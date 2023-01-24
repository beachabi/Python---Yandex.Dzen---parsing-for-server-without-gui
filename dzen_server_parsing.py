from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By #для by
from selenium.webdriver.common.keys import Keys
import requests #pip install requests
from bs4 import BeautifulSoup #pip install beautifulsoup
import time
import random #pip install random2
import csv #included default
import re



def csv_write (data):

    with open(f'dzen_dillan.csv', 'a', newline = '', encoding = 'utf-8') as file:

        order = [
                    'id_link',
                    'title',
                    'main_image',
                    'article_body'
                ]

        writer = csv.DictWriter(file, fieldnames=order, delimiter='^', quoting=csv.QUOTE_NONE, quotechar='')
        writer.writerow(data)







def fill_dict (soup, link):

    #собираем блоки с данными сам парсинг
    dict_name = dict()

    try:
        dict_name['id_link'] = link
    except:
        dict_name['id_link'] = "no data"


    try:
        dict_name['title'] = soup.find('h1', {'class':'article__title'})
    except:
        dict_name['title'] = "no data"

    
    try:
        dict_name['main_image'] = soup.find('img', {'class':'article-image-item__image'})
    except:
        dict_name['main_image'] = "no data"
    

    try:
        dict_name['article_body'] = soup.find('div', {'class':'article-link__no-carrot-accents'})
    except:
        dict_name['article_body'] = "no data"



    csv_write(dict_name)

        












def open_window (url):
    print("start_parse")

###
    options = webdriver.ChromeOptions()
    options.add_argument(f'--user-agent={random.choice(user_agents)}')
    options.add_argument("--disable-blink-features=AutomationControlled")
###
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
###
    options.add_argument("--headless=chrome")
    driver = webdriver.Chrome(
        executable_path="chromedriver",
        options=options
    )

    driver.get(url = url)
    driver.implicitly_wait(30)

    print("wait")

    #пролистываем страницу до конца
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True


    #парсим общую страницу
    driver.implicitly_wait(30)
    soup = BeautifulSoup(driver.page_source, "lxml")
    blocks = soup.find_all('div', {'class':'feed__row'})

    links = list()
    blocks_href = soup.find_all('a', {'class':'card-image-compact-view__clickable'})

    #парсим ссылки на страницы
    for block in blocks_href:
        # print(block.get('href'))
        id_link = ''.join(map(str, re.findall(r'.*(?=\?)', block.get('href'))))

        if id_link not in links:
            links.append(id_link)
    print(links)
    # print(len(links))

    for link in links:
        print(link)
        driver.get(url = link)
        driver.implicitly_wait(30)
        soup = BeautifulSoup(driver.page_source, "lxml")
        fill_dict(soup, link)









if __name__ == '__main__':

    init_file = {'id_link':'id_link','title':'title','main_image':'main_image','article_body':'article_body'}
    with open(f'dzen_dillan.csv', 'w', newline = '', encoding = 'utf-8') as file:
        order = [
                    'id_link',
                    'title',
                    'main_image',
                    'article_body'
                ]
        writer = csv.DictWriter(file, fieldnames=order, delimiter='^', quoting=csv.QUOTE_NONE, quotechar='')
        writer.writerow(init_file)
        file.close()


    user_agents = [
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 13.0; rv:106.0) Gecko/20100101 Firefox/106.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/106.0.1370.52'
]


    links_for_parse_from_dzen = [
        # "https://dzen.ru/your_name_of_chenel",
        # "https://dzen.ru/your_name_of_chenel",
        # "https://dzen.ru/your_name_of_chenel",
    ]

    for link in links_for_parse_from_dzen:
        open_window(link)