#coding:utf-8

import logging
import hashlib
import config
import re

from .BaseHandler import BaseHandler
from utils.response_code import RET

class CreateLabelHandler(BaseHandler):
    def post(self):
        # 获取参数
        label_name = self.json_args.get("label_name")
        label_alias = self.json_args.get("label_alias")

        # 检查参数
        if not all([label_name, label_alias]):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数不完整"))

        sql = "insert into vor_label(vor_label_name, vor_label_alias) values(%(name)s, %(alias)s)"

        try:
            label_id = self.db.execute(sql, name=label_name, alias=label_alias)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DATAERR, errmsg="数据错误!"))

        if not label_id:
            return self.write(dict(errno=RET.NODATA, errmsg="无数据!"))
        else:
            return self.write(dict(errno=RET.OK, errmsg="成功", label_id=label_id))



class DeleteLabelHandler(BaseHandler):
    def post(self):
        # 获取参数
        label_id = self.json_args.get('label_id')
        if not all([label_id]):
            return self.write(dict(errcode=RET.PARAMERR, errmsg='参数错误'))
        try:
            res=self.db.get("select * from vor_label where vor_label_id=%(id)s", id=label_id)
            try:
                self.db.execute("delete from vor_label where vor_label_id=%(id)s", id=res.get('vor_label_id'))
                self.write(dict(errno=RET.OK, errmsg="OK", label_id=res.get('vor_label_id')))
            except Exception as e:
                logging.error(e)
                return self.write(dict(errno=RET.DATAERR, errmsg="数据错误!"))

        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DATAERR, errmsg="数据错误!"))





