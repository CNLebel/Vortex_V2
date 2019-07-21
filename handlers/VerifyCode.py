#coding:utf-8
import json
import logging
import random
import constants
import re
from .BaseHandler import BaseHandler
from utils.captcha import captcha
from utils.response_code import RET
from libs.yuntongxun.CCP import ccp



class ImageCodeHandler(BaseHandler):
    """"""
    def get(self):
        """获取图片验证码"""
        code_id = self.get_argument("code_id")
        pre_code_id = self.get_argument("pcode_id")
        if pre_code_id:
            try:
                self.redis.delete("image_code_%s"%pre_code_id)
            except Exception as e:
                logging.error(e)

        # 生成图片验证码
        name, text, image = captcha.captcha.generate_captcha()
        try:
            self.redis.setex(("image_code_%s"%code_id), constants.IMAGE_CODE_EXPIRES_SECONDS, text)
        except Exception as e:
            logging.error(e)
            self.write("")
        else:
            self.set_header("Content-Type","image/jpg")
            self.write(image)



class SMSCodeHandler(BaseHandler):
    """"""
    def post(self):

        # 获取参数
        # mobile = self.json_args.get("mobile")
        # image_code_id = self.json_args.get("image_code_id")
        # image_code_text = self.json_args.get("image_code_text")

        data = json.loads(self.get_argument("data"))
        mobile=data.get('mobile')
        image_code_id=data.get('image_code_id')
        image_code_text=data.get('image_code_text')

        # 参数校验
        if not all((mobile, image_code_id, image_code_text)):
            return self.write(dict(errno=RET.PARAMERR, errmsg="参数缺失"))
        if not re.match(r"1\d{10}",mobile):
            return self.write(dict(errno=RET.PARAMERR, errmsg="手机号格式错误"))

        # 判断图片难码
        try:
            real_image_code_text = self.redis.get("image_code_%s"%image_code_id)
            real_image_code_text = real_image_code_text.decode('ascii')
        except Exception as e:
            return self.write(dict(errno=RET.DBERR, errmsg="查询错误"))

        if not real_image_code_text:
            return self.write(dict(errno=RET.NODATA, errmsg="验证码过期"))

        if real_image_code_text.lower() != image_code_text.lower():
            return self.write(dict(errno=RET.DATAERR, errmsg="验证码错误"))

        # 若成功
        # 生成随机验证码
        sms_code ="%04d"%random.randint(0,9999)
        try:
            self.redis.setex(("sms_code_%s"%mobile), constants.SMS_CODE_EXPIRES_SECONDS, sms_code)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="数据库出错"))

        # 发送短信
        try:
            result = ccp.sendTemplateSMS(mobile, 1, [sms_code, constants.SMS_CODE_EXPIRES_SECONDS/60])
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.THIRDERR, errmsg="发送短信失败"))

        if result:
            self.write(dict(errcode=RET.OK, errmsg="发送成功"))
        else:
            self.write(dict(errcode=RET.UNKOWNERR, errmsg="发送失败"))













