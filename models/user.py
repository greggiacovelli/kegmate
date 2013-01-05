from google.appengine.ext import db

class User(db.Model):

   user_name = db.StringProperty(required=True)
   personas = db.StringListProperty()

class Persona(db.Expando):

   id = db.StringProperty(required=True)
   type = db.StringProperty(required=True)
   time_created = db.DateTimeProperty(auto_now_add=True)
   time_modified = db.DateTimeProperty(auto_now=True)
   auth_token = db.StringProperty()


