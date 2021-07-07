
working_dir = ".\Institutions_Data"


urls = ["https://targetstudy.com/coaching/engineering-entrance-exams-coaching-in-jaipur.htm"]


for a in urls:
    print(a)


import requests as R
from bs4 import BeautifulSoup as bs
import csv


def get_data(url):
    
    agent = {'User-Agent':'Mozilla/5.0'}
    source = R.get(url,headers=agent)
    soup = bs(source.content,'html5lib')
    
    return soup


def scrape(soup):
    
    places = []
    
    for sel in soup.findAll('div',attrs = {'class':'card-body'}):

        place = {}
        sel1 = sel.find('a',attrs = {'class':'card-title h5'})
        
        name = str(sel1)[str(sel1).find('">')+2:str(sel1).find('</a>')]
        
        if len(name) < 5:
            continue
        
        place['name'] = name
        
        sel1 = sel.find('p',attrs = {'class':'card-subtitle mt-0'})
        
        place['address'] = str(sel1)[str(sel1).find('</i>')+5:str(sel1).find('</p>')-17]
        
        sel1 = sel.find('div', attrs = {'class':'media-body'})
        
        if str(sel1).find("phone_iphone") == -1:
            place['contact'] = str(sel1)[str(sel1).find('dark">call')+15:str(sel1).find('</p>',str(sel1).find('dark">call'))-17]
        else:
            place['contact'] = str(sel1)[str(sel1).find('dark">call')+15:str(sel1).find('<i class',str(sel1).find('dark">call'))-3] + '  Mob. - ' + str(sel1)[str(sel1).find('iphone')+11:str(sel1).find('</div>')-35]
        
        sel1 = sel.find('ul',attrs = {'class':'list-info'})
        
        place['subjects'] = str(sel1)[str(sel1).find('<li>')+4:str(sel1).find('</li>')]
        
        if place['subjects'].find('<span') == -1:
            place['subjects']
        else:
            place['subjects'] = place['subjects'].split('<span')[0]
        places.append(place)

    return places


import pandas as pd

final=None

for url in urls:
    
    soup = get_data(url)
    
    info = scrape(soup)
    temp = pd.json_normalize(info)

    try:
        
        final = pd.concat([final,temp],axis=0)
    
    except:
        
        final = temp
    


final['city'] = final['address'].apply(lambda x : x.split(",")[-3].lstrip().rstrip() )
final['district'] = final['address'].apply(lambda x : x.split(",")[-2].lstrip().rstrip() )
final['state'] = final['address'].apply(lambda x : x.split(",")[-1].lstrip().rstrip() )
final['subjects'] = final['subjects'].apply(lambda x : x.replace('&amp;','and') )



final.head()



file_name = working_dir+"\Rajasthan_Institutes_TargetStudy_03.csv"



final.to_csv(file_name,index=False)





