import webapp2
from utils.decorators import require

class RegisterUser(webapp2.RequestHandler):

    @require(query=['user_id', 'name'])
    def get(self):
        self.response.out.write('Hello world!')

