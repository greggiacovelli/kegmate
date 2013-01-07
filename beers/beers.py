from google.appengine.ext import db
import webapp2
import webob.exc
from webapp2_extras import json
from models import beers
from models import beers
from utils import funcs
from utils.decorators import require
from utils.exceptions import Conflict, InvalidParameterException

class BeerInfo(webapp2.RequestHandler):

    def get_beer_or_bust(self, beer_id):
        beer = beers.Beer.get_by_key_name(beer_id)
        if not beer:
           beer = beers.Beer.get(beer_id)
        if not beer:
           raise webob.exc.HTTPNotFound()
        return beer

    def get(self, beer_id, **kwargs):
        self.response.write(json.json.dumps(
            {'meta' : funcs.meta_ok(),
             'beer' : funcs.convert_model(self.get_beer_or_bust(beer_id))
            }
         ))

    def post(self, beer_id):
        beer = self.get_beer_or_bust(beer_id)
        beer.geo_location.lat = self.request.params.get('latitude', beer.geo_location.lat)
        beer.geo_location.lon = self.request.params.get('longitude', beer.geo_location.lon)
        beer.photo_url = self.request.params.get('photo_url', beer.photo_url)
        beer_id = self.request.params.get('beer')
        if beer_id:
            beer = beers.Beer.get_by_key_name(beer_id)
            if not beer:
                raise InvalidParameterException(param='beer', value=beer_id, description='The given beer could not be located')
            if beer.empty():
                raise InvalidParameterException(param='beer', value=beer_id, description='The given beer is reported empty')
            query = Beer.all(keys_only=True).filter('beer =', beer)
            keys = [key for key in query]
            if keys and not beer.key() in keys:
                raise InvalidParameterException(param='beer', value=beer_id, description='The given beer is already associated to another beer')
            beer.put()
            beer.beer = beer.key()
        beer.put()
        webapp2.redirect_to('beer', beer_id=beer_id)

class BeerList(webapp2.RequestHandler):

    def get(self):
       full = self.request.GET.get('full', False)
       limit = self.request.params.get('limit', 20)
       offset = self.request.params.get('offset', 0)
       all_beers = beers.Beer.all(keys_only=not full)
       total = all_beers.count(read_policy=db.EVENTUAL_CONSISTENCY, deadline=5)
       payload = [a_beer for a_beer in all_beers.run(offset=offset, limit=min(limit, total))]
       if not payload:
          raise webob.exc.HTTPNotFound()
       data = {}
       if not full:
          data['beers'] = [webapp2.uri_for('beer', beer_id=beer.name()) for beer in all_beers]
       else:
          data['beers'] = [funcs.convert_model(beer) for beer in all_beers]
       data['meta'] = funcs.meta_ok()
       self.response.write(json.json.dumps(data))

    @require(params=['name', 'latitude', 'longitude'])
    def post(self):
       name = self.request.params['name']
       if beers.Beer.get_by_key_name(name):
          raise Conflict(name, webapp2.uri_for('beer', beer_id=name))
       latitude = self.request.params['latitude']
       longitude = self.request.params['longitude']
       a_beer = beers.Beer(key_name=name, geo_location=db.GeoPt(latitude, longitude))
       a_beer.put()
       webapp2.redirect_to('beer', beer_id=name)
