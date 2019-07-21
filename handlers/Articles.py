#coding:utf-8

import logging
import hashlib
import config
import re
import json
import datetime

from .BaseHandler import BaseHandler
from utils.response_code import RET
from utils.common import require_login


class PublicArticleHandler(BaseHandler):

    @require_login
    def post(self):
        # 获取参数
        article_author = self.json_args.get("article_author")
        article_title = self.json_args.get("article_title")
        article_content = self.json_args.get("article_content")
        article_sort = self.json_args.get("article_sort")
        article_abstract = self.json_args.get("article_abstract")
        article_abstract_img = self.json_args.get("article_abstract_img")

        # 检查参数
        if not all([article_author, article_title, article_content,article_sort,
                    article_abstract,article_abstract_img
                ]):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数不完整"))

        sql = "insert into vor_article(vor_article_author,vor_article_title,vor_article_content,vor_article_sort,vor_article_abstract," \
              "vor_article_abstract_img) values(%(author)s, %(title)s, %(content)s, %(sort)s, %(abstract)s, %(abstract_img)s);"

        try:
            article_id = self.db.execute(sql, author=article_author, title=article_title, content=article_content,
                                      sort=article_sort, abstract=article_abstract, abstract_img=article_abstract_img)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DATAERR, errmsg="数据错误!"))

        if not article_id:
            return self.write(dict(errno=RET.NODATA, errmsg="无数据!"))
        else:
            return self.write(dict(errno=RET.OK, errmsg="成功", article_id=article_id))


class EditArticleHandler(BaseHandler):

    @require_login
    def post(self):
        # 获取参数
        article_id = self.json_args.get("article_id")
        article_author = self.json_args("article_author")
        article_title = self.json_args.get("article_title")
        article_content = self.json_args.get("article_content")
        article_sort = self.json_args.get("article_sort")
        article_abstract = self.json_args.get("article_abstract")
        article_abstract_img = self.json_args.get("article_abstract_img")

        # 检查参数
        if not all([article_id, article_title, article_content,article_sort,article_abstract,article_abstract_img]):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数不完整"))

        sql = "UPDATE vor_article set vor_article_title=%(title)s, vor_article_content=%(content)s, vor_article_sort=%(sort)s, " \
              "vor_article_abstract=%(abstract)s, vor_article_abstract_img=%(abstract_img)s where vor_article_id=%(id)s"

        try:
            res = self.db.execute(sql, title=article_title, content=article_content,sort=article_sort, abstract=article_abstract,
                                         abstract_img=article_abstract_img,id=article_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DATAERR, errmsg="数据错误!"))

        if not res:
            return self.write(dict(errno=RET.NODATA, errmsg="无数据!"))
        else:
            return self.write(dict(errno=RET.OK, errmsg="成功", article_id=article_id))


class DeleteArticleHandler(BaseHandler):
    def post(self):
        # 获取参数
        article_id = self.json_args.get('article_id')
        article_user = self.json_args.get('article_user')
        if not all([article_id, article_user]):
            return self.write(dict(errcode=RET.PARAMERR, errmsg='参数错误'))
        try:
            id = self.db.get("select * from vor_article where vor_article_id=%(id)s", id=article_id).get('vor_article_id')
            try:
                self.db.execute("delete from vor_article where vor_article_id=%(id)s", id=id)
                self.write(dict(errno=RET.OK, errmsg="OK", label_id=id))
            except Exception as e:
                logging.error(e)
                return self.write(dict(errno=RET.DATAERR, errmsg="数据错误!"))
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DATAERR, errmsg="数据错误!"))


class ListArticleHandler(BaseHandler):
    def get(self):
        """获取参数"""
        page_limit = int(self.get_argument('page_limit'))
        page_start = int(self.get_argument('page_start'))

        # 检查参数
        if not all([page_limit,page_start]):
            return self.write(dict(errcode=RET.PARAMERR, errmsg='参数错误'))

        page_start = (page_start - 1) * page_limit
        sql = "select * from vor_article limit %(start)s, %(page)s;"
        try:
            article_list=self.db.query(sql,start=page_start,page=page_limit)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DATAERR, errmsg="数据错误!"))

        if not article_list:
            return self.write(dict(errno=RET.NODATA, errmsg="无数据!"))
        else:
            article = []
            for i in article_list:
                i = {
                    "article_id": i['vor_article_id'],
                    "article_title": i['vor_article_title'],
                    "article_author": i['vor_article_author'],
                    "article_content": i['vor_article_content'],
                    "article_sort": i['vor_article_sort'],
                    "article_abstract": i['vor_article_abstract'],
                    "article_abstract_img": i['vor_article_abstract_img'],
                    "article_views": i['vor_article_views'],
                    "article_like_count": i['vor_article_like_count'],
                    "article_comment_count": i['vor_article_comment_count'],
                    # "create_time": i['vor_article_ctime'],
                }
                article.append(i)
            self.write(dict(errno=RET.OK, errmsg="OK",message=article ))
            article.clear()



class SortArticleHandler(BaseHandler):
    pass


