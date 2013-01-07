import webapp2
import webapp2_extras.routes as routes
from kegs import kegs

class Catch(webapp2.RequestHandler):
   def get(this):
      this.response.write('Wild: uri %s\n' % this.request.path_info)

app = webapp2.WSGIApplication([
                               routes.RedirectRoute('/keg/<keg_id>/', kegs.KegInfo, name='keg', strict_slash=True), 
                               routes.RedirectRoute('/kegs/', kegs.KegList, name='kegs', strict_slash=True),
                               webapp2.Route('/.*', Catch)],
                              debug=True)
