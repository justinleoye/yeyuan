#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os

import sae
import web
#~ import memcache

from setting import render
from account import AcountHandler
from models import WordsBook

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

def valid_invitation_code(code):
    if valid_word(code):
        if code in [u'yechangjie',u'yezhangjie']:
            return True
    return False

class InvitationHandler(AcountHandler):
    def write_html(self, user=None, invitation_error=''):
        return render.invitation(user=user,invitation_error=invitation_error)

    def GET(self):
        user = self.valid()
        return self.write_html(user)

    def POST(self):
        i = web.input()
        invitation = i.invitation
        if type(invitation) == unicode:
            invitation = invitation.encode('utf8')
        print 'invi:',type(invitation)
        user = self.valid()
        if valid_invitation_code(invitation):
            web.setcookie('invitation-code',invitation)
            return self.redirect('/goagent')
        else:
            invitation_error = 'Invitation code error!/邀请码错误！'
            return self.write_html(user,invitation_error)

class GoagentHandler(AcountHandler):
    def write_html(self, user = None):
        return render.goagent_help(user = user)

    def GET(self):
        user = self.valid()
        is_invited = self.valid_invitation()
        if not is_invited:
            self.redirect('/invitation')
        return self.write_html(user)

    def valid_invitation(self):
        cookie_invitation_code = web.cookies().get('invitation-code')
        result = valid_invitation_code(cookie_invitation_code)
        if result:
            return True
        else:
            web.setcookie('invitation-code','')
            return False

