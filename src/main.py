from views import ShowEventos, CrearEvento, DeleteEvento, EditEvento, OpenEvento, Logout
import webapp2

app = webapp2.WSGIApplication([
        ('/', ShowEventos), 
        ('/new', CrearEvento),
        ('/delete/([\d]+)', DeleteEvento),
        ('/edit/([\d]+)', EditEvento),
        ('/open/([\d]+)', OpenEvento),
        ('/logout', Logout)
        ],
        debug=True)
