from google.appengine.ext import ndb
    
class Usuario(ndb.Model):
    nombre = ndb.StringProperty()
    email = ndb.StringProperty()

class Comentario(ndb.Model):
    autor = ndb.StructuredProperty(Usuario)
    comentario = ndb.StringProperty()

class Eventos(ndb.Model):
    nombre = ndb.StringProperty()
    descripcion = ndb.StringProperty()
    direccion = ndb.StringProperty()
    creador = ndb.StructuredProperty(Usuario)
    latitud = ndb.FloatProperty()
    longitud = ndb.FloatProperty()
    fechaInicio = ndb.DateTimeProperty()
    fechaFin = ndb.DateTimeProperty()
    likes = ndb.StructuredProperty(Usuario, repeated=True)
    comentarios = ndb.StructuredProperty(Comentario, repeated=True)
    
    
    