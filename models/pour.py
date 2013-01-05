from google.appengine.ext import db

class Pour(db.Model):
    '''A Pour is a record that a given user poured a given amount of a given beer at a specific tap at a certain time
    '''
    user = db.ReferenceProperty(required=True, reference_class=User)
    beer = db.ReferenceProperty(required=True, reference_class=Beer)
    tap = db.ReferenceProperty(required=True, reference_class=Tap)
    rating = db.RatingProperty()
    time_created = db.DateTimeProperty(auto_add_now=True)


