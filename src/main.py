from views import ShowEventos, CrearEvento, DeleteEvento, EditEvento
import webapp2

app = webapp2.WSGIApplication([
        ('/', ShowEventos), 
        ('/new', CrearEvento),
        ('/delete/([\d]+)', DeleteEvento),
        ('/edit/([\d]+)', EditEvento)
        ],
        debug=True)
