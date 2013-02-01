from google.appengine.ext import db

class Beer(db.Expando):
    '''Beer instances contain quality attributes about that sweet nectar from the earth.
    Every beer is named and has a certain style, description and other attributes.
    The system will keep a running tally of the local rating of a specific beer.
    '''
    style = db.StringProperty(required=True)
    abv = db.FloatProperty(required=True)
    description = db.StringProperty(required=True)
    brewery = db.StringProperty(required=True)
    vintage = db.IntegerProperty()
    house_rating = db.RatingProperty()
    photo_url = db.LinkProperty()


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

class User(db.Model):

   user_name = db.StringProperty(required=True)
   personas = db.StringListProperty()


class Persona(db.Expando):

   id = db.StringProperty(required=True)
   type = db.StringProperty(required=True)
   time_created = db.DateTimeProperty(auto_now_add=True)
   time_modified = db.DateTimeProperty(auto_now=True)
   auth_token = db.StringProperty()

class Pour(db.Model):
    '''A Pour is a record that a given user poured a given amount of a given beer at a specific tap at a certain time
    '''
    user = db.ReferenceProperty(required=True, reference_class=User)
    beer = db.ReferenceProperty(required=True, reference_class=Beer)
    tap = db.ReferenceProperty(required=True, reference_class=Tap)
    rating = db.RatingProperty()
    time_created = db.DateTimeProperty(auto_now_add=True)

