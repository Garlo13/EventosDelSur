from views import ShowEventos #, NewAdd, DeleteAdd, EditAdd
import webapp2

app = webapp2.WSGIApplication([
        ('/', ShowEventos), 
#        ('/new', NewAdd), 
#        ('/edit/([\d]+)', EditAdd),
#        ('/delete/([\d]+)', DeleteAdd),
        ],
        debug=True)
