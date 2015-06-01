#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sae
import web

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text , DateTime


Base = declarative_base()

class User(Base):
    __tablename__='user'

    userid = Column(Integer, primary_key = True)
    username = Column(String(20))
    userpass = Column(String(100))
    salt = Column(String(100))
    email = Column(String(100))
    qq = Column(String(13))

class WordsBook(Base):
    __tablename__ = 'wordsbook'

    userwordid = Column(Integer, primary_key = True)
    userid = Column(Integer)
    word = Column(String(60))
    count = Column(Integer)
    date = Column(DateTime)
