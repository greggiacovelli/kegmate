import webapp2
import webapp2_extras.routes as routes
from beers import beers

class Catch(webapp2.RequestHandler):
   def get(this):
      this.response.write('Wild: uri %s\n' % this.request.path_info)

app = webapp2.WSGIApplication([
                               routes.RedirectRoute('/beer/<beer_id>/', beers.BeerInfo, name='beer', strict_slash=True), 
                               routes.RedirectRoute('/beers/', beers.BeerList, name='beers', strict_slash=True),
                               webapp2.Route('/.*', Catch)],
                              debug=True)
