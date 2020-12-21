# -*- coding: utf-8 -*-
# assign04_김은혜.py

import requests
import time
import re
import urllib3
from bs4 import BeautifulSoup
from selenium import webdriver

# 웹 브라우저 별도로 생김
driver = webdriver.Chrome(
    executable_path=r'C:\chromedriver_win32\chromedriver.exe')

# 해당 페이지 입력
url = 'http://www.yes24.com/Product/Goods/78145872'

# 별도 웹페이지가 여기로 이동
driver.get(url)

# 판매지수 구하기
html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')
point = soup.select('#yDetailTopWrap > div.topColRgt > div.gd_infoTop > span.gd_ratingArea > span.gd_sellNum')[
    0].text.split()[2]

# 체크박스 팝업 끄기
checkbox = driver.find_element_by_id("chk_info")
checkbox.click()

# 건강 취미 부문의 순위 구하기
element1 = driver.find_element_by_xpath(
    '//*[@id="yDetailTopWrap"]/div[2]/div[1]/span[3]/span[4]/dl/dd/a')
time.sleep(3)

print('판매지수: ' + point + ', 베스트셀러 건강 취미: ' + element1.text.split()[2])

# 리뷰 총 개수, 총 페이지 수 구하기 (반복 횟수를 정하기 위해)

element2 = driver.find_element_by_xpath(
    '//*[@id="yDetailTopWrap"]/div[2]/div[1]/span[3]/span[2]/a/em')
element2.click()

total_review = soup.select(
    '#infoset_reviewTop > div.review_starWrap > p > em')[0].text
total_review = int(total_review)

if total_review % 5 == 0:
    total_page = int(total_review / 5)
else:
    total_page = int((total_review / 5) + 1)

# 각 페이지 마다 '뇌' 단어가 있으면 pass, 없으면 제목 보여주기

for i in range(total_page):
    front_url = 'http://www.yes24.com/Product/communityModules/GoodsReviewList/78145872?PageNumber='
    page_num = str(i+1)
    review_url = front_url + page_num

    review_detail = requests.get(review_url).text
    soup_detail = BeautifulSoup(review_detail, 'html.parser')
    review_all = soup_detail.find_all('span', class_='review_tit')
    for review in review_all:
        review_text = review.get_text().strip()
        if '뇌' in review_text:
            continue
        else:
            print(review_text)

# 마쳤으면 종료하기
driver.close()
