# -*- coding:utf8 -*-
# add by lee 14.7.28 17:20
__author__ = 'hugleecool'

# 模仿microblog的mail。看来，要多看书。

from threading import Thread

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper