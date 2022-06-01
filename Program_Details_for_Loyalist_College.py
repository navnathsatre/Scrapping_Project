# Import libraris
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import json
import os
import numpy as np
from requests.models import MissingSchema
import trafilatura

def Program_Details_Scrapper(base_url):
    page_source = requests.get(base_url)
    soup = BeautifulSoup(page_source.content, 'html.parser',from_encoding="utf-8")


    # Define Function for data extraction
    def beautifulsoup_extract_text_fallback(response_content):

        '''
        This is a fallback function, so that we can always return a value for text content.
        Even for when both Trafilatura and BeautifulSoup are unable to extract the text from a 
        single URL.
        '''

        # Create the beautifulsoup object:
        soup = BeautifulSoup(response_content, 'html.parser',from_encoding="utf-8")

        # Finding the text:
        text = soup.find_all(text=True)

        # Remove unwanted tag elements:
        cleaned_text = ''
        blacklist = [
            '[document]',
            'noscript',
            'header',
            'html',
            'meta',
            'head', 
            'input',
            'script',
            'style',]

        # Then we will loop over every item in the extract text and make sure that the beautifulsoup4 tag
        # is NOT in the blacklist
        for item in text:
            if item.parent.name not in blacklist:
                cleaned_text += '{} '.format(item)

        # Remove any tab separation and strip the text:
        cleaned_text = cleaned_text.replace('\t', '')
        cleaned_text = re.sub(r"[^a-z A-Z 0-9$£]","",cleaned_text)
        return cleaned_text.strip()


    def extract_text_from_single_web_page(url):

        downloaded_url = trafilatura.fetch_url(url)
        try:
            a = trafilatura.extract(downloaded_url, include_links=True,deduplicate=True,output_format='json', with_metadata=True, include_comments = False,
                                date_extraction_params={'extensive_search': True, 'original_date': True})
        except AttributeError:
            a = trafilatura.extract(downloaded_url, include_links=True,deduplicate=True,output_format='json', with_metadata=True,
                                date_extraction_params={'extensive_search': True, 'original_date': True})
        if a:
            json_output = json.loads(a)
            return json_output['text']
        else:
            try:
                resp = requests.get(url)
                # We will only extract the text from successful requests:
                if resp.status_code == 200:
                    return beautifulsoup_extract_text_fallback(resp.content)
                else:
                    # This line will handle for any failures in both the Trafilature and BeautifulSoup4 functions:
                    return np.nan
            # Handling for any URLs that don't have the correct protocol
            except MissingSchema:
                return np.nan
    
    
    # Collect all urls
    raw_urls = []
    for link in soup.find_all('a'):          
        raw_urls.append(link.get('href'))
    raw_urls = list(raw_urls)
    
    
    #take relevent urls
    sub_urls = []
    base = 'https://www.loyalistcollege.com'
    pattern ='^\/programs-and-courses\/full-time-programs\/.+'
    for link in raw_urls:
        if link != None:
            if re.search(pattern, link):
                sub_urls.append(base + link)
    sub_urls = set(sub_urls)
    sub_urls = list(sub_urls)
    sub_urls.sort()
    
    # extract text
    text_content = [extract_text_from_single_web_page(url) for url in sub_urls]
    
    
    directory = "loyalist_college_data"
    if not os.path.exists(directory):
        os.mkdir(directory)
        
    # Serializing json 
    json_object = json.dumps(text_content, indent = 2)

    # Writing to sample.json
    with open(directory+"/"+"loyalist_colleges.json", "w") as outfile:
        outfile.write(json_object)
        
Program_Details_Scrapper('https://www.loyalistcollege.com/programs-and-courses/full-time-programs/')


def Program_details_Mapper():

    # Opening JSON file
    with open('loyalist_college_data/loyalist_colleges.json', 'r') as openfile:

        # Reading from json file
        json_object = json.load(openfile)

    # Define Functios 
    def Program_name():
        pattern = '\A.*'
        return [''.join(re.findall(pattern, string)) for string in json_object]

    def Credential():
        pattern = '-\sCredential\n(.*)'
        return [''.join(re.findall(pattern,string)) for string in json_object]

    def Start_Date():
        pattern = '-\sStart\sDate\n(.*)'
        return [''.join(re.findall(pattern,string)) for string in json_object]

    def Location():
        pattern = '-\sLocation\n(.*\sCampus).*'
        return [''.join(re.findall(pattern,string)) for string in json_object]

    def Discriptions():
        pattern = "^[F|f]ind\s[y|Y]our\s[c|C]areer(.*)Is\sit\sfor\syou/?"
        return [''.join(re.findall(pattern,string,re.MULTILINE | re.DOTALL)).replace('\n',' ') for string in json_object]

    def Is_it_for_you():
        pattern = "^Is\sit\sfor\syou\?(.*)Experiential\slearning"
        return [''.join(re.findall(pattern,string,re.MULTILINE | re.DOTALL)).replace('\n',' ') for string in json_object]

    def Duration():
        Duration = []
        pattern = "^.*\sYear\s-\sSemester\s.*$"
        Year_Semester = [''.join(re.findall(pattern,string,re.MULTILINE )).replace('\n',' ') for string in json_object]
        for year in Year_Semester:
            if re.findall("Fourth Year", year) :
                Duration.append('4 Year')
            elif re.findall("Third Year", year) :
                Duration.append('3 Year')
            elif re.findall("Second Year", year) :
                Duration.append('2 Year')
            elif re.findall("First Year", year) :
                Duration.append('1 Year')
            else :
                Duration.append(' ')
        return Duration

    def Semester():
        Semester = []
        pattern = "^.*\sYear\s-\sSemester\s.*$"
        Year_Semester = [''.join(re.findall(pattern,string,re.MULTILINE )).replace('\n',' ') for string in json_object]
        for year in Year_Semester:
            if re.findall("Fourth Year", year) :
                Semester.append('8 Semester')
            elif re.findall("Third Year", year) :
                Semester.append('6 Semester')
            elif re.findall("Second Year", year) :
                Semester.append('4 Semester')
            elif re.findall("First Year", year) :
                Semester.append('2 Semester')
            else :
                Semester.append(' ')
        return Semester

    def Tuition_Fee():
        pattern = "Approximate\scosts.*\n.*:\s(.*)\n.*\n.*"
        return [''.join(re.findall(pattern,string)).replace('\n',' ') for string in json_object]

    def Ancillary_Fees():
        pattern = "Approximate\scosts.*\n.*\n.*(\$.*)\n.*\n.*"
        return [''.join(re.findall(pattern,string)).replace('\n',' ') for string in json_object]

    def Mode():
        pattern = "Approximate\scosts.*\n.*\n-\s(Full-Time|Online)\s.*\n.*\n.*"
        return [''.join(re.findall(pattern,string)).replace('\n',' ') for string in json_object]

    def Admission_requirements():
        pattern = "with\sa\sstudent\sloan\.(.*)\[Click\shere\]"
        return [''.join(re.findall(pattern,string,re.MULTILINE | re.DOTALL)).replace('\n',' ') for string in json_object]

    def Link_of_the_program():   
        base_url = 'https://www.loyalistcollege.com/programs-and-courses/full-time-programs/'
        page_source = requests.get(base_url)
        soup = BeautifulSoup(page_source.content, 'html.parser',from_encoding="utf-8")
        raw_urls = []
        for link in soup.find_all('a'):        
            raw_urls.append(link.get('href'))
        raw_urls = list(raw_urls)
        sub_urls = []
        base = 'https://www.loyalistcollege.com'
        pattern ='^\/programs-and-courses\/full-time-programs\/.+'
        for link in raw_urls:
            if link != None:
                if re.search(pattern, link):
                    sub_urls.append(base + link)
        sub_urls = set(sub_urls)
        sub_urls = list(sub_urls)
        sub_urls.sort()
        return sub_urls

    # create mapping with dictinary
    data_dict = {
        'Institution Name'              :'Loyalist College Canada',
        'Program Name'                  :Program_name(),
        'Mode'                          :Mode(),
        'Duration of program'           :Duration(),
        'No of Semester'                :Semester(),
        'Currency used in the country'  :'CAD$',
        'Level of Education(Credential)':Credential(),
        'Start Date'                    :Start_Date(),
        'Location'                      :Location(),
        'Discriptions'                  :Discriptions(),
        'Is it for you ?'               :Is_it_for_you(),
        'Tuition Fee'                   :Tuition_Fee(),
        'Ancillary Fees'                :Ancillary_Fees(),
        'Admission requirements'        :Admission_requirements(),
        'Link of the program'           :Link_of_the_program()
                 }
    # convert into dataframe
    df = pd.DataFrame(data=data_dict)

    #convert into excel
    df.to_excel("loyalist_college_data/LOYALiST_COLLEGE_Details.xlsx", index=False)
    

Program_details_Mapper()