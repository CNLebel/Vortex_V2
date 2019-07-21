from .send import Send
import logging

_accountSid = "8aaf0708659e8e420165a9699fc207db"

_accountToken = "d7c8d85e3f3344ea98b5d4af3b8dd1ff"

_appId = "8a216da86b652116016b780b0c180f99"

_serverIP = "app.cloopen.com"

_serverPort = "8883"

_softVersion = "2013-12-26"


class _CCP(object):
    def __init__(self):
        self.send = Send(_accountSid,_accountToken,_appId,_serverIP,_serverPort,_softVersion)


    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def sendTemplateSMS(self, to, tempId, datas):
        return self.send.SendRequest(to, tempId, datas)

ccp = _CCP.instance()


if __name__ == '__main__':
    ccp.sendTemplateSMS('17788719869','1','["hello",2]')

