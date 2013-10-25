# -*- coding: utf-8 -*-
import webapp2
import jinja2
import os

from routes import route_list

app = webapp2.WSGIApplication( route_list, debug=True)
    
