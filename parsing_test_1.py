#!/usr/bin/python3.7
# -*- coding: utf-8 -*-

import requests
import json

from bs4 import BeautifulSoup


def get_hthl():
    """The function makes a request to the URL"""
    url = 'https://www.mebelshara.ru/contacts'
    page = requests.get(url)
    if page.status_code == 200:
        return parsing(page.text)
    print('Not found')


def create_json(result):
    """The function creates a JSON and writes information to it"""

    with open('site_1.json', 'w', encoding='UTF-8') as f:
        f.write(json.dumps(result, ensure_ascii=False))


def parsing(html):
    """The function gets the necessary information from the site and returns a list"""
    soap = BeautifulSoup(html, 'lxml')
    cities = soap.find_all(class_="expand-block top-border")
    result = []
    for shops in cities:
        if len(shops.find_all(class_="shop-list-item")) > 1:
            for shop in shops.find_all(class_="shop-list-item"):
                address = f'{shops.find(class_="js-city-name").text.strip()}, ' \
                          f'{shop.find(class_="shop-address").text.strip()}'
                latlon = [float(shop.get('data-shop-latitude')), float(shop.get('data-shop-longitude'))]
                name = shop.find(class_="shop-name").text.strip()
                phones = [shop.find(class_="shop-phone").text.strip().replace('(', '').replace(')', '')]
                if shop.find(class_="shop-work-time").text.strip().startswith('Без'):
                    working_hours = [f'пн - вс {shop.find(class_="shop-weekends").text[13:].strip()}']
                else:
                    working_hours = [shop.find(class_="shop-work-time").text.strip(),
                                     shop.find(class_="shop-weekends").text.strip()[14:]
                                     ]
                result.append({"address": address, "latlon": latlon, "name": name,
                               "phones": phones, "working_hours": working_hours})
        else:
            address = f'{shops.find(class_ = "js-city-name").text.strip()},' \
                      f' {shops.find(class_="shop-address").text.strip()}'
            latlon = [float(shops.find(class_="shop-list-item").get('data-shop-latitude')),
                      float(shops.find(class_="shop-list-item").get('data-shop-longitude'))
                      ]
            name = shops.find(class_="shop-name").text.strip()
            phones = [shops.find(class_="shop-phone").text.strip().replace('(', '').replace(')', '')] # улучшить!

            if shops.find(class_="shop-work-time").text.strip().startswith('Без'):
                working_hours = [f'пн - вс {shops.find(class_="shop-weekends").text[13:].strip()}']
            else:
                working_hours = [shops.find(class_="shop-work-time").text.strip(),
                                 shops.find(class_="shop-weekends").text.strip()[14:]]
            result.append({"address": address, "latlon": latlon, "name": name,
                           "phones": phones, "working_hours": working_hours})
    return create_json(result)


if __name__ == '__main__':
    get_hthl()
