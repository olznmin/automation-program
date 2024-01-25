# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time 
from selenium.webdriver.common.by import By
import json
# 크롬 드라이버 자동 업데이트을 위한 모듈
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import json 
import codecs
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# 불필요한 에러 메시지 삭제
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
# 크롬 드라이버 최신 버전 설정
service = Service(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)

#우회용 delay 
time.sleep(random.uniform(1,3))
# 웹페이지 해당 주소 이동
browser.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")

# 자동방지 우회 로그인 
input_js = ' \
        document.getElementById("id").value = "{id}"; \
        document.getElementById("pw").value = "{pw}"; \
    '.format(id = "dkjayden", pw = "a796796796")
time.sleep(random.uniform(1,3)) # 자동화탐지를 우회 하기 위한 delay
browser.execute_script(input_js)
time.sleep(random.uniform(1,3)) # 자동화탐지를 우회 하기 위한 delay
browser.find_element(By.ID,"log.login").click()

# 터미널에서 URL 입력 받기
# url = input("웹 페이지 URL을 입력하세요: ")

#Json 파일 불러오는 코드 
filename = input("입력하고 싶은 파일명을 입력하세요 : ")
with open(filename+'.json','r',encoding='utf-8')as f:
    data = json.load(f)

#url 저장 
url = data[0].get('Product_URL')

# 웹페이지 해당 주소 이동
browser.get(url)

try:
    element = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'._1SHgFqYghw._1NXyF7xfLC')))
    print ('ERROR: 도착보장 상품은 구매할 수 없습니다.')
    browser.close()
except:
    # 'optionName'의 값을 'optionname'에 저장
    optionnames = {}
    option = data[0].get('option') if len(data) > 0 else None
    if not isinstance(option, list):
        option = [{}]
        
    if option and option[0]:
        for i in range(1, 11):
            key = 'optionName' + str(i)
            if key in option[0]:
                optionnames[key] = option[0][key]

    # 단일상품일경우 코드 
    if optionnames.get('optionName1') == None :
        count = input('주문하고싶은 상품의 수량을 입력하세요')
        
        try:
            element = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.bd_EZ05h.bd_2nJMW.N\\=a\\:pcs\\.quantity')))
            
            if element is not None:
                element_text = browser.find_element(By.CSS_SELECTOR, '.bd_2eiJL.N\\=a\\:pcs\\.quantity').text
                value = 0  # value를 0으로 초기화합니다.
                if element_text:
                    value = int(element_text)
                else:
                    print("단일 상품의 제품을 선택합니다.")

            count = int(count)
            while value < count:
                element.click()
                value = int(browser.find_element(By.CSS_SELECTOR, '.bd_2eiJL.N\\=a\\:pcs\\.quantity').get_attribute('value'))  
                
                print ('상품 개수를 맞게 선택하였습니다. ')

        except TimeoutException:
            print('요소를 찾지못했습니다')    


    # 옵션상품 코드 
            
    #첫번째 옵션 선택 코드 
    if 'optionName1' in optionnames:
        try:
            try:
                element = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.bd_1fhc9.N\\=a\\:itm\\.opopen')))
            except:
                element = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.bd_1fhc9.N\\=a\\:pcs\\.opopen')))
            element.click()

            try:
                ul_element = browser.find_element(By.CLASS_NAME,'bd_zxkRR')
            except:
                print("Error: 1번")
                
            tags = ul_element.find_elements(By.XPATH,'./li')
            for tag in tags:
                # print(tag.text)
                if tag.text == optionnames.get('optionName1'):
                    print("첫번째 옵션인" +tag.text+ "을 성공적으로 클릭했습니다!")
                    tag.click()
                    break

        except TimeoutException:
            print ("ERROR: 2번 ")

    # 두 번째 옵션 선택
    if 'optionName2' in optionnames:
        try:
            elements = WebDriverWait(browser, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.bd_1fhc9.N\\=a\\:pcs\\.opopen')))
            element = elements[1]  # 두 번째 요소 선택
            element.click()

            ul_element = browser.find_element(By.CLASS_NAME,'bd_zxkRR')

            tags = ul_element.find_elements(By.XPATH,'./li')
            for tag in tags:
                if tag.text == optionnames.get('optionName2'):
                    print("두번째 옵션인"+ tag.text + "을 성공적으로 클릭했습니다.")
                    tag.click()
                    break
        except TimeoutException:
            print('Error: 3번')

    #장바구니 버튼 클릭 
    try:
        element = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div[2]/div[2]/fieldset/div[8]/div[2]/div[3]/a')))
        element.click()
        element.send_keys(Keys.RETURN)
        print("구매하기버튼 웹 요소를 성공적으로 클릭하고 엔터키를 눌렀습니다.")
    except TimeoutException:
        try:
            element = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div[2]/div[2]/fieldset/div[9]/div[2]/div[3]/a')))
            element.click()
            element.send_keys(Keys.RETURN)
            print("구매하기버튼 웹 요소를 성공적으로 클릭하고 엔터키를 눌렀습니다.")
        except TimeoutException:
            try:
                element = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[3]/div[2]/fieldset/div[9]/div[2]/div[3]/a')))
                element.click()
                element.send_keys(Keys.RETURN)
                print("구매하기버튼 웹 요소를 성공적으로 클릭하고 엔터키를 눌렀습니다.")
            except TimeoutException:
                try:
                    element = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[3]/div[2]/fieldset/div[9]/div[2]/div[3]/a')))
                    element.click()
                    element.send_keys(Keys.RETURN)
                    print("구매하기버튼 웹 요소를 성공적으로 클릭하고 엔터키를 눌렀습니다.")
                except TimeoutException:
                    print("구매하기버튼 웹 요소를 찾는 데 실패했습니다. XPath를 확인하거나 대기 시간을 조정해보세요.")

    #장바구니창 alert 진입 코드 
    time.sleep(1)
    try:
        alert = browser.switch_to.alert  # alert 창으로 포커스를 전환합니다.
        alert.accept()  # alert 창의 확인 버튼을 누릅니다.
    except :
        print("No alert present.")

    #총 주문하기 버튼 클릭 
    try:
        element = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="app"]/div/div[9]/div/div[2]/button[2]')))
        element.click()
        element.send_keys(Keys.RETURN)
    except:
        element = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="app"]/div/div[10]/div/div[2]/button[2]')))
        element.click()
        element.send_keys(Keys.RETURN)
    print('총 주문하기 버튼을 늘렀습니다.')

    # time.sleep(7)
    # browser.close()