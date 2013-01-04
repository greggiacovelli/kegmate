import webapp2
from utils import require
import models
class RegisterUser(webapp2.RequestHandler):

    @require(query=['user_id', 'name'])
    def get(self):
        self.response.out.write('Hello world!')

