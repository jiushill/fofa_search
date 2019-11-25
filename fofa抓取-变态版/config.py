#@author:九世
#@time:2019/10/27
#@file:config.py

import base64

data="后台登录"
SEARCH=str(bytes.decode(base64.b64encode(bytes(data,encoding='utf-8')))).replace('+','%2B')
PAGE=30
COOKIES="<FOFA_YOUR_COOKIE>"
