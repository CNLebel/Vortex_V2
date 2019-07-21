#coding:utf-8

import logging
import hashlib
import config
import re
import json

from .BaseHandler import BaseHandler
from utils.response_code import RET
from utils.session import Session
from utils.common import require_login


class IndexHandler(BaseHandler):
    def get(self):
        logging.debug("debug msg")
        logging.info("info msg")
        logging.warning("warning msg")
        logging.error("error msg")
        print("print msg")
        self.write("hello itcast litong!  fsdffwefew")


class ResigerHandler(BaseHandler):
    """注册"""
    def post(self):

        # 获取参数
        # mobile = self.json_args.get("mobile")
        # sms_code = self.json_args.get("smscode")
        # password = self.json_args.get("password")

        data = json.loads(self.get_argument("data"))
        mobile = data.get('mobile')
        sms_code = data.get('smscode')
        password = data.get('password')
        password2 = data.get('password2')

        # 检查参数
        if not all([mobile, sms_code, password, password2]):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数不完整"))

        if not re.match(r"^1\d{10}$", mobile):
            return self.write(dict(errcode=RET.DATAERR, errmsg="手机号格式错误"))

        try:
            real_code = self.redis.get("sms_code_" + mobile)
            real_code = real_code.decode('ascii')
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="查询验证码出错"))

        # 判断短信验证码是否过期
        if not real_code:
            return self.write(dict(errcode=RET.NODATA, errmsg="验证码过期"))

        if real_code != str(sms_code):
            return self.write(dict(errno=2, errmsg="验证码错误!"))

        if password != password2:
            return self.write(dict(errno=RET.PWDERR, errmsg="密码错误!"))

        password = hashlib.sha256((config.passwd_hash_key + password).encode('utf-8')).hexdigest()

        sql = "insert into vor_user(vor_user_name,vor_user_mobile,vor_user_password) values(%(name)s, %(mobile)s, %(password)s);"
        try:
            user_id = self.db.execute(sql, name=mobile, mobile=mobile, password=password)
        except Exception as e:
            logging.error(e)
            return self.write({"errno":3, "errmsg":"手机号已注册!"})

        # 用session记录用户的登录状态
        try:
            self.session = Session(self)
            self.session.data["user_id"] = user_id
            self.session.data["name"] = mobile
            self.session.data["mobile"] = mobile
            self.session.save()
        except Exception as e:
            logging.error(e)

        self.write(dict(errcode=RET.OK, errmsg="注册成功"))



class LoginHandler(BaseHandler):
    """登录"""
    def post(self):
        # 获取参数
        # mobile = self.json_args.get("mobile")
        # password = self.json_args.get("password")
        data = json.loads(self.get_argument("data"))
        mobile = data.get('mobile')
        password = data.get('password')
        password2 = data.get('password2')

        # 检查参数
        if not all([mobile, password, password2]):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数错误"))
        if not re.match(r"^1\d{10}$", mobile):
            return self.write(dict(errcode=RET.DATAERR, errmsg="手机号错误"))

        res_mobile = self.db.get("select vor_user_mobile from vor_user where vor_user_mobile=%(mobile)s",mobile=mobile)
        if not res_mobile:
            return self.write(dict(errcode='3', errmsg="手机号未注册!"))

        # 检查秘密是否正确
        res = self.db.get("select vor_user_id, vor_user_name, vor_user_password from vor_user where vor_user_mobile=%(mobile)s or vor_user_name=%(mobile)s", mobile=mobile)
        password = hashlib.sha256((config.passwd_hash_key + password).encode('utf-8')).hexdigest()
        if res and res["vor_user_password"] == password:
            # 生成session数据
            # 返回客户端
            try:
                self.session = Session(self)
                self.session.data['user_id'] = res['vor_user_id']
                self.session.data['name'] = res['vor_user_name']
                self.session.save()
            except Exception as e:
                logging.error(e)
            return self.write(dict(errcode=RET.OK, errmsg="OK"))
        else:
            return self.write(dict(errcode=2, errmsg="手机号或密码错误！"))


class LogoutHandler(BaseHandler):
    """退出登录"""
    @require_login
    def get(self):
        # 清除session数据
        self.session= Session(self)
        self.session.clear()
        self.write(dict(errcode=RET.OK, errmsg="退出成功"))


class CheckLoginHandler(BaseHandler):
    """检查登陆状态"""
    def get(self):
        if self.get_current_user():
            self.write(dict(errcode=RET.OK, errmsg="true", data={"name":self.session.data.get("name")}))
        else:
            self.write(dict(errcode=RET.SESSIONERR, errmsg="false"))







