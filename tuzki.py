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

def get_pageval(page):
    return (int(page)-1)*15

class TuzkiHandler(AcountHandler):
    def write_html(self, user = None, words= [],words_count = None, pager=None):
        return render.tuzki(user = user, words=words,words_count = words_count, pager=pager)

    def GET(self,page):
        user = self.valid()
        if not user:
            self.redirect('/login')
        #words = web.ctx.orm.query(WordsBook).filter(WordsBook.userid == user.userid).order_by(desc(WordsBook.date)).offerset((page-1)*15).limit(15).all()
        pageval = get_pageval(page);
        per_page_count = 15

        def has_prev_page(curr_page, words_count, per_page_count):
            return False

        def has_next_page(curr_page, words_count, per_page_count):
            return True

        words_count = web.ctx.orm.query(func.count('*')).filter(WordsBook.userid == user.userid).scalar()
        
        words = web.ctx.orm.query(WordsBook).filter(WordsBook.userid == user.userid).order_by(desc(WordsBook.date)).limit(per_page_count).offset(pageval).all()

        pager = {
            'current_page': page,
            'has_prev_page': has_prev_page(page, words_count, per_page_count),
            'has_next_page': has_next_page(page, words_count, per_page_count)
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

class TuzkiDetailHandler(AcountHandler):
    def write_html(self,user=None):
        return render.tuzki_help(user = user)

    def GET(self):
        user=self.valid()
        return self.write_html(user)

class TuzkiDeleteWordHandle(AcountHandler):
    def write_html(self,user =None):
        return render.tuzki_delete(user = user)
    def GET(self):
        user = self.valid()
        if not user:
            self.redirect('/login')

        word = "a"
        deleteWord =  web.ctx.orm.query(WordsBook).filter(WordsBook.userid == user.userid).filter(WordsBook.word == word).first()
        web.ctx.orm.delete(deleteWord)
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






















