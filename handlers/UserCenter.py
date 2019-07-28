#coding:utf-8

import logging
import hashlib
import config
import re

from .BaseHandler import BaseHandler
from utils.session import Session
from utils.response_code import RET



class EditUserInfoHandler(BaseHandler):
    pass

class UserInfoHandler(BaseHandler):
    def get(self):

        current_id=self.get_current_user().get('user_id')
        # current_id=10001
        sql = "select * from vor_user where vor_user_id=%(id)s"
        try:
            userinfo=self.db.get(sql,id=current_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DATAERR, errmsg="数据错误!"))
        users = {
            'user_id': userinfo['vor_user_id'],
            'user_photo': userinfo['vor_user_photo'],
            'user_name':userinfo['vor_user_name'],
            'user_mobile':userinfo['vor_user_mobile'],
            'user_wechat':userinfo['vor_user_wechat'],
            'user_qq':userinfo['vor_user_qq'],
            'user_nickname':userinfo['vor_user_nickname'],
            'user_address':userinfo['vor_user_address'],
            'user_occupation':userinfo['vor_user_occupation'],
            'user_interest':userinfo['vor_user_interest'],
            'user_aboutme':userinfo['vor_user_aboutme'],
            'user_ctime':str(userinfo['vor_user_ctime']),
        }
        print(users)

        if not userinfo:
            return self.write(dict(errno=RET.NODATA, errmsg="无数据!"))
        else:
            return self.write(dict(errno=RET.OK, errmsg="OK",message=users ))











