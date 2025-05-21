import requests
TO_USER = 'tracy'
class WeChat():
    def __init__(self):
        self.CORP_ID = "ww23ed864e1727f8ac"
        self.SECRET = "pLAHzse5N3ATwdQexvysT1zBU7_L0mmCfytg4h8tNao"
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
        print(res)
        if res['errmsg'] == 'ok':
            print("已通过企业微信发送提醒")
            return "已通过企业微信发送提醒"
        else:
            return res

WeChat().send("text")