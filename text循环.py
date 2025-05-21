import time
from selenium import webdriver
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import win32api, win32con, io
from PIL import ImageGrab
import threading

option = webdriver.ChromeOptions()
option.add_argument(r"user-data-dir=C:\Users\FENGBICHUAN\AppData\Local\Google\Chrome\User_Data_bc")
option.add_argument("blink-settings=imagesEnabled=false")
option.add_argument("--ignore-certificate-errors")  # 忽略证书错误
option.add_argument("--disable-popup-blocking")  # 禁用弹出拦截
option.add_argument("no-sandbox")  # 取消沙盒模式
option.add_argument("no-default-browser-check")  # 禁止默认浏览器检查
option.add_argument("about:histograms")
option.add_argument("about:cache")
option.add_argument("disable-extensions")  # 禁用扩展
option.add_argument("disable-glsl-translator")  # 禁用GLSL翻译
option.add_argument("disable-translate")  # 禁用翻译
option.add_argument("--disable-gpu")  # 谷歌文档提到需要加上这个属性来规避bug
option.add_argument("--disable-dev-shm-usage")
option.add_argument("--hide-scrollbars")  # 隐藏滚动条, 应对一些特殊页面
driver = webdriver.Chrome(options=option)
TO_USER = 'tracy'


# 检查页面元素，判定是否邮票
def haveticket(driver):
    e = driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[2]/div[4]/div[2]/div[1]/div')
    p = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/div[4]/ul[3]/li[2]/div/div[2]')
    print(e.text)
    if p.text == '1':
        # and e.text == '立即购票'
        return 1
    else:
        return 0


# 企业微信发消息
class WeChat():
    def __init__(self):
        self.CORP_ID = "wwd058c08979f0ee9d"
        self.SECRET = "6Bgu9p9xARkr-zX-l6goVd8FAUEfh9fU0_uqKOJzIFQ"
        self.AGENT_ID = 1000002
        self.token = self.get_token()

    def get_token(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        data = {
            "corpid": self.CORP_ID,
            "corpsecret": self.SECRET
        }
        req = requests.get(url=url, params=data)
        res = req.json()
        if res['errmsg'] == 'ok':
            return res["access_token"]
        else:
            return res

    def send(self, content):
        to_user = TO_USER
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % self.token
        data = {
            "touser": to_user,
            "msgtype": "text",
            "agentid": self.AGENT_ID,
            "text": {"content": content},
            "safe": "0"
        }
        req = requests.post(url=url, json=data)
        res = req.json()
        if res['errmsg'] == 'ok':
            print("已通过企业微信发送提醒")
            return "已通过企业微信发送提醒"
        else:
            return res


# 截图
def screenshot():
    time.sleep(0.5)
    width = 1920
    height = 1080
    img = ImageGrab.grab(bbox=(0, 0, width, height))
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format='JPEG')
    pic = imgByteArr.getvalue()
    open("%s.jpeg" % time.strftime("%Y-%m-%d %H.%M.%S", time.localtime()), "wb").write(pic)


cnt = 0
while True:
    try:
        print("开始!")
        driver.get('https://show.bilibili.com/platform/detail.html?id=72320&from=pc_ticketlist')
        while (cnt != 1):
            while haveticket(driver) == 0:
                driver.get('https://show.bilibili.com/platform/detail.html?id=72320&from=pc_ticketlist')
                WebDriverWait(driver, 5, 0.01).until(EC.presence_of_all_elements_located(
                    (By.XPATH, '/html/body/div/div[2]/div[2]/div[2]/div[4]/div[2]/div[1]/div')))

            driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[2]/div[4]/ul[1]/li[2]/div[1]').click()
            print("ok1")
            driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[2]/div[4]/ul[2]/li[2]/div').click()
            print("ok2")
            driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/div[4]/div[2]/div[1]/div').click()
            print("ok3")
            WeChat().send("抢票通道开启")
            time.sleep(2)
            #WebDriverWait(driver, 5, 0.01).until(
              #  EC.presence_of_all_elements_located((By.XPATH, '//*[@id="app"]/div[2]/div/div[6]/div[2]')))

            if not driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[6]/div[2]'):
                pass
            else:
                driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[6]/div[2]').click()
                cnt = 1
                if driver.find_element_by_id('payQRCode'):
                    WeChat().send("cp29 的票抢到了有十分钟的时间,快去付款！！！！！！！")
    finally:
        print('本轮结束！已截图')
        threading.Thread(target=screenshot, name="thread_screenshot").start()
        time.sleep(2)
        driver.close()
