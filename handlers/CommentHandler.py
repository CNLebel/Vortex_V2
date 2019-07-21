#coding:utf-8

import logging
import hashlib
import config
import re

from .BaseHandler import BaseHandler
from utils.response_code import RET
from utils.common import require_login

class CreateCommentHandler(BaseHandler):
    def post(self):
        # 获取参数
        comment_user = self.json_args.get('comment_user')
        comment_article = self.json_args.get('comment_article')
        comment_content = self.json_args.get('comment_content')
        parent_comment_id = self.json_args.get('parent_comment_id')

        # 检查参数
        if not all([comment_user, comment_article, comment_content, parent_comment_id]):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数不完整"))

        sql = "insert into vor_comment(vor_comment_user,vor_comment_article,vor_comment_content,parent_comment_id) " \
              "values(%(user)s, %(article)s, %(content)s, %(parent)s);"

        try:
           comment_id = self.db.execute(sql, user=comment_user, article=comment_article, content=comment_content, parent=parent_comment_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DATAERR, errmsg="数据错误!"))

        if not comment_id:
            return self.write(dict(errno=RET.NODATA, errmsg="无数据!"))
        else:
            return self.write(dict(errno=RET.OK, errmsg="成功", comment_id=comment_id))


class EditCommentHandler(BaseHandler):
    def post(self):
        # 获取参数
        comment_id = self.json_args.get("comment_id")
        comment_user = self.json_args.get("comment_user")
        comment_content = self.json_args.get("comment_content")

        if not all([comment_id, comment_user, comment_content]):
            return self.write(dict(errno=RET.PARAMERR, errmsg="参数不完整"))

        try:
            current_user_id = self.get_current_user().get('user_id')
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.SESSIONERR, errmsg="用户未登录!"))

        if not comment_user == current_user_id:
            return self.write(dict(errno=RET.ROLEERR, errmsg="用户身份错误"))

        try:
            res = self.db.get("select * from vor_comment where vor_comment_id=%(id)s",id=comment_id)
            try:
                sql = "UPDATE vor_comment set vor_comment_content=%(content)s where vor_comment_id=%(id)s"
                self.db.execute(sql, content=comment_content, id=res.get('vor_comment_id'))
                self.write(dict(errno=RET.OK, errmsg="OK", comment_id=res.get('vor_comment_id')))
            except Exception as e:
                logging.error(e)
                return self.write(dict(errno=RET.DATAERR, errmsg="数据错误!"))
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DATAERR, errmsg="数据错误!"))


class DeleteCommentHandler(BaseHandler):
    def post(self):
        # 获取参数
        comment_id = self.json_args.get('comment_id')
        comment_user = self.json_args.get('comment_user')

        if not all([comment_id, comment_user]):
            return self.write(dict(errno=RET.PARAMERR, errmsg="参数不完整"))

        try:
            id = self.db.get("select * from vor_comment where vor_comment_id=%(id)s", id=comment_id).get('vor_comment_id')
            try:
                self.db.execute("delete from vor_comment where vor_comment_id=%(id)s", id=id)
                self.write(dict(errno=RET.OK, errmsg="OK", comment_id=id))
            except Exception as e:
                logging.error(e)
                return self.write(dict(errno=RET.DATAERR, errmsg="数据错误!"))
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DATAERR, errmsg="数据错误!"))
