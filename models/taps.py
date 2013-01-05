from google.appengine.ext import db

class Tap(db.Model):
    '''A Tap is a physical beer tap installation somewhere. Basically it thought of
    as the place you have a beer. Each Tap can have a keg installed. This keg contains
    the beer that will be rated whenever someone pours from the Tap instance
    '''

    geo_location = db.GeoPtProperty(required=True)
    photo_url = db.LinkProperty()
    time_created = db.DateTimeProperty(auto_now_add=True)
    time_modified = db.DateTimeProperty(auto_now=True)
    keg = db.ReferenceProperty(reference_class=Keg)
