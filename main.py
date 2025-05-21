import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

option = webdriver.ChromeOptions()
option.add_argument(r"user-data-dir=C:\Users\FENGBICHUAN\AppData\Local\Google\Chrome\User_Data_back")
option.add_argument("blink-settings=imagesEnabled=false")
driver = webdriver.Chrome(options=option)


print("开始!")
driver.get('https://show.bilibili.com/platform/detail.html?id=72320&from=pc_ticketlist')
def haveticket(driver):
    if driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/div[4]/ul[3]/li[2]/div/div[2]').text == '0':
        print('无票')
        return 0
    elif driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/div[4]/ul[3]/li[2]/div/div[2]').text != '0':
        print('正常进入买票系统')
        return 1
try:
    while haveticket(driver) == 0:
        driver.get('https://show.bilibili.com/platform/detail.html?id=72320&from=pc_ticketlist')
        time.sleep(0.3)


    driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[2]/div[4]/ul[1]/li[2]/div[1]').click()
    driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[2]/div[4]/ul[2]/li[2]/div').click()
    driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/div[4]/div[2]/div[1]/div').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[5]/div[2]').click()

finally:
    time.sleep(10)
    driver.close()

