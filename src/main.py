from views import ShowEventos, CrearEvento, DeleteEvento, EditEvento, OpenEvento, Logout, LikeEvento
import webapp2

app = webapp2.WSGIApplication([
        ('/', ShowEventos), 
        ('/new', CrearEvento),
        ('/delete/([\d]+)', DeleteEvento),
        ('/edit/([\d]+)', EditEvento),
        ('/like/([\d]+)', LikeEvento),
        ('/open/([\d]+)', OpenEvento),
        ('/logout', Logout)
        ],
        debug=True)
