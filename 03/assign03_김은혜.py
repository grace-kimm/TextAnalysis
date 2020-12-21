# assign03_김은혜
# import requests, beautifulSoup
import requests
from bs4 import BeautifulSoup

# best seller url에서 베스트셀러 순위가 있는 부분 가져옴
url = 'http://www.yes24.com/24/category/bestseller'
html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')
books = soup.select('ol > li')

# rank 할당
rank = 0

# 출간일을 위해 세부 URL에 붙일 앞 URL 다시 설정
url2 = 'http://www.yes24.com'

# 파일 저장을 위해 open txt 파일
f = open('yes24_best_seller_results.txt', 'w', encoding='utf-8')

for book in books:
    try :
        # 순위
        rank = rank+1
        # 19, 20순위는 제외
        if rank in [19, 20]:
            continue

        else:
            # 책제목
            title = book.select('p > a')[2].text.strip()
            # 저자, 출판사를 가져올 info
            info = book.select('p.aupu')[0].text.strip()
            # 저자
            author = info.split(' | ')[0].strip()
            # 출판사
            company = info.split(' | ')[1].strip()

            # 출간일이 담겨 있는 상품의 세부 URL 찾기
            detail = book.select('p > a')[0]
            detail_link = detail.get('href')

            # 세부 URL에서 출간일을 찾을 것
            detail_url = url2 + detail_link
            html_detail = requests.get(detail_url).text
            soup_detail = BeautifulSoup(html_detail, 'html.parser')

            # 출간일
            date = soup_detail.select(
                '#yDetailTopWrap > div.topColRgt > div.gd_infoTop > span.gd_pubArea > span.gd_date')[0].text.strip()

            # 최종 결과
            result = str(rank) + '. ' + title + '; ' + author + '; ' + company + '; ' + date + '\n'
            print(result)

            # 최종 결과 저장
            f.write(result)

    # error handling : 우선 진행한다.
    except Exception as e :
        continue


# 작업이 끝났으면 txt 파일을 닫아준다.
f.close()

