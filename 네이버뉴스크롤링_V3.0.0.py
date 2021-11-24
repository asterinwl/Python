import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
#import datetime
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta

es = Elasticsearch('http://127.0.0.1:9200')


keyword=['카카오','삼성sds','lgcns','디리아','메가존클라우드','nshc']


now = datetime.now()
today = now.strftime('%Y.%m.%d')
yesterday = now - timedelta(days=1)
yesterday = yesterday.strftime('%Y.%m.%d.%H.%M')

title_list = []
url_list = []
comp_list = []
thumbnail_list = []
text_list = []
day_list = []
keyword_list =[]




for j in range(len(keyword)) :      
    
    response1 = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query='+ keyword[j]
    response2= '&sort=0&photo=0&field=0&pd=4&ds=' + today + '&de=' + yesterday + '&cluster_rank=27&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:1d,a:all&start='
 
    response = requests.get(response1+response2+str(1))
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.select('#main_pack > section > div > div.group_news > ul > li')
    

    for article in articles:
        a_tag1 = article.select_one('.news_tit')
            
        title = a_tag1.text
        title_list.append(title.strip())
            

        url = a_tag1['href']
        url_list.append(url.strip())

        comp = article.select_one('a.info.press').text
        comp = comp.replace('언론사 선정', '')
        comp_list.append(comp.strip())

        text = article.select_one('a.api_txt_lines.dsc_txt_wrap').text
        text_list.append(text.strip())

        day_list.append(today)
            
        keyword_list.append(keyword[j])
info = {'title':title_list, 'url':url_list, 'company':comp_list, 'contents':text_list, 'date':day_list, 'keyword':keyword_list}


index_name = 'newstest'+"_"+today

for i in range(0,len(info['title'])):
    es.index(index=index_name, 
            doc_type='string', 
            body={'title':info['title'][i],
            'url':info['url'][i], 
            'company':info['company'][i],
            'contents':info['contents'][i], 
            'date':info['date'][i], 
            'keyword':info['keyword'][i]})


es.indices.put_alias(index = index_name, name = 'newsletter')