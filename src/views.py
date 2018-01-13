from datetime import datetime
import os
import webapp2
import jinja2
#import googlemaps


from google.appengine.ext import ndb
from google.appengine.api import users

from __builtin__ import int
from models import Usuario, Eventos, Comentario

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
        user = users.get_current_user()
        usuario = Usuario.query().filter(Usuario.email == user.email()).get()
        
        if not usuario:
            usuario = Usuario (nombre = user.nickname(), email = user.email())
            usuario.put()
            
        eventos = Eventos.query()
        self.render_template('listadoEventos.html',{'eventos':eventos} )
       
class CrearEvento(BaseHandler):
    
    def post(self):
        #usuario = Usuario(nombre="ADRI",email="cardenitas96@gmail.com")
        #usuario.put()
        user = users.get_current_user()
        usuario = Usuario.query().filter(Usuario.email == user.email()).get()
        
        evento = Eventos(nombre=self.request.get('nombre'),
                         descripcion=self.request.get('descripcion'),
                         direccion=self.request.get('direccion'),
                         creador= usuario,
                         latitud=float(self.request.get('latitud')),
                         longitud=float(self.request.get('longitud')),
                         fechaInicio=self.request.get('fechaInicio'),
                         fechaFin=self.request.get('fechaFin'),
                         likes = [],
                         comentarios =[]
                         )
                         
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

class OpenEvento(BaseHandler):
    def get(self, evento_id):
        iden = int(evento_id)
        evento = Eventos.get_by_id(iden)
        user = users.get_current_user()
        usuario = Usuario.query().filter(Usuario.email == user.email()).get()
        #gmaps = googlemaps.Client(key='ce467785e4e6b7dc282e86e0f2268c26')
        #reverse_geocode_result = gmaps.reverse_geocode((evento.latitud, evento.longitud))
        #now = datetime.now()
        #self.render_template('verEvento.html', {'evento':evento, 'map':reverse_geocode_result})
        self.render_template('verEvento.html', {'evento': evento, 'user':usuario})

    def post(self, evento_id):
        iden = int(evento_id)
        evento = Eventos.get_by_id(iden)
        usuarioSesion = users.get_current_user()
        email = usuarioSesion.email()
        usuario = Usuario.query().filter(Usuario.email == email).get()
        
        comentario = Comentario(autor = usuario,
                                comentario = self.request.get('comentario') ) 
        
        if not evento.comentarios:
            evento.comentarios = [comentario]
        else:
            evento.comentarios.append(comentario) 
        
        evento.put()
        self.render_template('verEvento.html', {'evento': evento, 'user':usuario})
        #return webapp2.redirect('/open/')

class LikeEvento(BaseHandler):
    def get(self, evento_id):
        iden = int(evento_id)
        evento = Eventos.get_by_id(iden)
        usuarioSesion = users.get_current_user()
        email = usuarioSesion.email()
        usuario = Usuario.query().filter(Usuario.email == email).get()
        
        if not evento.likes :
            evento.likes = [usuario]
        else:
            evento.likes.append(usuario) 
    
        evento.put()
        self.render_template('verEvento.html', {'evento': evento, 'user':usuario})
        
class Logout(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            logout = users.create_logout_url('/')
            return self.redirect(logout)
            
        
        