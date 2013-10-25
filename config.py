# -*- coding: utf-8 -*-
import jinja2
import os

jinja_enviroment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+'/views/'))
