import requests
from bs4 import BeautifulSoup

indeed_result=requests.get("https://www.indeed.com/jobs?q=python&limit=50")
#print(indeed_result)
## 결과값 <Response [200]> 은 잘 가져왔다는 것이다.

#print(indeed_result.text)
## HTML꼴로 결과값을 가져온다

indeed_soup = BeautifulSoup(indeed_result.text, "html.parser")

#print(indeed_soup)
## HTML꼴로 이쁘게 나온다.

pagination=indeed_soup.find("div",{"class":"pagination"})
#print(pagination)
## pagination이라는 class를 가진 div를 가져온다는 의미이다.

links=pagination.find_all('a')
pages=[]
#print(links)
## a는 ancher을 의미한다. 숫자정보는 a에 있었으므로 a를 찾는 것이다.

for link in links:
    pages.append(link.find("span").string)  #string만 가져온다.
#print(pages[:-1])
## 마지막 요소 전까지 저장. 결과값을 보면 숫자정보는 span에 있었으므로 span을 찾는다.
print(pages)
pages=pages[0:-1]
print(pages)

## 정수로 나타내주기. list는 int()가 먹지 않아서 다음과 같은 방법을 사용해야 된다.
page=[]
for link in links[:-1]:
    page.append(int(link.string))
print(page)
max_page=page[-1]
print(max_page)

for n in range(max_page):
    print(f"start={n*50}")
