#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os

import sae
import web
#~ import memcache

from setting import render
from account import AcountHandler
from models import WordsBook

from sqlalchemy import desc,distinct,or_

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


class TuzkiHandler(AcountHandler):
    def write_html(self, user = None, words= []):
        return render.tuzki(user = user, words=words)

    def GET(self):
        user = self.valid()
        if not user:
            self.redirect('/login')
        words = web.ctx.orm.query(WordsBook).filter(WordsBook.userid == user.userid).order_by(desc(WordsBook.date)).all()

        return self.write_html(user, words)

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

class TuzkiGetAcountStateHandler(AcountHandler):
    def GET(self):
        user = self.valid()
        if user:
            #code 10 means user valided and return the valided userid
            return json.dumps({'code': '10', 'userid': user.userid, 'username': user.username, 'update': 'False'})
        else:
            # code 3 means user not valided
            return json.dumps({'code': '13', 'update': 'False'})






















