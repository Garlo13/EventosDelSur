from datetime import datetime
import os
import webapp2
import jinja2
import json


from google.appengine.ext import ndb
from google.appengine.api import users

from __builtin__ import int
from models import Usuario, Eventos, Comentario, Tag

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
       
       
        diccionario = []
        for evento in eventos:
            diccionario.append(evento.nombre.encode('utf-8'))
            diccionario.append(evento.latitud)
            diccionario.append(evento.longitud)
            #diccionario[evento.nombre.encode("utf-8")]=(evento.latitud,evento.longitud)
           
           # diccionario= ['evento':{'nombre':evento.nombre.encode('utf-8'), 'latitud':evento.latitud, 'longitud':evento.longitud}]
        #dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
        #jsondic = json.dumps(diccionario)
        print diccionario
        self.render_template('listadoEventos.html',{'eventos':eventos, 'diccionario':diccionario} )
       
class CrearEvento(BaseHandler):
    
    def post(self):
        #usuario = Usuario(nombre="ADRI",email="cardenitas96@gmail.com")
        #usuario.put()
        user = users.get_current_user()
        usuario = Usuario.query().filter(Usuario.email == user.email()).get()
        
        seleccion = self.request.get('checks', allow_multiple = True)
        listaTags = [];
        
        for nombreTag in seleccion:
            tag = Tag.query().filter(Tag.nombre == nombreTag).get()
            listaTags.append(tag)
        
        
        evento = Eventos(nombre=self.request.get('nombre'),
                         descripcion=self.request.get('descripcion'),
                         direccion=self.request.get('direccion'),
                         creador= usuario,
                         latitud=float(self.request.get('latitud')),
                         longitud=float(self.request.get('longitud')),
                         fechaInicio=self.request.get('fechaInicio'),
                         fechaFin=self.request.get('fechaFin'),
                         likes = [],
                         comentarios =[],
                         tags = listaTags
                         )
                         
        evento.put()
        return webapp2.redirect('/')
    
    def get(self):
        tags = Tag.query()
        self.render_template('CrearEvento.html', {'tags':tags})
        
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
        tags = Tag.query()
        
        tagsevento = map(lambda tag: tag.nombre, evento.tags) #Devuelve una lista de nombre de eventos (strings)
        
        self.render_template('editarevento.html', {'evento':evento, 'tags':tags, 'tagseventos':tagsevento})
        
    def post(self,evento_id):
        iden = int(evento_id)
        evento = Eventos.get_by_id(iden)
        
        seleccion = self.request.get('checks', allow_multiple = True)
        listaTags = [];
        
        for nombreTag in seleccion:
            tag = Tag.query().filter(Tag.nombre == nombreTag).get()
            listaTags.append(tag)
        
        evento.nombre = self.request.get('nombre')
        evento.descripcion=self.request.get('descripcion')
        evento.latitud = float(self.request.get('latitud'))
        evento.longitud = float(self.request.get('longitud'))
        evento.fechaInicio=self.request.get('fechaInicio')
        evento.fechaFin=self.request.get('fechaFin')
        evento.tags = listaTags
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
        nombreTags = map(lambda tag: tag.nombre.encode("utf-8"), evento.tags)      
        self.render_template('verEvento.html', {'evento': evento, 'user':usuario, 'nombreTags':nombreTags })

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
        
        #self.render_template('verEvento.html', {'evento': evento, 'user':usuario})
        return webapp2.redirect('/open/'+evento_id)

class LikeEvento(BaseHandler):
    def get(self, evento_id):
        iden = int(evento_id)
        evento = Eventos.get_by_id(iden)
        usuarioSesion = users.get_current_user()
        email = usuarioSesion.email()
       # usuario = Usuario.query().filter(Usuario.email == email).get()
        
        if not evento.likes :
            evento.likes = [email]
        else:
            evento.likes.append(email) 
    
        evento.put()
        
        return webapp2.redirect('/open/'+evento_id)
        
class Logout(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            logout = users.create_logout_url('/')
            return self.redirect(logout)
            
        
        