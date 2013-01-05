from google.appengine.ext import db

class Beer(db.Expando):
    '''Beer instances contain quality attributes about that sweet nectar from the earth.
    Every beer is named and has a certain style, description and other attributes.
    The system will keep a running tally of the local rating of a specific beer.
    '''
    name = db.StringProperty(required=True)
    style = db.StringProperty(required=True)
    abv = db.DecimalProperty(required=True)
    description = db.StringProperty(required=True)
    brewery = db.StringProperty(required=True)
    vintage = db.IntegerProperty()
    house_rating = db.RatingProperty()
    photo_url = db.LinkProperty()


