from datetime import datetime
import os
import webapp2
import jinja2

from google.appengine.ext import ndb

from models import Eventos, Usuario
from __builtin__ import int


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
       eventos = Eventos.query()
       #{'eventos':eventos}
       self.render_template('listadoEventos.html',{'eventos':eventos} )
       
class CrearEvento(BaseHandler):
    
    def post(self):
        usuario = Usuario(nombre="ADRI",email="cardenitas96@gmail.com")
        usuario.put()
        
        evento = Eventos(nombre=self.request.get('nombre'),
                         descripcion=self.request.get('descripcion'),
                         direccion=self.request.get('direccion'),
                         creador= usuario,
                         latitud=float(self.request.get('latitud')),
                         longitud=float(self.request.get('longitud')),
                         fechaInicio=self.request.get('fechaInicio'),
                         fechaFin=self.request.get('fechaFin'))
        evento.put()
        return webapp2.redirect('/')
    
    def get(self):
        self.render_template('CrearEvento.html',{})
        
class DeleteEvento(BaseHandler):
    
    def get(self,evento_id):
        iden = int(evento_id)
        evento = Eventos.get_by_id(iden)
        evento.key.delete()
        return webapp2.redirect('/')
    
class EditEvento(BaseHandler):
    
    def get(self,evento_id):
        iden = int(evento_id)
        evento = Eventos.get_by_id(iden)
        self.render_template('editarevento.html', {'evento':evento})
        
    def post(self,evento_id):
        iden = int(evento_id)
        evento = Eventos.get_by_id(iden)
        evento.nombre = self.request.get('nombre')
        evento.descripcion=self.request.get('descripcion')
        evento.latitud = float(self.request.get('latitud'))
        evento.longitud = float(self.request.get('longitud'))
        evento.fechaInicio=self.request.get('fechaInicio')
        evento.fechaFin=self.request.get('fechaFin')
        evento.put()
        return webapp2.redirect('/')