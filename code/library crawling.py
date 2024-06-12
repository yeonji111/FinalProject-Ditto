from selenium import webdriver
import time
from selenium.webdriver.common.by import By


selector= By.CSS_SELECTOR
driver=webdriver.Chrome()   # driver.

# 양곡도서관 홈페이지 크롤링
url= "https://www.gimpo.go.kr/yanggok/selectBbsNttList.do?bbsNo=315&key=2926&searchCtgry=%EC%96%91%EA%B3%A1%EB%8F%84%EC%84%9C%EA%B4%80"
driver.get(url)
driver.implicitly_wait(2)



# 책 정보 추출
def get_books() :
    book_list = driver.find_elements(selector, "#contents > div > div > div.book_search_content > div.book_search_list > div.list_box")

    # 총 도서 개수
    books_cnt = driver.find_element(selector,".em_black").text
    # print("책 개수 : " ,books_cnt)
    book_data = []
    for book in book_list :
        book_img = book.find_element(selector, "img").get_attribute("src")
        book_name = book.find_element(selector, ".book_nm").text
        book_author = book.find_element(selector, ".clearfix > li:nth-child(1)").text
        book_company = book.find_element(selector, ".clearfix > li:nth-child(2)").text
        book_release = book.find_element(selector, ".clearfix > li:nth-child(3)").text
        book_data.append([book_img, book_name, book_author,book_company,book_release])
        # print(book_img, book_name, book_author,book_company,book_release)
        # print(book_data)
    return book_data


page = 1;
craw_books_cnt = page * 10
# 버튼 클릭 이벤트 관련

book = get_books()
# while len(book) < int(books_cnt) :
while len(book) < 101 :
    btn_list = driver.find_elements(selector,"span.p-page__link-group > strong.active + a")
    for btn in btn_list :
        btn.click()
        time.sleep(2)
        get_books()
        book += get_books()
        if len(book) % 100 == 0 :
            next_btn = driver.find_element(selector,"#contents > div > div > div.book_search_content > div.p-pagination > div > span:nth-child(3) > a.p-page__link.next")
            next_btn.click()
            time.sleep(2)
print(book)
print(len(book))

