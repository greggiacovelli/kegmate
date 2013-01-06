from google.appengine.ext import db

class Keg(db.Model):
    '''Keg instances serve as inventory for beer. These should be thought
    of the childen of beer. So every keg is of a specific beer type and can track
    how much of it is left and how much it can hold to begin with.
    '''
    capacity_liters = db.FloatProperty(required=True)
    amount_left_liter = db.FloatProperty()
    time_installed = db.DateTimeProperty(auto_now_add=True)
    time_modified = db.DateTimeProperty(auto_now=True)

    def is_empty():
        return amount_left_liter == 0
