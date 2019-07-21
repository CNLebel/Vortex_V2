#coding:utf-8

import os
from handlers import Passport, VerifyCode, UserCenter, Articles, LabelHandler, CommentHandler

handlers = [
    (r"/", Passport.IndexHandler),
    (r"/api/imagecode", VerifyCode.ImageCodeHandler),
    (r"/api/smscode", VerifyCode.SMSCodeHandler),

    (r"/api/edituserinfo", UserCenter.EditUserInfoHandler),
    (r"/api/userinfo", UserCenter.UserInfoHandler),

    (r"/api/register", Passport.ResigerHandler),
    (r"/api/login", Passport.LoginHandler),
    (r"/api/logout", Passport.LogoutHandler),
    (r"/api/checklogin", Passport.CheckLoginHandler),

    (r"/api/publicarticle", Articles.PublicArticleHandler),
    (r"/api/editarticle", Articles.EditArticleHandler),
    (r"/api/deletearticle", Articles.DeleteArticleHandler),
    (r"/api/sortarticle", Articles.SortArticleHandler),
    (r"/api/listarticle", Articles.ListArticleHandler),


    (r"/api/createlabel", LabelHandler.CreateLabelHandler),
    (r"/api/deletelabel", LabelHandler.DeleteLabelHandler),

    (r"/api/createcomment", CommentHandler.CreateCommentHandler),
    (r"/api/editcomment", CommentHandler.EditCommentHandler),
    (r"/api/deletecomment", CommentHandler.DeleteCommentHandler),

]
