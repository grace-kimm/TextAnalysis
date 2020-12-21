# -*- coding: utf-8 -*-
# 중간고사_김은혜.py

import requests
import time
import re
import urllib3
from bs4 import BeautifulSoup
from selenium import webdriver

# 웹 브라우저 별도로 생김
driver = webdriver.Chrome(
    executable_path=r'C:\chromedriver_win32\chromedriver.exe')

# 메인 페이지 입력
url = 'http://www.yes24.com/main/default.aspx'

# 별도 웹페이지가 여기로 이동
driver.get(url)

# '베스트' 탭 클릭해야 함

# element의 경로를 find_element_by_xpath() 이용해서 찾기
element1 = driver.find_element_by_xpath(
    '//*[@id="yesFixCorner"]/dl/dd/ul[1]/li[1]/a')
time.sleep(3)
# 별도 웹페이지가 '베스트' 탭으로 이동
element1.click()

# 베스트셀러 탭에서 책 정보 가져올 준비하기
url2 = 'http://www.yes24.com/24/category/bestseller'
html = requests.get(url2).text
soup = BeautifulSoup(html, 'html.parser')
books = soup.select('ol > li')
print(len(books))

# 순위와 상세링크에 이용할 urㅣ 선언하기
rank = 0
url3 = 'http://www.yes24.com'

# 체크박스 팝업 끄기
checkbox = driver.find_element_by_id("chk_info")
time.sleep(3)
checkbox.click()


# 예외처리 필요
for book in books:
    # 순위 부여
    rank = rank+1
    if rank == 11:
        break
    else:
        # 제목
        title = book.select('p > a')[2].text.strip()
        info = book.select('p.aupu')[0].text.strip()
        author1 = info.split(' | ')[0].strip()
        # 원저, 글, 편의 경우 '저'로 바꿔서 '저' 앞까지만 보여줄 것
        author2 = re.sub(r'(원저|글|편)', '저', author1)
        # 작가명 (저 앞까지 표시)
        author3 = author2.split('저')[0].strip()
        # 출판사
        company = info.split(' | ')[1].strip()
        # 판매가
        price = book.select('p.price > strong')[0].text

        # 출간일, 판매가를 뽑기 위해 상세 페이지로 이동
        detail = book.select('p > a')[0]
        detail_link = detail.get('href')

        detail_url = url3 + detail_link
        html_detail = requests.get(detail_url).text
        soup_detail = BeautifulSoup(html_detail, 'html.parser')

        # 출간일
        date = soup_detail.select(
            '#yDetailTopWrap > div.topColRgt > div.gd_infoTop > span.gd_pubArea > span.gd_date')[0].text.strip()

        detail2 = driver.find_element_by_xpath(
            '//*[@id="bestList"]/ol/li['+str(rank)+']/p[3]/a')
        driver.implicitly_wait(10)
        detail2.click()

        driver.implicitly_wait(10)

        try:

            # 회원 리뷰 이동 클릭
            review = driver.find_element_by_xpath(
                '//*[@id="yDetailTopWrap"]/div[2]/div[1]/span[3]/span[2]/a/em')
            time.sleep(3)
            review.click()

            time.sleep(3)

            # 리뷰 더보기 클릭
            review_click = driver.find_element_by_xpath(
                '//*[@id="infoset_reviewContentList"]/div[2]/div[2]/a/div')
            review_click.click()

            time.sleep(3)

            # html 소스코드 뽑기
            html2 = driver.page_source
            soup2 = BeautifulSoup(html2, 'html.parser')

            # 1번째 리뷰 뽑기
            review2 = soup2.find_all('div', class_='review_cont')[1]

            # 1번째 리뷰의 1번째 줄 뽑기
            review3 = review2.get_text(separator='|', strip=True).split('|')[0]

            # 제목, 저자, 출판사, 판매가 뽑기
            result = str(rank) + '. ' + '제목: ' + title + ', 저자: ' + author3 + \
                ', 출판사: ' + company + ', 판매가: ' + price + ', 출간일: ' + date
            print(result)
            # 회원리뷰의 첫줄 뽑기
            review_result = '회원리뷰: ' + review3 + '\n'
            print(review_result)

        # 리뷰가 없을 경우 예외 처리
        except Exception:
            # 제목, 저자, 출판사, 판매가 뽑기
            result = str(rank) + '. ' + '제목: ' + title + ', 저자: ' + author3 + \
                ', 출판사: ' + company + ', 판매가: ' + price + ', 출간일: ' + date
            print(result)
            # 리뷰가 없을 경우 '리뷰가 없습니다' 안내문구 보여주기
            review_result_none = '회원리뷰: 리뷰가 없습니다. \n'
            print(review_result_none)

            # 기다렸다가 '뒤로' 버튼으로 이동하기 (베스트셀러 페이지로 다시 가기)
            time.sleep(3)
            driver.back()
            time.sleep(3)
            continue

        # 기다렸다가 '뒤로' 버튼으로 이동하기 (베스트셀러 페이지로 다시 가기)
        time.sleep(3)
        driver.back()
        time.sleep(3)

# 끝났으면 드라이버 종료하기
driver.close()
