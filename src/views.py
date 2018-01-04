'''
Created on 4 ene. 2018

@author: Adrián
'''
from datetime import datetime
import os
import webapp2
import jinja2

from google.appengine.ext import ndb

from models import Eventos 

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = \
    jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

class BaseHandler(webapp2.RequestHandler):

    def render_template(
        self,
        filename,
        template_values,
        **template_args
        ):
        template = jinja_environment.get_template(filename)
        self.response.out.write(template.render(template_values)) 
    
class ShowEventos(BaseHandler):
    
    def get(self):
        #eventos = Eventos.query()
        self.render_template('eventos.html') #, {'eventos': eventos})