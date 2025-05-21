import requests
import pprint
import time
import schedule


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"

cookies = {
"buvid3":"A5600C67-CBD3-BFDE-F574-D8AE51189D2091704infoc",
"b_nut":"1664094891",
"i-wanna-go-back":"-1",
"_uuid":"42767F72-482F-4E5D-C833-BCEB138AA8C292012infoc",
"buvid4":"091F5A46-F034-A39A-27A7-EED4E7A8E89192892-022092516-NiF68S9WvH9H36ZKT5EOSQ%3D%3D",
"buvid_fp_plain":"undefined",
"nostalgia_conf":"-1",
"LIVE_BUVID":"AUTO8816645616706381",
"fingerprint":"c20131f17e5989e4b9620080f78cb15c",
"buvid_fp":"5d34caaa8d33264eb589a3b17ae2da44",
"CURRENT_BLACKGAP":"0",
"is-2022-channel":"1",
"CURRENT_FNVAL":"4048",
"rpdid":"|(uRkJRmRm|R0J'uYYmRmY|)u",
"CURRENT_QUALITY":"0",
"FEED_LIVE_VERSION":"V8",
"header_theme_version":"CLOSE",
"DedeUserID":"5942570",
"DedeUserID__ckMd5":"62ab001a2c06170b",
"b_ut":"5",
"SESSDATA":"e978ca94%2C1698114475%2C3e0f4%2A42",
"bili_jct":"e4b9602379355155e3fda2ce4e99990a",
"bp_video_offset_5942570":"789176957827809300",
"PVID":"1",
"home_feed_column":"5",
"browser_resolution":"1536-746",
"msource":"pc_web",
"from":"pc_ticketlist",
"deviceFingerprint":"1de4f7e882a2a782ac373021d8a8b4bb",
"Hm_lvt_909b6959dc6f6524ac44f7d42fc290db":"1682583178,1682606854,1682606886,1682678241",
"Hm_lpvt_909b6959dc6f6524ac44f7d42fc290db":"1682678241"
}

device_id = cookies["deviceFingerprint"]

project_id = "72320"
screen_id = "126698"
sku_id = "380920"

#project_id = "71352"
#screen_id = "120772"
#sku_id = "371307"


name = "冯碧川"
phone = "13023151153"
pay_money = "8000"


def getToken():
    token_url = "https://show.bilibili.com/api/ticket/order/prepare"
    data = {
        "project_id": project_id,
        "screen_id": screen_id,
        "order_type": "1",
        "count": "1",
        "sku_id": sku_id,
        "token": "",
    }
    res = requests.post(
        token_url, data=data, cookies=cookies, headers={"User-Agent": USER_AGENT})
    token_json = res.json()
    pprint.pprint(token_json)
    if token_json["errno"] == 0:
        return token_json["data"]["token"]
    return None


def placeOrder(token: str):
    order_url = "https://show.bilibili.com/api/ticket/order/createV2"
    data = {
        "project_id": project_id,
        "screen_id": screen_id,
        "order_type": "1",
        "count": "1",
        "sku_id": sku_id,
        "token": token,
        "deviceId": device_id,
        "pay_money": pay_money,
        "timestamp": str(int(time.time() * 1000)),
        "buyer": name,
        "tel": phone
    }
    res = requests.post(
        order_url, data=data, cookies=cookies, headers={"User-Agent": USER_AGENT})
    order_json = res.json()
    pprint.pprint(order_json)
    if order_json["errno"] == 0:
        return order_json["data"]["token"]
    return None


def checkOrder(order_token: str):
    check_url = f"https://show.bilibili.com/api/ticket/order/createstatus?token={order_token}&timestamp={int(time.time() * 1000)}"
    res = requests.get(
        check_url, cookies=cookies, headers={"User-Agent": USER_AGENT})
    check_json = res.json()
    pprint.pprint(check_json)
    if check_json["errno"] == 0:
        return check_json["data"]["order_id"]
    return None


def job():
    token = ""
    while True:
        token = getToken()
        if token != None:
            break
        time.sleep(0.1)
    order_token = ""
    while True:
        order_token = placeOrder(token)
        if order_token != None:
            break
        time.sleep(0.1)
    order_id = ""
    while True:
        order_id = checkOrder(order_token)
        if order_id != None:
            break
        time.sleep(0.1)

    order_detail_url = "https://show.bilibili.com/platform/orderDetail.html?order_id={order_id}"
    print('success! pay your order here: ' + order_detail_url)


job()
cnt = 0
schedule.every().day.at('18:59:59').do(job)
while True:
    schedule.run_pending()

    time.sleep(1)