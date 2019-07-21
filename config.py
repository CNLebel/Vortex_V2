#coding:utf-8

import os

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "template"),
    "cookie_secret": "PzqVDnApQRqMDOohV3EF8glpfCcX+0Nyus5kcpeIFdw=",
    "xsrf_cookies": False,
    "debug": True,
}


mysql_options = dict(
    host="127.0.0.1",
    database="vortex_v2",
    user="root",
    password="LItong1998"
)


redis_options = dict(
    host = "127.0.0.1",
    port = 6379
)

log_file = os.path.join(os.path.dirname(__file__), "logs/log")
log_level = "debug"

session_expires = 86400

passwd_hash_key = "nlgCjaTXQX2jpupQFQLoQo5N4OkEmkeHsHD9+BBx2WQ="