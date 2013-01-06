import webapp2
import webapp2_extras.routes as routes
from taps import taps

class Catch(webapp2.RequestHandler):
   def get(this):
      this.response.write('Wild: uri %s\n' % this.request.path_info)

app = webapp2.WSGIApplication([
                               routes.RedirectRoute('/tap/<tap_id>/', taps.TapInfo, name='tap', strict_slash=True), 
                               routes.RedirectRoute('/taps/', taps.TapList, name='taps', strict_slash=True),
                               webapp2.Route('/.*', Catch)],
                              debug=True)
