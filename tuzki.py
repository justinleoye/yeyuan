#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os

import sae
import web
#~ import memcache

from setting import render
from account import AcountHandler
from models import WordsBook

from sqlalchemy import desc,distinct,or_,func
from utils import url_query_parser,row2dict
import json
import urllib2
import copy
import re
import time
import sys

# ensure the encoding is utf-8,so some werid errors won't occur!
reload(sys)
sys.setdefaultencoding('utf-8')

def valid_word(word):
    if type(word) == str and word:
        return True
    return False

def get_pageval(page,per_page_count):
    return (int(page)-1)*per_page_count

class TuzkiHandler(AcountHandler):
    def write_html(self, user = None, words= [],words_count = None, pager=None):
        return render.tuzki(user = user, words=words,words_count = words_count, pager=pager)

    def GET(self,page):
        user = self.valid()
        if not user:
            self.redirect('/login')
        #words = web.ctx.orm.query(WordsBook).filter(WordsBook.userid == user.userid).order_by(desc(WordsBook.date)).offerset((page-1)*15).limit(15).all()
        
        per_page_count = 10

        words_count = web.ctx.orm.query(func.count('*')).filter(WordsBook.userid == user.userid).scalar()

        all_page = words_count //per_page_count
        if words_count % per_page_count > 0:
            all_page = all_page +1
        def has_prev_page(curr_page):
            #using int()
            if int(curr_page)>1:
                return True
            else:
                return False

        def has_next_page(curr_page,all_page):
            if int(curr_page)  < all_page :
                return True
            else:
                return False

        pageval = get_pageval(page,per_page_count)
        
        words = web.ctx.orm.query(WordsBook).filter(WordsBook.userid == user.userid).order_by(desc(WordsBook.date)).limit(per_page_count).offset(pageval).all()

        pager = {
            'current_page': page,
            'all_page':all_page,
            'has_prev_page': has_prev_page(page),
            'has_next_page': has_next_page(page, all_page)
        }
        return self.write_html(user, words,words_count,pager)

    def POST(self):
        user = self.valid()

        if user:
            word = web.data()
            if(valid_word(word)):
                word_exist = web.ctx.orm.query(WordsBook).filter(WordsBook.userid == user.userid).filter(WordsBook.word == word).first()
                if not word_exist:
                    w = WordsBook(
                        userid = user.userid,
                        word = word,
                        count = 1
                    )
                    web.ctx.orm.add(w)
                    # code 0 means added at the first time
                    return json.dumps({'code': '0', 'count': '1'})
                else:
                    word_exist.count += 1
                    # code 1 means added at the second time or more
                    return json.dumps({'code': '1', 'count': str(word_exist.count)})
            # code 2 means word not valided
            return json.dumps({ 'code': '2' })
        else:
            # code 3 means user not valided
            return json.dumps({ 'code': "3"})

    def DELETE(self):
        user = self.valid()
        if user:
            userwordid = web.data()
            web.ctx.orm.query(WordsBook).filter(WordsBook.userid == user.userid).filter(WordsBook.userwordid == userwordid).delete()
            return json.dumps({'code': '1'})


class TuzkiDetailHandler(AcountHandler):
    def write_html(self,user=None):
        return render.tuzki_help(user = user)

    def GET(self):
        user=self.valid()
        return self.write_html(user)

        

class TuzkiGetAcountStateHandler(AcountHandler):
    def GET(self):
        user = self.valid()
        if user:
            #code 10 means user valided and return the valided userid
            return json.dumps({'code': '10', 'userid': user.userid, 'username': user.username, 'update': 'False'})
        else:
            # code 3 means user not valided
            return json.dumps({'code': '13', 'update': 'False'})


class TuzkiAPIHandler(AcountHandler):

    def GET(self):
        user = self.valid()
        if not user:
            self.redirect('/login')
        #words = web.ctx.orm.query(WordsBook).filter(WordsBook.userid == user.userid).order_by(desc(WordsBook.date)).offerset((page-1)*15).limit(15).all()
        query = web.ctx.query

        args = url_query_parser(query)
        page = int(args['page'])

        per_page_count = 10

        words_count = web.ctx.orm.query(func.count('*')).filter(WordsBook.userid == user.userid).scalar()

        all_page = words_count //per_page_count
        if words_count % per_page_count > 0:
            all_page = all_page +1
        def has_prev_page(curr_page):
            #using int()
            if int(curr_page)>1:
                return True
            else:
                return False

        def has_next_page(curr_page,all_page):
            if int(curr_page)  < all_page :
                return True
            else:
                return False

        pageval = get_pageval(page,per_page_count)
        
        words = web.ctx.orm.query(WordsBook).filter(WordsBook.userid == user.userid).order_by(desc(WordsBook.date)).limit(per_page_count).offset(pageval).all()
        word_list = []
        for word in words:
            word = row2dict(word)
            word['date'] = time.mktime(word['date'].timetuple())
            word_list.append(word)

        pager = {
            'current_page': page,
            'all_page':all_page,
            'has_prev_page': has_prev_page(page),
            'has_next_page': has_next_page(page, all_page)
        }
        return json.dumps({
            'pager':pager,
            'words':word_list
            })






















