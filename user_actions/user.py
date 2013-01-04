import webapp2
from webapp2_extras import json
from utils.decorators import require
from models import user
class UserInfo(webapp2.RequestHandler):

    @require(query=['name'])
    def post(self, user_id):
        name = self.request.GET.get('name')
        new_user = user.User(key_name=user_id, user_name=name)
        new_user.put()
	props = new_user.properties()
        
        self.response.write(
            json.json.dumps(
                {'meta': 200,
                 'user': convert_user(new_user)
                }
            ))

    def get(self, user_id):
        a_user = user.User.get_by_key_name(user_id)
        self.response.write(
            json.json.dumps(
                {'meta': 200,
                 'user': convert_user(a_user)
                }
            ))

class PersonaInfo(webapp2.RequestHandler):

    def get(self, user_id):
        self.response.write('YAY')


def convert_user(user, include_key=False):
    user_dict = {}
    if user:
        props = user.properties()
        for prop in props.keys():
            user_dict[prop] = getattr(user, prop)
        if user_dict and include_key:
            user_dict['id'] = user.key()
    return user_dict

