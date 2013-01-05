from google.appengine.ext import db

class Keg(db.Model):
    '''Keg instances serve as inventory for beer. These should be thought
    of the childen of beer. So every keg is of a specific beer type and can track
    how much of it is left and how much it can hold to begin with.
    '''
    capacity_liters = db.DecimalProperty(required=True)
    amount_left_liter = db.DecimalProperty()
    time_installed = db.DateTimeProperty(auto_add_now=True)
    time_modified = db.DateTimeProperty(auto_now=True)
