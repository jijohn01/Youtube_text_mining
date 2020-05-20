
from bs4 import BeautifulSoup
import time
import urllib.request #
from selenium.webdriver import Chrome
import re
from selenium.webdriver.common.keys import Keys
import pandas as pd

def delete_useless_chr_from_title(datalist):
    # 이모티콘 제거
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)

    # 분석에 어긋나는 불용어구 제외 (특수문자, 의성어)
    han = re.compile(r'[([\])!ㅣ?~,".\n\r#\ufeff\u200d]')
    no_need = re.compile(r'[([\])!ㅣ?~,"\n\r#\ufeff\u200d]')
    title_ls = []
    view_ls = []
    like_ls = []
    unlike_ls = []
    for i in range(len(datalist)):
        a = re.sub(emoji_pattern, '', datalist['title'].iloc[i])
        view = re.sub(no_need,'',datalist['view'].iloc[i])
        like = re.sub(no_need,'',datalist['like'].iloc[i])
        unlike = re.sub(no_need,'',datalist['unlike'].iloc[i])

        b = re.sub(han, '', a)

        title_ls.append(b)
        view_ls.append(view)
        like_ls.append(like)
        unlike_ls.append(unlike)

    datalist['title'] = title_ls
    datalist['view'] =view_ls
    datalist['like'] =like_ls
    datalist['unlike'] = unlike_ls

    return datalist

delay=3
browser = Chrome()
browser.implicitly_wait(delay)
start_url  = 'https://www.youtube.com'
browser.get(start_url)
time.sleep(2)
# browser.maximize_window()
browser.find_element_by_xpath('//*[@id="search-form"]/div/div/div/div[2]/input').click() #검색창영역클릭 커서를 올려야함
browser.find_element_by_xpath('//*[@id="search-form"]/div/div/div/div[2]/input').send_keys('딩고 채널')#검색창 영역에 원하는 youtuber입력
browser.find_element_by_xpath('//*[@id="search-form"]/div/div/div/div[2]/input').send_keys(Keys.RETURN)#엔터
time.sleep(2)

# browser.find_element_by_xpath('//*[@class="yt-simple-endpoint style-scope ytd-channel-renderer"]/div[2]/h3/span').click()


browser.find_element_by_partial_link_text('딩고').click()

browser.find_element_by_xpath('//*[@class="scrollable style-scope paper-tabs"]/paper-tab[2]').click()

body = browser.find_element_by_tag_name('body')  # 스크롤하기 위해 소스 추출
num_of_pagedowns = 90
# 25번 밑으로 내리는 것
while num_of_pagedowns:
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    num_of_pagedowns -= 1
time.sleep(2)

html0 = browser.page_source
html = BeautifulSoup(html0,'html.parser')
video_ls=html.find_all('ytd-grid-video-renderer',{'class':'style-scope ytd-grid-renderer'})
b = html.find('div',{'id':'items','class':'style-scope ytd-grid-renderer'})
len(b.find_all('ytd-grid-video-renderer',{'class':'style-scope ytd-grid-renderer'}))#450개의 영상정보를 수집

tester_url = []
for i in range(len(video_ls)):
    url = start_url+video_ls[i].find('a',{'id':'thumbnail'})['href']
    tester_url.append(url)
print(len(video_ls))
data_list =[['title','view','like','unlike','date']]

for idx,url in enumerate(tester_url):
    browser.get(url)
    time.sleep(2)
    soup0 = browser.page_source
    soup = BeautifulSoup(soup0,'html.parser',from_encoding='utf-8')

    info1 = soup.find('div',{'id':'info-contents'})
    #댓글을 막아놓은 영상이 있기 때문에 예외처리를 꼭해준다.
    try:
        comment = soup.find('yt-formatted-string',{'class':'count-text style-scope ytd-comments-header-renderer'}).text
    except:
        comment = '댓글x'
    try:
        title = info1.find('h1',{'class':'title style-scope ytd-video-primary-info-renderer'}).find('yt-formatted-string').text #영상제목
        # print(title)
        view =info1.find('yt-view-count-renderer',{'class':'style-scope ytd-video-primary-info-renderer'}).find('span').text #영상 조회수
        like = info1.find('div',{'id':'top-level-buttons'}).find_all('yt-formatted-string')[0].text #좋아요수
        # print(like)
        unlike = info1.find('div',{'id':'top-level-buttons'}).find_all('yt-formatted-string')[1].text #싫어요수
        # print(unlike)
        date = info1.find('div',{'id':'date'}).find('yt-formatted-string',{'class':'style-scope ytd-video-primary-info-renderer'}).text#영상업로드날짜
        # print(date)
        data_list.append([title,view,like,unlike,date])
        # print(data_list[-1])
    except:
        print("뭐지")

df=pd.DataFrame(data_list[1:],columns=data_list[0])
df = delete_useless_chr_from_title(df)
df.to_csv('./rawdata.csv',encoding='utf-8-sig')
print("End!!!")
browser.close()


