# coding:utf-8

import json
import hashlib
import datetime
import base64
from urllib import request

class Send(object):
    def __init__(self,accountSid,accountToken,appId,serverIP,serverPort,softVersion):
        self.accountSid = accountSid
        self.accountToken = accountToken
        self.appId = appId
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.softVersion = softVersion

    def GenerateUrl(self):
        # 生成时间戳
        nowdate = datetime.datetime.now()
        self.batch = nowdate.strftime("%Y%m%d%H%M%S")

        # 生成sig
        signature = self.accountSid + self.accountToken + self.batch
        self.sig = hashlib.md5(signature.encode(encoding="UTF-8")).hexdigest().upper()

        # 拼接URL
        self.url = "https://" + self.serverIP + ":" + self.serverPort + "/" + self.softVersion + "/Accounts/" + self.accountSid + "/SMS/TemplateSMS?sig=" + self.sig

        # 生成auth
        src = self.accountSid + ":" + self.batch
        self.auth = base64.b64encode(src.encode(encoding='utf-8')).strip()


    def SendRequest(self,phone, temp, datas):
        self.GenerateUrl()
        data = {
            "to": phone,
            "appId": self.appId,
            "templateId": temp,
            "datas": datas
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json;charset=utf-8",
            "Authorization": self.auth
        }

        data_json = json.dumps(data)
        data_json = bytes(data_json, "utf8")
        req = request.Request(self.url, headers=headers, data=data_json)
        respone = request.urlopen(req).read().decode('utf-8')
        return respone














