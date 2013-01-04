from google.appengine.ext import db

class User(db.Model):

   user_name = db.StringProperty(required=True)
   personas = db.StringListProperty()

class Persona(db.Expando):

   id = db.StringProperty(required=True)
   type = db.StringProperty(required=True)
   auth_token = db.StringProperty()


