#!/usr/bin/env python
#-*- coding: utf-8 -*-

def url_query_parser(query):
    query = query[1::]
    args_str = query.split('&')
    args = {}
    for a_str in args_str:
        args_key,args_value = a_str.split('=')
        args_key = args_key.strip()
        args_value = args_value.strip()
        args[args_key] = args_value

    return args

def row2dict(row):
    d = { }
    for column in row.__table__.columns:
        d[column.name] = getattr(row,column.name)

    return d
