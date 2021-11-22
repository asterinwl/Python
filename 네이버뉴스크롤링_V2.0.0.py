import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
#import datetime
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta

es = Elasticsearch('http://127.0.0.1:9200')


search=['주토피아','AWS','엘라스틱','안경','몽타','라라랜드']

news_num = int(input('총 필요한 뉴스기사 수를 입력해주세요.(한 페이지 당 뉴스 10개 검색, 2선택시 20개 뉴스기사, 숫자만 검색) : '))

now = datetime.now()
nowDatetime = now.strftime('%Y.%m.%d.%H.%M')
nowDate = now.strftime('%Y.%m.%d')



beforeDatetime = now - timedelta(days=1)
beforeDatetime = beforeDatetime.strftime('%Y.%m.%d.%H.%M')

title_list = []
url_list = []
comp_list = []
thumbnail_list = []
text_list = []
day_list = []
keyword_list =[]

# 출력값을 리스트에 넣어주기 위해서 빈 리스크를 만들어준다.


for j in range(0,len(search)) :        # 검색어로 넣을 키워드를 반복한다.
    
    response1 = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query='+ search[j]
    response2= '&sort=0&photo=0&field=0&pd=4&ds=' + nowDatetime + '&de=' + beforeDatetime + '&cluster_rank=27&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:1d,a:all&start='
    # 필요한 url을 세팅해둔다.
    
    postNum = 1 # 뉴스 기사 수
    
    for i in range(news_num): # 뉴스 기사 수 
        response = requests.get(response1+response2+str(postNum))

        html = response.text

        soup = BeautifulSoup(html, 'html.parser')

        articles = soup.select('#main_pack > section > div > div.group_news > ul > li')

        postNum = postNum+10 # 뉴스 기사 수
        

        for article in articles:
            a_tag1 = article.select_one('.news_tit')
            
            title = a_tag1.text
            title_list.append(title.strip())
            #title_list.append(str(title)) 이 코드로도 가능하다.

            url = a_tag1['href']
            url_list.append(url.strip())

            comp = article.select_one('a.info.press').text
            comp = comp.replace('언론사 선정', '')
            comp_list.append(comp.strip())

            try:
                thumbnail = article.select_one('div > a > img')['src']
                thumbnail_list.append(thumbnail.strip())

            except:
                thumbnail_list.append('https://search.pstatic.net/common/?src=https%3A%2F%2Fimgnews.pstatic.net%2Fimage%2Forigin%2F366%2F2021%2F09%2F23%2F762207.jpg&type=ff264_180&expire=2&refresh=true')
            # 일부 기사는 이미지가 없는 경우가 있다. 따라서 이미지가 없는 경우 기본값을 설정해주었다.

            text = article.select_one('a.api_txt_lines.dsc_txt_wrap').text
            text_list.append(text.strip())

            day_list.append(nowDate)
            
            keyword_list.append(search[j])
info = {'제목':title_list, 'url':url_list, '언론사':comp_list, '썸네일':thumbnail_list, '내용':text_list, '수집 날짜':day_list, '키워드':keyword_list}
#print(info)
#news = pd.DataFrame(info)
#news = news.to_json("exmple.json", orient='table')
#print(news)

print(info['제목'])
index_name = 'newstest1'
for i in range(0,len(info['제목'])):
    es.index(index=index_name, doc_type='string', body={'제목':info['제목'][i],'url':info['url'][i], '언론사':info['언론사'][i], '썸네일':info['썸네일'][i], '내용':info['내용'][i], '수집 날짜':info['수집 날짜'][i], '키워드':info['키워드'][i]})


#index_name = 'newstest'
#es.index(index=index_name, doc_type='string', body=info)

#index_name = 'goods'

#doc1 = {'goods_name': '삼성 노트북 9',    'price': 1000000}
#for 
#es.index(index=index_name, doc_type='string', body=doc1)