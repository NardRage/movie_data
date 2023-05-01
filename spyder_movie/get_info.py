# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     get_info
   Description :   
   Author :       admin
   date：          2023/4/20
-------------------------------------------------
   Change Activity:
                   2023/4/20 16:38: 
-------------------------------------------------
"""
import json
import re
from xml import etree

import requests
from bs4 import BeautifulSoup


def get_film_infos():
    url = fr'https://movie.douban.com/top250?start=225&filter='

    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept - Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'Keep-Alive',
        'Host': 'movie.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.0.0'
                      ' Chrome/86.0.4240.111 Safari/537.36 Edge/15.15063'}
    response = requests.get(url, headers=headers, timeout=5)

    soup = BeautifulSoup(response.text, 'html.parser')

    movie_list = soup.find_all('div', class_='item')

    film_list = []
    for movie in movie_list:

        text = movie.find('p', class_='').text

        director_pattern = r'导演: (\S+\s*\S+)\s+'
        actor_pattern = r'主演: (\S+\s*\S+).*?'
        year_pattern = r'(\d{4})'
        country_pattern = r'\/\s+(\S+)\s+\/'
        genre_pattern = r'\/\s+(\S+\s*\S+)\s*$'
        film_dict = {}
        try:
            director = re.findall(director_pattern, text)[0]
            actor = re.findall(actor_pattern, text)[0]
            year = re.findall(year_pattern, text)[0]
            country = re.findall(country_pattern, text)[0]
            genre = re.findall(genre_pattern, text)[0]
            title = movie.find('span', class_='title').text
            rating = movie.find('span', class_='rating_num').text
            film_dict["name"] = title
            print("影片名称:", title)
            film_dict["rating"] = rating
            print("评分:", rating)
            film_dict['director'] = director
            print("导演:", director)
            film_dict['actor'] = actor
            print("演员:", actor)
            film_dict['year'] = year
            print("上映时期:", year)
            film_dict['country'] = country
            print("国家:", country)
            film_dict['type'] = genre
            print("影片类型:", genre)
            film_list.append(film_dict)
        except IndexError:
            pass

    with open(fr'../json_data/film.json', 'a+') as f:
        for value in film_list:
            print(value)
            json_data = json.dumps(value, ensure_ascii=False)
            print(json_data)
            f.write(json_data + '\n')

        f.close()


# get_film_infos()

def get_actor_infos():
    urls = ['http://star.iecity.com/{}/'.format(i) for i in range(5249500000, 5249505653)]
    for url in urls:
        headers = {
            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept - Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'Keep-Alive',
            'Host': 'movie.douban.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.0.0'
                          ' Chrome/86.0.4240.111 Safari/537.36 Edge/15.15063'}
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            actor_list = soup.find_all('div',class_='NewsText')
            for actor_info in actor_list:
                print(actor_info)

get_actor_infos()
