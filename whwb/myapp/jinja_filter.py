# -*- coding: utf-8 -*-
__author__ = 'Bin'


# 时间格式化
def datetimeformat(value, format="%m-%d %H:%M"):
    # print value, type(value)
    return value.strftime(format)


# 截取字符串
def string_truncate(value, start=0, end=0):
    if start == 0:
        return value[:end]
    if end == 0:
        return value[start:]
    else:
        return value[start:end]



