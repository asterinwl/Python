import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
#import datetime
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta

es = Elasticsearch('http://127.0.0.1:9200')

#키워드는 "빅데이터","빅데이타" 연관검색어는 1개만 넣는것이 좋음 (중복된 데이터가 수집됨) 
competitor=['카카오','삼성sds','lgcns','디리아','메가존클라우드','nshc',"cloudera","엘라스틱서치코리아","네이버","이지팜"]
bigdata_industry = ["빅데이터", "마이데이터", "가트너","DW", "데이터웨어하우스", "Migration", "ETL","EAI","ESB","cloud","AWS","GCP"]
bigdata_solution = ["splunk","apache kafka", "apache spark", "elasticsearch","zookeeper", "confluent","yarn","kibana","logstash","file beats","docker","kubernetes"]
keyword = [competitor , bigdata_industry , bigdata_solution]

now = datetime.now()
today = now.strftime('%Y-%m-%d')
yesterday = now - timedelta(days=1)
yesterday = yesterday.strftime('%Y-%m-%d-%H-%M')

title_list = []
url_list = []
comp_list = []
thumbnail_list = []
text_list = []
day_list = []
keyword_list =[]
category_list = []
keyword = sum(keyword,[])


for j in range(len(competitor)+len(bigdata_industry)+len(bigdata_solution)) :      
    
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

        try:
            thumbnail = article.select_one('div > a > img')['src']
            thumbnail_list.append(thumbnail.strip())

        except:
            thumbnail_list.append(
                'https://search.pstatic.net/common/?src=https%3A%2F%2Fimgnews.pstatic.net%2Fimage%2Forigin%2F366%2F2021%2F09%2F23%2F762207.jpg&type=ff264_180&expire=2&refresh=true')
        # 일부 기사는 이미지가 없는 경우가 있다. 따라서 이미지가 없는 경우 기본값을 설정해주었다.
        

        if (keyword[j] in competitor):
            category_list.append("competitor")

        elif (keyword[j] in bigdata_industry):
            category_list.append("bigdata_industry")

        elif (keyword[j] in bigdata_solution):
            category_list.append("bigdata_solution")
        
            
info = {'title':title_list, 'url':url_list, 'company':comp_list, 'contents':text_list, 'date':day_list, 'image':thumbnail_list ,'keyword':keyword_list, 'category': category_list}

index_name = 'newsletter'+"_"+today

for i in range(len(info['title'])):
    es.index(index=index_name, 
            doc_type='_doc', 
            body={'title':info['title'][i],
            'url':info['url'][i], 
            'company':info['company'][i],
            'contents':info['contents'][i], 
            'date':info['date'][i],
            'image':info['image'][i],
            'keyword':info['keyword'][i],
            'category':info['category'][i]})

es.indices.put_alias(index = index_name, name = 'newsletter')