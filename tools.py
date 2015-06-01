#!/usr/bin/env python
#-*- coding: utf-8 -*-

from math import ceil,floor

class InvalidPage(Exception):
    pass

class PageNotAnInteger(InvalidPage):
    pass

class EmptyPage(InvalidPage):
    pass

class Paginator(object):
    def __init__(self,total_records=None,per_page=None,display_certain_size=5):
        # total records
        self.total_records = total_records

        # records per page
        self.per_page = per_page

        # total pages
        self.total_pages = 0

        #data
        self.data = {}

        #display certain links per page
        self.display_certain_size = display_certain_size

        # start calculate the pages
        self.__judge__()

    def __judge__(self):
        # records could not display in one page
        if self.total_records > self.per_page:
            # calculate the total pages, get value under floor
            self.total_pages = int(floor(self.total_records/float(self.per_page)))

            # calculate the start and end of each page
            for i in range(0,self.total_pages):
                if i == 0:
                    self.data[i+1] = Page(i+1,i,i+self.per_page,self)
                else:
                    self.data[i+1] = page(i+1,self.data[i].end,self.data[i].end+self.per_page,self)

            if self.total_pages < (self.total_records/float(self.per_page)):
                # cal the last page,and it should be full
                self.data[self.total_pages+1] = Page(self.total_pages+1,self.data[self.total_pages].end.self.total_records,self)
        else:
            self.total_pages = 1
            self.data[1] = Page(1,0,self.total_records,self)

    def page(self,page_number):
        page_number = int(page_number)
        if page_number in self.data.keys():
            return self.data[page_number]
        else:
            raise EmptyPage("The page contains no results")

    # check if all the records can display on one page
    def check_less_than_certain_size(self):
        if len(self.data) <= self.display_certain_size:
            return True
        else:
            return False

    # calculate the display page links
    def calculate_display_pages(self,page_number):
        # the current request pages less than page links each display
        display_pages = {}
        # display all pages except one
        if len(self.data) == 1:
            return None
        elif self.check_less_than_certain_size():
            return self.sort_dict_values(self.data)
        else:
            if page_number <= self.display_certain_size/float(2):
                for i in range(0,self.display_certain_size):
                    display_pages[i+1] = self.data[i+1]
            else:
                # current page items minus the half of the displayed items more than 0,
                # current page items plus the half of the displayed items less than the whole items
                half_of_display_certain_size = int(floor(self.display_certain_size/float(2)))
                if page_number - half_of_display_certain_size > 0 and page_number + half_of_display_certain_size <= len(self.data):
                    for i in range(page_number - half_of_display_certain_size,page_number + half_of_display_certain_size + 1):
                        display_pages[i] = self.data[i]
                else:
                    for i in range(len(self.data) - self.display_certain_size + 1, len(self.data) + 1):
                        display_pages[i] = self.data[i]

        return self.sort_dict_values(display_pages)

    # sort for the dict
    def sort_dict_values(self,adict):
        keys = adict.keys()
        keys.sort()
        return [(key,adict[key]) for key in keys]

#Page class        include the start and end of each page,and the current page holds where
class Page(object):
    def __init__(self,page_number=1,start=0,end=0,paginator=None):
        # the start of each page
        self.start = start

        # the end of each page
        self.end = end

        # the page number of each page
        self.page_number = page_number

        # paginator tool class
        self.paginator = paginator

        # next page
        self.next_page_number = self.page_number + 1
        # previous page
        self.prev_page_number =self.page_number -1

    def __repr__(self):
        return '<Page start at %s end at %s>' % (self.start,self.end)

    # whether next page exists
    def has_next(self):
        return self.page_number<self.paginator.total_records/float(self.paginator.per_page)

    # whether previous page exists
    def has_prev(self):
        return self.page_number>1





























