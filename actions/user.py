import webapp2
import webapp2_extras.routes as routes
from users import user

class Catch(webapp2.RequestHandler):
   def get(this):
      this.response.write('Wild: uri %s\n' % this.request.path_info)

app = webapp2.WSGIApplication([routes.PathPrefixRoute('/user', [
                               routes.RedirectRoute('/<user_id>/', user.UserInfo, name='user', strict_slash=True), 
                               routes.RedirectRoute('/<user_id>/personas/', user.PersonaInfo, name='personas', strict_slash=True),
                               webapp2.Route('/.*', Catch)])],
                              debug=True)
