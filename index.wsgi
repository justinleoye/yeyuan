#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

import sae
import web

import copy

from setting import render
from setting import load_sqla
from account import get_user
from models import User
from account import AcountHandler,SignupHandler,LoginHandler,LogoutHandler,WelcomeHandler,ProfileHandler,EditProfileHandler,DelAcountHandler,get_user
from tuzki import TuzkiHandler,TuzkiDetailHandler,TuzkiGetAcountStateHandler,TuzkiDeleteWordHandle
from goagent import GoagentHandler,InvitationHandler
# the urls of the web system
urls = (
    '/(.*)/', 'RedirectHandler',
    '/', 'HomeHandler',
    '/home','HomeHandler',
    '/tuzki_page/([0-9]*)','TuzkiHandler',  
    '/tuzki_help','TuzkiDetailHandler',
    '/tuzki_delete','TuzkiDeleteWordHandle',
    '/tuzki-get-acount-state','TuzkiGetAcountStateHandler',
    '/goagent','GoagentHandler',
    '/invitation','InvitationHandler',
    '/user/([0-9]*)','UserHandler',
    '/about','AboutHandler',
    '/contact','ContactHandler',
    '/terms','TermsHandler',
    '/help','HelpHandler',
    '/signup','SignupHandler',
    '/login','LoginHandler',
    '/logout','LogoutHandler',
    '/welcome','WelcomeHandler',
    '/profile','ProfileHandler',
    '/editprofile','EditProfileHandler',
    '/delacount','DelAcountHandler',
    '/test','TestHandler'
)


#access the database
#db = web.database(dbn='mysql', db='alexbox', user='root', pw='alexzone')

class Handler:
    def redirect(self,path):
        web.seeother(path)

#when the url ended with '/',then redirect the url to the one without ending '/'
class RedirectHandler(Handler):
    def GET(self, path):
        self.redirect('/' + path)

class HomeHandler(AcountHandler):
    def write_html(self, user=None, items=None):
        return render.home(user=user, items=items)

    def GET(self):
        user=self.valid()
        user_agent_check = self.check_user_agent()
        if not user_agent_check:
            self.redirect('/help#browser')
        return self.write_html(user)

    def POST(self):
        user = self.valid()

        i = web.input()
        
class UserHandler(AcountHandler):
    def write_html(self,user=None, owner=None, search_error=''):
        return render.user(user=user, owner=owner, search_error=search_error)

    def GET(self,userid):
        user=self.valid()
        owner = get_user(userid)

        search_error = '200'
        if not owner:
            search_error='616' #user not found

        if owner:

            return self.write_html(user,owner,search_error)
        return self.write_html(user=user,owner=owner,search_error=search_error)

    
class AboutHandler(AcountHandler):
    def write_html(self, user=None):
        return render.about(user=user)

    def GET(self):
        user=self.valid()
        return self.write_html(user)

class ContactHandler(AcountHandler):
    def write_html(self, user=None):
        return render.contact(user=user)
        
    def GET(self):
        user=self.valid()
        return self.write_html(user)

class TermsHandler(AcountHandler):
    def write_html(self, user=None):
        return render.terms(user=user)

    def GET(self):
        user=self.valid()
        return self.write_html(user)

class HelpHandler(AcountHandler):
    def write_html(self,user=None):
        return render.help(user=user)

    def GET(self):
        user = self.valid()

        return self.write_html(user)

class TestHandler(AcountHandler):
	def write_html(self,user = None):
		return render.test(user=user)

	def GET(self):
		user = self.valid()

		return self.write_html(user)

#class Referer:
    #def GET(self):
        #referer = web.ctx.env.get('HTTP_REFERER','http://google.com')
        ##raise web.seeother(referer)
        ##return web.ctx.env
        ##return web.ctx.path
        ##return web.ctx.home
        ##return web.ctx.homedomain
        ##return web.ctx.status
        #return web.ctx.headers

app = web.application(urls, globals())
app.add_processor(load_sqla)

application = sae.create_wsgi_app(app.wsgifunc())

