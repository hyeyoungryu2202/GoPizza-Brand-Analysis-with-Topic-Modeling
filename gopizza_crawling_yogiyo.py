#!/usr/bin/env python
# coding: utf-8

# In[10]:


def pizza_site_crawler(location):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import time
    driver = webdriver.Chrome('/Users/angieryu2202/Downloads/chromedriver')
    driver.implicitly_wait(3)
    driver.get('http://www.bdtong.co.kr/')
    driver.find_element_by_xpath('//*[@id="header"]/div[4]/div/ul/li[3]/a').click()
    driver.find_element_by_xpath('//*[@id="address_box"]/span/div').click()
    driver.find_element_by_xpath('//*[@id="posCurrent"]').send_keys("서울특별시 " + str(location))
    driver.find_element_by_xpath('//*[@id="posCurrent"]').send_keys(Keys.RETURN)
    driver.find_element_by_xpath('//*[@id="addr_list"]/li').click()
    # 창의 끝까지 scroll down
    SCROLL_PAUSE_TIME = 0.5


    while True:

        # Get scroll height
        ### This is the difference. Moving this *inside* the loop
        ### means that it checks if scrollTo is still scrolling 
        last_height = driver.execute_script("return document.body.scrollHeight")

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:

            # try again (can be removed)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")

            # check if the page height has remained the same
            if new_height == last_height:
                # if so, you are done
                break
            # if not, move on to the next loop
            else:
                last_height = new_height
                continue
            
    globals()[str(location).replace(" ","")+"_element"] = driver.find_element_by_xpath('//*[@id="store_list"]')
    globals()[str(location).replace(" ","")+"_hrefs"] = [x.get_attribute('href') for x in globals()[str(location).replace(" ","")+"_element"].find_elements_by_css_selector('a')]
    globals()[str(location).replace(" ","")+"_stripped_hrefs"] = []
    for globals()[str(location).replace(" ","")+"_href"] in globals()[str(location).replace(" ","")+"_hrefs"]:
        globals()[str(location).replace(" ","")+"_stripped_hrefs"].append(globals()[str(location).replace(" ","")+"_href"][42:-20])
    print(str(location).replace(" ","") + ' end')


# In[11]:


# 관악구, 마포구, 서대문구
locations = ['관악구 보라매동', '관악구 은천동', '관악구 성현동', '관악구 중앙동', '관악구 청림동', '관악구 행운동', '관악구 청룡동', '관악구 낙성대동', '관악구 인헌동', '관악구 남현동', '관악구 신림동', '관악구 신사동', '관악구 조원동', '관악구 미성동', '관악구 난곡동', '관악구 난향동', '관악구 서원동', '관악구 신원동', '관악구 서림동', '관악구 삼성동', '관악구 대학동',
            '마포구 공덕동', '마포구 아현동', '마포구 도화동', '마포구 용강동', '마포구 대흥동', '마포구 염리동', '마포구 신수동', '마포구 서강동', '마포구 서교동', '마포구 합정동', '마포구 망원1동', '마포구 망원2동', '마포구 연남동', '마포구 성산1동', '마포구 성산2동', '마포구 상암동',
            '서대문구 충현동', '서대문구 천연동', '서대문구 북아현동', '서대문구 신촌동', '서대문구 신촌동', '서대문구 연희동', '서대문구 홍제1동', '서대문구 홍제2동', '서대문구 홍제3동', '서대문구 홍은1동', '서대문구 홍은2동', '서대문구 남가좌1동', '서대문구 남가좌2동', '서대문구 북가좌1동', '서대문구 북가좌2동']


# In[13]:


for location in locations:
    pizza_site_crawler(location)


# In[103]:


def pizza_review_crawler (url):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import time
    from bs4 import BeautifulSoup
    
    driver = webdriver.Chrome('/Users/angieryu2202/Downloads/chromedriver')
    driver.get(str(url))
    location = driver.find_element(By.XPATH,'//*[@id="subContents"]/div/div[1]/div[3]/div[2]/div/div[2]/div[1]/div[2]/div/dl[1]/dd').text
    print(location)
    
    driver.find_element_by_xpath('//*[@id="subContents"]/div/div[1]/div[3]/div[1]/div[1]/ul/li[2]/a').click()

    SCROLL_PAUSE_TIME = 0.5

    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:

            # try again (can be removed)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")

            # check if the page height has remained the same
            if new_height == last_height:
                # if so, you are done
                break
            # if not, move on to the next loop
            else:
                last_height = new_height
                continue

    page_source1 = driver.page_source
    soup1 = BeautifulSoup(page_source1, 'lxml')
    #store = str(soup1.find('div', class_='detlow dlow1').get_text())
    globals()[str(location).replace(" ","")+"_reviews"] = []
    globals()[str(location).replace(" ","")+"_review_selectors"] = soup1.find_all('div', class_='textzone')
    for globals()[str(location).replace(" ","")+"_review_selector"] in globals()[str(location).replace(" ","")+"_review_selectors"]:
        globals()[str(location).replace(" ","")+"_review"] = globals()[str(location).replace(" ","")+"_review_selector"].find('div', class_='textz').find('p').get_text()
        globals()[str(location).replace(" ","")+"_review"] = globals()[str(location).replace(" ","")+"_review"].strip()
        globals()[str(location).replace(" ","")+"_reviews"].append(globals()[str(location).replace(" ","")+"_review"])
    print("Finished: " + str(url))


# In[104]:


pizza_review_crawler('http://www.bdtong.co.kr/%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C-%EA%B4%80%EC%95%85%EA%B5%AC-%EC%84%9C%EC%9B%90%EB%8F%99/%ED%94%BC%EC%9E%90/%EC%B0%A9%ED%95%9C%ED%94%BC%EC%9E%90/S0248437')


# In[105]:


착한피자신림점_reviews

