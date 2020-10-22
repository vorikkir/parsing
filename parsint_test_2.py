#!/usr/bin/python3.7
# -*- coding: utf-8 -*-

import requests
import json


def get_page():
    """The function makes a request to the URL"""
    url = 'https://apigate.tui.ru/api/office/list?cityId=1&subwayId=&' \
          'hoursFrom=&hoursTo=&serviceIds=all&toBeOpenOnHolidays=false'
    page = requests.get(url)
    if page.status_code == 200:
        return parsing(requests.get(url).json()['offices'])
    print('Not found')


def create_json(result):
    """The function creates a JSON and writes information to it"""
    with open('site_2.json', 'w', encoding='UTF-8') as f:
        f.write(json.dumps(result, ensure_ascii=False))


def parsing(info):
    """The function gets the necessary information from the site and returns a list"""
    result = []
    for office in info:
        address = office['address']
        latlon = [office['latitude'], office['longitude']]
        name = office['name']
        phones = [i['phone'].strip() for i in office["phones"]]
        working_hours = office['hoursOfOperation']
        time = []
        for day in working_hours:
            if working_hours[day]['isDayOff']:
                continue
            start_time = working_hours[day]['startStr']
            end_time = working_hours[day]['endStr']
            if day == 'workdays':
                time.append(f'пн - пт {start_time} до {end_time}')
            elif day == 'saturday':
                time.append(f'сб {start_time} до {end_time}')
            elif day == 'sunday':
                time.append(f'вс {start_time} до {end_time}')
        result.append({"address": address, "latlon": latlon, "name": name, "phones": phones, "working_hours": time})

    return create_json(result)


if __name__ == '__main__':
    get_page()
