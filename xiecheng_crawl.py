#!/usr/bin/env python
#-*-coding=utf-8-*-

import re
import json
import time
import random
import requests
import datetime
from bs4 import BeautifulSoup
from user_agents import agents


session = requests.session()
session.headers = {"hearders":random.choice(agents)}

def get_flight_info(from_city,to_city,day_time):
    try:
        url = "http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1" \
              "="+str(from_city)+"&ACity1="+str(to_city)+"&SearchType=S&DDate1="+str(day_time)+\
              "&IsNearAirportRecommond=0"
        print(url)
        data = session.get(url,timeout = 30).text
        sleeptime = (1, 2, 3, 4, 10, 20, 1, 2, 1, 3, 1, 4, 50, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2)
        time.sleep(random.choice(sleeptime))
        lowest_price_list = json.loads(data)['lps']
        fis = json.loads(data)['fis']
        for fi in fis:
            flight = fi['fn']
            fly_time = fi['dt']
            arrival_time = fi['at']
            fly_station = fi['dpbn']
            arrival_station = fi['apbn']
            depart_brigdge = json.loads(fi['confort'])['DepartBridge']
            History_Punctuality = json.loads(fi['confort'])['HistoryPunctuality']
            tax = fi['tax']
            print("航班：",flight)
            print("起飞时间：",fly_time)
            print("到达时间：",arrival_time)
            print("廊桥率：",depart_brigdge)
            print("准点率：",History_Punctuality)
            print("出发站台：",fly_station)
            print("到达站台：",arrival_station)
            print("民航发展基金:",tax)
            prices = fi['scs']
            for price in prices:
                alt_price = price['salep']
                print("可选价位",alt_price)
            print("==================================================")
    except Exception as e:
        print("Eorro:",e)
def get_flight_url():
    all_flight_urls = []
    html = session.get('http://flights.ctrip.com/schedule/',timeout = 30).text
    bsobj = BeautifulSoup(html,"lxml")
    city_flights = bsobj.findAll("div",{"class":"m"})
    for city_flight in city_flights:
        flight_urls = re.findall('a href="(.*)"',str(city_flight))
        for flight_url in flight_urls:
            flight_url = 'http://flights.ctrip.com'+flight_url
            all_flight_urls.append(flight_url)
    for url in all_flight_urls:
        days = 1
        crawl_num = 1
        while days<90:
            if crawl_num >10:
                crawl_num -= 10
                print("please wait for moment")
                time.sleep(60)
            today = datetime.date.today()
            next_day = datetime.date(today.year, today.month,today.day) + datetime.timedelta(days)
            next_day = '{}-{}-{}'.format(next_day.year,next_day.month,next_day.day)
            print("出发日期：",next_day)
            sleeptime = (1, 2, 3, 4, 10, 20, 1, 2, 1, 3, 1, 4, 50, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2)
            time.sleep(random.choice(sleeptime))
            html = session.get(url,timeout = 30).text
            crawl_num += 1
            bsobj = BeautifulSoup(html,'lxml')
            contents = bsobj.findAll('div',{"class":"m"})
            for content in contents:
                city_city_flights = re.findall('a href="(.*)"',str(content))
                for city_city_flight in  city_city_flights:
                    citys = city_city_flight.split('/')[4].split('.')
                    from_city = citys[0]
                    to_city = citys[1]
                    print(from_city,to_city)
                    get_flight_info(from_city,to_city,next_day)
                    crawl_num += 1
                    time.sleep(10)
            days += 1

get_flight_url()
