from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import pandas as pd

selector= By.CSS_SELECTOR
driver=webdriver.Chrome()   # driver.

# 양곡도서관 홈페이지 크롤링
url= "https://www.gimpo.go.kr/yanggok/selectBbsNttList.do?key=2926&bbsNo=315&integrDeptCode=&searchKrwd=&searchCtgry=%EC%96%91%EA%B3%A1%EB%8F%84%EC%84%9C%EA%B4%80"
driver.get(url)
driver.implicitly_wait(2)


name_list = []
release_list = []
author_list = []
company_list = []
img_list = []
content_list = []
book_data = []

# 책 제목 a태그 눌러서
# 책 정보 추출하는 함수
def get_books() :

    a_list = len(driver.find_elements(selector, "#contents > div > div > div.book_search_content > div.book_search_list > div.list_box > .info_area > .book_nm > a"))
    for index in range(a_list) :
        book_img = driver.find_elements(selector,"div.book_img_area > label > img")[index].get_attribute("src")
        a = driver.find_elements(selector,"#contents > div > div > div.book_search_content > div.book_search_list > div.list_box > .info_area > .book_nm > a")[index]
        a.click()
        time.sleep(2)
        book_name = driver.find_element(selector, "#contents > div > table > tbody > tr:nth-child(2) > td").text
        book_release = driver.find_element(selector, "#contents > div > table > tbody > tr:nth-child(3) > td").text
        book_author = driver.find_element(selector, "#contents > div > table > tbody > tr:nth-child(4) > td").text
        book_company = driver.find_element(selector, "#contents > div > table > tbody > tr:nth-child(5) > td").text
        book_content = driver.find_element(selector, "#contents > div > table > tbody > tr:nth-child(6) > td").text
        # print("도서명", book_name, "해당년월", book_release, "저자", book_author, "출판사", book_company)


        # pandas를 위해 빈배열에 각기 다른 데이터를 담기
        name_list.append(book_name)
        release_list.append(book_release)
        author_list.append(book_author)
        company_list.append(book_company)
        img_list.append(book_img)
        content_list.append(book_content)
        df = pd.DataFrame({
            # 'BOK_NO': 1,
            'BOK_NAME': name_list,
            'BOK_COM': company_list,
            'BOK_INT': content_list,
            'BOK_REN': "n",
            'BOK_AUTHOR': author_list,
            'BOK_RELEASE': release_list
        })

        book_data.append(df)
        # 목록 버튼
        list_btn = driver.find_element(selector, "#contents > div > div > div.col-12.col-sm-24.right > a")
        list_btn.click()
        time.sleep(2)



    return book_data


total_cnt = driver.find_element(selector,"#contents > div > div > div.row > div.col-12.col-sm-24.margin_t_10.small > em.em_black").text

books = get_books()
# print(books)

while len(books) < 330 :
    # books += get_books()
    if(len(books) % 100 == 0) :
        # 책이 100권 모였을 경우 다음 버튼 누르기 (페이지네이션이 10으로 고정되어있으므로)
        next_btn = driver.find_element(selector,"#contents > div > div > div.book_search_content > div.p-pagination > div > span:nth-child(3) > a.p-page__link.next")
        next_btn.click()
        time.sleep(2)
        books = get_books()

    # 페이지 버튼
    elif(len(books) % 10 == 0):
        btn_list = driver.find_elements(selector,"span.p-page__link-group > strong.active + a")
        for btn in btn_list :
            btn.click()
            time.sleep(2)
        books = get_books()

    else :
        books = get_books()
    # df


# df
books[len(books)-1]
books[len(books)-1].to_csv("bookList.csv")
