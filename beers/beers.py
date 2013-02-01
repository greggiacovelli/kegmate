from google.appengine.ext import db
import webapp2
import webob.exc
from webapp2_extras import json
from models import Beer
from utils import funcs
from utils.decorators import require
from utils.exceptions import Conflict, InvalidParameterException

class BeerInfo(webapp2.RequestHandler):

    def get_beer_or_bust(self, beer_id):
        beer = Beer.get_by_key_name(beer_id)
        if not beer:
           beer = Beer.get(beer_id)
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
        beer.brewery = self.request.params.get('brewery', beer.brewery)
        beer.description = self.request.params.get('description', beer.description)
        beer.photo_url = self.request.params.get('photo_url', beer.photo_url)
        beer.style = self.request.params.get('style', beer.style)
        beer.abv = self.request.params.get('abv', beer.abv)
        beer.vintage = self.request.params.get('vintage', beer.vintage)
        if 'house_rating' in self.request.params and 'force' in self.request.GET:
            beer.house_rating = self.request.params['house_rating']
        beer.put()
        webapp2.redirect_to('beer', beer_id=beer_id)

class BeerList(webapp2.RequestHandler):

    def get(self):
       full = self.request.GET.get('full', False)
       limit = self.request.params.get('limit', 20)
       offset = self.request.params.get('offset', 0)
       all_beers = Beer.all(keys_only=not full)
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

    @require(params=['name', 'description', 'abv', 'brewery', 'style'])
    def post(self):
       name = self.request.params['name']
       description = self.request.params['description']
       style = self.request.params['style']
       abv = float(self.request.params['abv'])
       brewery = self.request.params['brewery']
       if Beer.get_by_key_name(name):
          raise Conflict(name, webapp2.uri_for('beer', beer_id=name))
       new_beer = Beer(key_name=name, style=style, abv=abv, description=description,
				brewery=brewery)
       if 'vintage' in self.request.params:
          new_beer.vintage = int(self.request.get('vintage'))
       if 'photo_url' in self.request.params:
          new_beer.photo_url = photo_url
       new_beer.put()
       webapp2.redirect_to('beer', beer_id=name)
