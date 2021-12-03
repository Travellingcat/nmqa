from flask import g,redirect,url_for
from functools import wraps

# 用装饰器写登录鉴权
def log_required(func):
    @wraps(func)
    def wrappers(*args, **kwargs):
        if hasattr(g, 'user'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for("user.login"))
    return wrappers