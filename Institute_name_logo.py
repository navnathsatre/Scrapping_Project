import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import json
import os
import numpy as np

base_url = input("Enter Your Institute URL: ")

def Institute_name(base_url):
    
    pattern1 = r'.*\/\/www\.(\w*)\..*'
    pattern2 = r'.*\/\/(\w*)\..*'
    if base_url.find('www.') == -1: 
        Institute = ' '.join(re.findall(pattern2, base_url))
    else:
        Institute = ' '.join(re.findall(pattern1, base_url))
    if Institute.find("college")==-1:
        Institute = Institute+" college"
    else:
        Institute = Institute[:-7]+' '+"college"  
    return Institute
Institute = Institute_name(base_url)

def logo_scrapper(base_url):
    logo_url_final = 'Not Found'
    try:
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML ,\
        like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
        if base_url[-4:] == 'html':
            pattern = r"(.*)\/.*\.html$"
            base_url = ''.join(re.findall(pattern, base_url))
        else:
            base_url
        res = requests.get(base_url, headers=headers)
        if res.status_code == 200:
            webpage=requests.get(base_url, headers=headers).text
            soup=BeautifulSoup(webpage,'lxml')
            doc = soup.find_all(['a','img','h1'])
            for i in doc:
                if i.find('img') != None:
                    try:
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
                    except:
                        print('Not Found')
                elif i.find('h1') != None and i.find('h1').find('xlink') != -1:
                    logo_url_final = "Protected Logo"                        
                elif i.find('h1') != None and i.find('h1').find('Logo') != -1:
                    logo_url_final = i
        else:
            logo_url_final
    except Exception as e:
        print()                      
    return logo_url_final
logo = logo_scrapper(base_url)

# create mapping with dictinary
data_dict = {
    'Institution Name'              :[Institute],
    'Institution Logo'              :[logo]}
columns=['Institution Name','Institution Logo']
# convert into dataframe
df = pd.DataFrame(data_dict,columns=columns)
if os.path.exists('Institute_name_logo.csv') == False :
    df.to_csv("Institute_name_logo.csv", index=False)
else:
    df.to_csv("Institute_name_logo.csv", index=False, mode='a',header=False)
