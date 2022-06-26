import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import json
import os
import numpy as np
import pyap
import wordninja

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}


def institute_name_scrapper():   
    pattern1 = r'.*\/\/www\.(\w*)\..*'
    pattern2 = r'.*\/\/(\w*)\..*'
    if base_url.find('www.') == -1: 
        Institute = ' '.join(re.findall(pattern2, base_url))
    else:
        Institute = ' '.join(re.findall(pattern1, base_url))
    if Institute.find("college") == -1:
        Institute = Institute +" college"
    else:
        Institute = ' '.join(wordninja.split(Institute))  
    return Institute
# Institute_name(base_url)

def logo_scrapper():
    logo_url_final = 'Not Found'

    #     soup = BeautifulSoup(urllib2.urlopen(url).read())
    doc = soup.find_all(['a','img'])
    for i in doc:
            if i.find('img') != None:
                if i.find('img')['src'].find('logo') != -1 or \
                    i.find('img')['src'].find('Logo') != -1 or \
                    i.find('img')['alt'].find('Logo') != -1 or \
                    i.find('img')['alt'].find('logo') != -1:

                    logo_url = i.find('img')['src']
                    if logo_url[0] == 'h':
                        logo_url_final = logo_url
                    else:
                        logo_url_final = base_url + logo_url

                    break
                else:
                    continue
                        
    return logo_url_final

def address_scrapper():
    
    doc = soup.find_all(['p', 'address','br'])

    final_text = ''
    for i in doc:
        final_text = final_text + i.text + ' '

    addresses = pyap.parse(final_text, country='CA')

    all_addresses = ' | '.join([str(i) for i in addresses])
    
    if all_addresses == '':
        addresses = pyap.parse(final_text, country='US')
        all_addresses = ' | '.join([str(i) for i in addresses])
        
        if all_addresses == '':
            all_addresses = 'Not Found'

    return all_addresses


def country_name_scrapper():
    
    doc = soup.find_all(['p', 'address','br'])

    final_text = ''
    for i in doc:
        final_text = final_text + i.text + ' '
    
    country_name = 'Not Found'
    
    
    addresses = pyap.parse(final_text, country='CA')
    

    if addresses:
        for address in addresses:
            address_dict = address.as_dict()
            if address_dict['country_id'] == 'CA':
                country_name = 'Canada'

    else:
        addresses = pyap.parse(final_text, country='US')
        for address in addresses:
            address_dict = address.as_dict()
            if address_dict['country_id'] == 'US':
                country_name = 'USA'

    return country_name

def inst_currency():
    InstCurrency = 'Not Found'
    
    country_name = country_name_scrapper()
    if country_name == 'Canada':
        InstCurrency = 'Canadian dollar(Can$)'
    elif country_name == 'USA':
        InstCurrency = 'United States Dollar($)'

    return InstCurrency

def provience_name_scrapper():
    doc = soup.find_all(['p', 'address','br'])

    final_text = ''
    for i in doc:
        final_text = final_text + i.text + ' '
    
    provience_name = 'Not Found'
    
    addresses = pyap.parse(final_text, country='CA')
    

    if addresses:
        for address in addresses:
            address_dict = address.as_dict()
            provience_name = address_dict['region1']

    else:
        addresses = pyap.parse(final_text, country='US')
        for address in addresses:
            address_dict = address.as_dict()
            provience_name = address_dict['region1']

    return provience_name

def city_name_scrapper():
    doc = soup.find_all(['p', 'address','br'])

    final_text = ''
    for i in doc:
        final_text = final_text + i.text + ' '
    
    city_name = 'Not Found'
    
    addresses = pyap.parse(final_text, country='CA')
    

    if addresses:
        for address in addresses:
            address_dict = address.as_dict()
            city_name = address_dict['city']

    else:
        addresses = pyap.parse(final_text, country='US')
        for address in addresses:
            address_dict = address.as_dict()
            city_name = address_dict['city']

    return city_name

def postal_code_scrapper():
    doc = soup.find_all(['p', 'address','br'])

    final_text = ''
    for i in doc:
        final_text = final_text + i.text + ' '
    
    postal_code = 'Not Found'
    
    addresses = pyap.parse(final_text, country='CA')
    

    if addresses:
        for address in addresses:
            address_dict = address.as_dict()
            postal_code = address_dict['postal_code']

    else:
        addresses = pyap.parse(final_text, country='US')
        for address in addresses:
            address_dict = address.as_dict()
            postal_code = address_dict['postal_code']

    return postal_code

def postal_code_scrapper():

    doc = soup.find_all(['p', 'address','br'])

    final_text = ''
    for i in doc:
        final_text = final_text + i.text + ' '
    
    postal_code = 'Not Found'
    
    addresses = pyap.parse(final_text, country='CA')
    

    if addresses:
        for address in addresses:
            address_dict = address.as_dict()
            postal_code = address_dict['postal_code']

    else:
        addresses = pyap.parse(final_text, country='US')
        for address in addresses:
            address_dict = address.as_dict()
            postal_code = address_dict['postal_code']

    return postal_code

def data_scrapper():
    
    Institute_name = institute_name_scrapper(),
    logo = logo_scrapper()
    address = address_scrapper()
    country_name = country_name_scrapper()
    provience_name = provience_name_scrapper()
    city_name = provience_name_scrapper()
    postal_code = postal_code_scrapper()
    inst_currency1 = inst_currency()
    
    # create mapping with dictinary
    data_dict = {
        'Institution Name'              : Institute_name,
        'Institution Logo'              : logo,
        'Institution address'           : address,
        'country_name'                  : country_name,
        'provience_name'                : provience_name,
        'city_name'                     : city_name,
        'postal_code'                   : postal_code,
        'website'                       : base_url,
        'inst currency'                 : inst_currency1
    }

    # convert into dataframe
    df = pd.DataFrame(data_dict)
    
    return df


# base_url = input('Enter Institute base URL : ')

final = pd.DataFrame()

with open("Input_URLS", 'r') as f:
    URLS = f.readlines()

for url in URLS:
    base_url = url.replace('\n','')
    try:
        res = requests.get(base_url, headers=headers)
        webpage = requests.get(base_url, headers=headers).text
        soup = BeautifulSoup(webpage,'lxml')
        df = data_scrapper()
        final = final.append(df, ignore_index=True)
        
    except Exception as e:
        print(e)
        print("Invalid URL")
        
final.to_csv('Institute_Details2.csv')