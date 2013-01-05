from google.appengine.ext import db

class Tap(db.Expando):

    geo_location = db.GeoPtProperty(required=True)
    photo_url = db.LinkProperty()
    time_created = db.DateTimeProperty(auto_now_add=True)
    time_modified = db.DateTimeProperty(auto_now=True)
