#!/usr/bin/env python
# coding: utf-8

# In[1]:


def pizza_review_crawler(address, location):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import time
    from bs4 import BeautifulSoup
    from tqdm import trange
    driver = webdriver.Chrome('/Users/angieryu2202/Downloads/chromedriver')
    driver.implicitly_wait(3)
    driver.get('https://www.yogiyo.co.kr/mobile/#/')
    driver.find_element_by_xpath('//*[@id="search"]/div/form/input').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="search"]/div/form/input').clear()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="search"]/div/form/input').send_keys(str(address))
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="button_search_address"]/button[2]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="category"]/ul/li[6]/span').click()
                
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
    
    globals()[str(location)+"restaurant_list"]=[]
    restaurants = driver.find_elements_by_css_selector('#content > div > div.restaurant-list > div.col-sm-6.contract')
    for restaurant in restaurants:
        globals()[str(location)+"restaurant_list"].append(restaurant.find_element_by_css_selector('div > table > tbody > tr > td:nth-child(2) > div > div.restaurant-name.ng-binding').text)
    pizza_store_names = ['피자헛', '도미노피자', '미스터피자', '파파존스', '피자헤븐']

    globals()[str(location)+"restaurant_list"] = [s for s in globals()[str(location)+"restaurant_list"] if any(xs in s for xs in pizza_store_names)]
    globals()[str(location)+"restaurant_list"] = set(globals()[str(location)+"restaurant_list"])
    print(globals()[str(location)+"restaurant_list"])
    
    
    globals()[str(location) + "_years"] = []
    globals()[str(location) + "_reviews"] = []
    
    for name in globals()[str(location)+"restaurant_list"]:
        driver.find_element_by_xpath('//*[@id="category"]/ul/li[1]/a').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="category"]/ul/li[15]/form/div/input').send_keys(name)
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="category_search_button"]').click()
        time.sleep(2)
        try:
            driver.find_element_by_xpath('//*[@id="content"]/div/div[4]/div[2]/div').click()
            time.sleep(2)
            print('리뷰 페이지 로드중...')
            driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a').click()
            time.sleep(2)
            driver.find_element_by_css_selector('ul#review a > span').click()
            time.sleep(2)
            review_count = int(driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a/span').text)
            click_count = int((review_count/10))
            print('모든 리뷰 불러오기 시작...')
            for _ in trange(click_count):
                try:
                    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                    driver.find_element_by_css_selector('ul#review a > span').click()
                    time.sleep(2)
                except Exception as e:
                    pass
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            print('모든 리뷰 불러오기 완료!')
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')

            # review collection
            globals()[str(name).replace(" ","") + "_reviews"] = []
            globals()[str(name).replace(" ","") + "_review_selectors"] = soup.find_all('li', class_='list-group-item star-point ng-scope')
            for globals()[str(name).replace(" ","")+ "_review_selector"] in globals()[str(name).replace(" ","") + "_review_selectors"]:
                globals()[str(name).replace(" ","") + "_review"] = globals()[str(name).replace(" ","") + "_review_selector"].find('p', class_='ng-binding').get_text()
                globals()[str(name).replace(" ","") + "_review"] = globals()[str(name).replace(" ","") + "_review"].strip()
                globals()[str(name).replace(" ","") + "_reviews"].append(globals()[str(name).replace(" ","") + "_review"])
            for item in globals()[str(name).replace(" ","") + "_reviews"]:
                globals()[str(location) + "_reviews"].append(item)
            print(globals()[str(name).replace(" ","") + "_reviews"])

            # date collection
            globals()[str(name).replace(" ","") + "_years"] = []
            globals()[str(name).replace(" ","") + "_year_selectors"] = soup.find_all('li', class_='list-group-item star-point ng-scope')
            for globals()[str(name).replace(" ","") + "_year_selector"] in globals()[str(name).replace(" ","") + "_year_selectors"]:
                globals()[str(name).replace(" ","") + "_year"] = globals()[str(name).replace(" ","") + "_year_selector"].find('span', class_='review-time ng-binding').get_text()
                globals()[str(name).replace(" ","") + "_year"] = globals()[str(name).replace(" ","") + "_year"].strip()
                globals()[str(name).replace(" ","") + "_years"].append(globals()[str(name).replace(" ","") + "_year"])
            for item in globals()[str(name).replace(" ","") + "_years"]:
                globals()[str(location) + "_years"].append(item)
        except:
            pass
            print('페이지 돌아가기중...')
            driver.execute_script("window.history.go(-1)")
            time.sleep(5)
    print("Finished: " + str(location))
    print(str(location) + "리뷰 수: " + str(len(globals()[str(location) + "_reviews"])))
    print(str(location) + "리뷰 날짜 수: " + str(len(globals()[str(location) + "_years"])))


# In[16]:


address_dict = {"대치본점" : "서울 강남구 삼성로 301",
                "평촌학원가점" : "경기 안양시 동안구 평촌대로 131",
                "홍성점" : "충남 홍성군 홍성읍 아문길29번길 67", 
                "진주경상대점":"경상남도 진주시 가좌동 868-33",
                "홍대상수점":"서울 마포구 독막로19길 32",
                "부산동아대점":"부산 서구 구덕로 220",
                "숭실대점":"서울 동작구 상도로 362-1",
                "일산라페스타점": "경기 고양시 일산동구 중앙로1275번길 38-5",
                "화성병점점": "경기 화성시 효행로 1060",
                "인천구월nc점": "인천 남동구 인하로 485 뉴코아아울렛",
                "일산후곡점": "경기 고양시 일산서구 일산로 547",
                "노량진점": "서울 동작구 노량진로16길 22-1",
                "수지구청점": "경기 용인시 수지구 풍덕천로 135",
                "상현역점": "경기 용인시 수지구 광교중앙로 305",
                "성남수진역점": "경기 성남시 중원구 원터로 116",
                "수원행궁동점": "경기 수원시 팔달구 정조로892번길 4",
                "부산광복점": "부산 중구 광복로97번안길 8-1",
                "고양어린이박물관점": "경기도 고양시 덕양구 화정동 1003 고양시 어린이 박물관",
                "마이크임펙트스튜디오점": "서울 강남구 역삼로 180"}
address_dict1 = {"대치본점" : "서울 강남구 삼성로 301",
                "평촌학원가점" : "경기 안양시 동안구 평촌대로 131",
                "홍성점" : "충남 홍성군 홍성읍 아문길29번길 67", 
                "진주경상대점":"경상남도 진주시 가좌동 868-33"}
address_dict2 = {"홍대상수점":"서울 마포구 독막로19길 32",
                "부산동아대점":"부산 서구 구덕로 220",
                "숭실대점":"서울 동작구 상도로 362-1"}
address_dict3 = {"일산라페스타점": "경기 고양시 일산동구 중앙로1275번길 38-5",
                 "화성병점점": "경기 화성시 효행로 1060"}
address_dict4 = {"인천구월nc점": "인천 남동구 인하로 485 뉴코아아울렛",
                "일산후곡점": "경기 고양시 일산서구 일산로 547"}
address_dict5 = {"노량진점": "서울 동작구 노량진로16길 22-1",
                 "수지구청점": "경기 용인시 수지구 풍덕천로 135"}
address_dict6 = {"상현역점": "경기 용인시 수지구 광교중앙로 305",
                "수원행궁동점": "경기 수원시 팔달구 정조로892번길 4"}
address_dict7 = {"성남수진역점": "경기 성남시 중원구 원터로 116",
                "부산광복점": "부산 중구 광복로97번안길 8-1"}
address_dict8 = {"고양어린이박물관점": "경기도 고양시 덕양구 화정동 1003 고양시 어린이 박물관",
                "마이크임펙트스튜디오점": "서울 강남구 역삼로 180"}


# In[3]:


for k,v in address_dict1.items():
    pizza_review_crawler(v, k)


# In[4]:


for k,v in address_dict2.items():
    pizza_review_crawler(v, k)


# In[8]:


for k,v in address_dict3.items():
    pizza_review_crawler(v, k)


# In[10]:


for k,v in address_dict4.items():
    pizza_review_crawler(v, k)


# In[13]:


for k,v in address_dict5.items():
    pizza_review_crawler(v, k)


# In[17]:


for k,v in address_dict6.items():
    pizza_review_crawler(v, k)


# In[18]:


for k,v in address_dict7.items():
    pizza_review_crawler(v, k)


# In[19]:


for k,v in address_dict8.items():
    pizza_review_crawler(v, k)


# In[184]:


papajohns = ['파파존스-대치점', '파파존스-평촌점', '파파존스-홍대점',
             '파파존스-상도점','파파존스-인천구월점', '파파존스-정발산점', '파파존스-상도점',
            '파파존스-수지점', '파파존스-야탑점', '파파존스-대신점', '파파존스-역삼점']
pizzahut = ['피자헛-홍대서교점', '피자헛-상도역점', '피자헛-일산킨텍스점', '피자헛-일산킨텍스점',
            '피자헛-상도역점', '피자헛-용인수지2점', '피자헛-신봉점',
            '피자헛-성남종합운동장점', '피자헛-동수원점','피자헛-부산보수점',
            '피자헛-화정역점']
pizzaheaven = ['김준현의피자헤븐-상도점','김준현의피자헤븐-화성동탄점', '김준현의피자헤븐-역삼점']
dominos = ['도미노피자-평촌점', '도미노피자-홍성점', '도미노피자-진주경상대점', '도미노피자-장항점',
          '도미노피자-병점점', '도미노피자-후곡점', '도미노피자-중앙대점', '도미노피자-화정점', '도미노피자-역삼점']
misterpizza = ['미스터피자-망원점', '미스터피자-라페스타장항점', '미스터피자-병점점', '미스터피자-주안역점',
              '미스터피자-풍동점', '미스터피자-노량진점', '미스터피자Single메뉴-수지점',
              '미스터피자-상현점', '미스터피자-북수원점', '미스터피자-화정점']


# In[185]:


def store_review_organizer(store_name, store_list):
    globals()[str(store_name)+"_reviews"] = []
    globals()[str(store_name)+"_years"] = []
    for name in store_list:
        for review in globals()[str(name)+"_reviews"]:
            globals()[str(store_name)+"_reviews"].append(review)
        for year in globals()[str(name)+"_years"]:
            globals()[str(store_name)+"_years"].append(year)
    print(len(globals()[str(store_name)+"_reviews"]))


# In[186]:


store_review_organizer('papajohns', papajohns)
store_review_organizer('pizzahut', pizzahut)
store_review_organizer('pizzaheaven', pizzaheaven)
store_review_organizer('dominos', dominos)
store_review_organizer('misterpizza', misterpizza)


# In[187]:


# Making dataframe for date and review content for 고피자 대치본점
def pizza_df_maker(store_name):
    import pandas as pd
    globals()[str(store_name) +"_tuple"] =  list(zip(globals()[str(store_name) +"_years"], globals()[str(store_name) +"_reviews"]))
    globals()[str(store_name) + "_df"] = pd.DataFrame(globals()[str(store_name) +"_tuple"], columns = ['date' , 'content'])
    #globals()[str(location) + "_df"].head()
    globals()[str(store_name) + "_df"]['location'] = str(store_name)
    #globals()[str(location) + "_df"]['date'] = globals()[str(location) + "_df"]['date'].replace("","")
    print(str(store_name) + "_df" + " finished")
    
store_name_list = ['papajohns', 'pizzahut', 'pizzaheaven', 'dominos', 'misterpizza']
for store_name in store_name_list:
    pizza_df_maker(store_name)


# In[188]:


# Concatenating the two dataframes for gopizza reviews
import pandas as pd
pizza_frames = [papajohns_df, pizzahut_df, pizzaheaven_df, dominos_df, misterpizza_df]
pizza_df = pd.concat(pizza_frames)
pizza_df.head()


# In[189]:


# Remove \n and | from review content
pizza_df = pizza_df.replace(r'\n',' ', regex=True).replace(r'|', '', regex=True)
pizza_df.head()


# In[190]:


# Save dataframe to tsv file without the index
pizza_df.to_csv('/Users/angieryu2202/Desktop/gopizza/전체피자요기요리뷰.tsv', sep = '\t', index = False)
print("요기요에서 크롤링한 총 피자 리뷰 수: " + str(len(pizza_df)))

