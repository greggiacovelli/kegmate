import webapp2
import webob.exc
from webapp2_extras import json
from utils.decorators import require
from utils import funcs
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
                {'meta': funcs.meta_ok(),
                 'user': funcs.convert_model(new_user)
                }
            ))

    def get(self, user_id):
        a_user = user.User.get_by_key_name(user_id)
        if not a_user:
           raise webob.exc.HTTPNotFound()

        self.response.write(
            json.json.dumps(
                {'meta': funcs.meta_ok(),
                 'user': funcs.convert_model(a_user)
                }
            ))

class PersonaInfo(webapp2.RequestHandler):

    def get(self, user_id):
        a_user = user.User.get_by_key_name(user_id)
        if not a_user:
           raise webob.exc.HTTPNotFound()
        personas = user.Persona.all().ancestor(a_user).run()
        if not personas:
           raise webob.exc.HTTPNotFound()
        personas = [funcs.convert_model(persona) for persona in personas]
        self.response.write(
            json.json.dumps(
               {'meta': funcs.meta_ok(),
                'personas' : personas
               }
            ))

    @require(query=['account_type', 'account_id'])
    def post(self, user_id):
        a_user = user.User.get_by_key_name(user_id)
        if not a_user:
           print 'OMG'
           return # raise webob.exc.HTTPNotFound()
        type = self.request.GET.get('account_type')
        id = self.request.GET.get('account_id')
        persona = user.Persona(key_name='%s-%s' % (a_user.key(), type), id=id, type=type, parent=a_user)
        persona.put()
        if not type in a_user.personas:
           a_user.personas.append(type)
           a_user.put()
        return webapp2.redirect_to('personas', user_id=user_id)

