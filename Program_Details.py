import re
import pandas as pd
import pyap
import wordninja
import requests
from bs4 import BeautifulSoup
headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

def program_details(base_url, program_url):
    
    raw_urls=[]
    webpage = requests.get(program_url, headers=headers).text
    soup = BeautifulSoup(webpage,'html.parser')
    for link in soup.find_all('a'):          #, attrs={'href': re.compile('^\/programs-and-courses\/full-time-programs\/')}
        raw_urls.append(link.get('href'))

    raw_urls = list(set(raw_urls))

    sub_urls = []
    base_url1 = base_url
    try:
        pattern ='\/programs\/'
    except:
        pattern = '.+programs-and-courses.+'
        
    for link in raw_urls:
        if link != None:
            if re.search(pattern, link):
                if link[0]== 'h':
                    sub_urls.append(link)
                else:
                    sub_urls.append(base_url1 + link)


    sub_urls = list(set(sub_urls))
    sub_urls.sort()
    
    webpage_for_base_url = requests.get(base_url1, headers=headers).text
    soup_for_base_url = BeautifulSoup(webpage_for_base_url, 'html.parser')
    
    final = pd.DataFrame()
    for url in sub_urls:
        webpage = requests.get(url, headers=headers).text
        soup = BeautifulSoup(webpage, 'html.parser')
        
        
        def institute_name_scrapper():   
            pattern1 = r'.*\/\/www\.(\w*)\..*'
            pattern2 = r'.*\/\/(\w*)\..*'
            if base_url1.find('www.') == -1: 
                Institute = ' '.join(re.findall(pattern2, base_url))
            else:
                Institute = ' '.join(re.findall(pattern1, base_url))
            if Institute.find("college") == -1:
                Institute = Institute +" college"
            else:
                Institute = ' '.join(wordninja.split(Institute))  
            return Institute
        
        def duration():
            text = soup.text
            try:
                start = text.find('Duration')
                if start == -1:
                    start = text.find('Length')
                    if start == -1:
                        start = text.find('Delivery')
                else:
                    duration1 = 'Not Found'
            except:
                duration1 = 'Not Found'

            duration1 = text[start + 8 : start + 30].strip()

            return duration1

        def program_name():
            course_name = 'Not Found'
            a= soup.find_all("h1")
            for i in a:
                try:
                    course_name = i.text.strip()
                except:
                    course_name = 'Not Found'
            return course_name
        
        def start_intake():
            text = soup.text
            try:
                start = text.find('Start Date')
                if start == -1:
                    start = text.find('Starts')
                    if start ==-1:
                        start=text.find('Program starts')
                        if start==-1:
                            start=text.find("Intake")
                            if start==-1:
                                start=text.find("Start")
                                if start==-1:
                                    start_date = 'Not Found'
                                    
                            
            except:
                start_date = 'Not Found'

            start_date = text[start+5 : start + 35].strip()
            if start==-1:
                start_date = 'Not Found'
            
            return start_date
        
        def status():
            text = soup.text
            try:
                start = text.find('Availability')
                if start == -1:
                    start = text.find('availability')
                    if start == -1:
                        start = text.find('Domestic Availability')
                        if start == -1:
                            start = text.find('domestic availability')
                            if start == -1:
                                start = text.find('STATUS')
                                if start == -1:
                                    start = text.find('status')
                                    if start == -1:
                                        start = text.find('Status')

                else:
                    duration1 = 'Not Found'
            except:
                duration1 = 'Not Found'

            duration1 = text[start+8: start + 13].strip()
            if start == -1:
                duration1 = 'Not Found'

            duration1
            
        def website_link():
            link = url
            
            return link
        
        
        
        
        def country_name_scrapper():
    
            doc = soup_for_base_url.find_all(['p', 'address','br'])

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
        
        institute_name_scrapper = institute_name_scrapper()
        duration1 = duration()
        course_name = program_name()
        start_intake = start_intake()
        status = status()
        website_link = website_link()
        Inst_Currency = inst_currency()

        dict1 = {'institute_name_scrapper':[institute_name_scrapper],'course_name' : [course_name], 'duration':[duration1], 'Intakes Dates': [start_intake],
                'status': [status], 'Link of the Program' : [website_link], 'inst_currency': [Inst_Currency]}

        final = final.append(pd.DataFrame(dict1),ignore_index=True )
    return final

base_url = input('Enter Base Url of Website: ')
program_url = input('Enter Program Url of Website: ')

final_data = program_details(base_url,program_url)


# base_url = https://www.fanshawec.ca/
# program_url = https://www.fanshawec.ca/programs-and-courses

# base_url = https://durhamcollege.ca
# program_url = https://durhamcollege.ca/programs-and-courses