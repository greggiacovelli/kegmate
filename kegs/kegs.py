from google.appengine.ext import db
import webapp2
import webob.exc
from webapp2_extras import json
from models import kegs
from models import kegs
from utils import funcs
from utils.decorators import require
from utils.exceptions import Conflict, InvalidParameterException

class KegInfo(webapp2.RequestHandler):

    def get_keg_or_bust(self, keg_id):
        keg = kegs.Keg.get_by_key_name(keg_id)
        if not keg:
           keg = kegs.Keg.get(keg_id)
        if not keg:
           raise webob.exc.HTTPNotFound()
        return keg

    def get(self, keg_id, **kwargs):
        self.response.write(json.json.dumps(
            {'meta' : funcs.meta_ok(),
             'keg' : funcs.convert_model(self.get_keg_or_bust(keg_id))
            }
         ))

    def post(self, keg_id):
        keg = self.get_keg_or_bust(keg_id)
        keg.geo_location.lat = self.request.params.get('latitude', keg.geo_location.lat)
        keg.geo_location.lon = self.request.params.get('longitude', keg.geo_location.lon)
        keg.photo_url = self.request.params.get('photo_url', keg.photo_url)
        keg_id = self.request.params.get('keg')
        if keg_id:
            keg = kegs.Keg.get_by_key_name(keg_id)
            if not keg:
                raise InvalidParameterException(param='keg', value=keg_id, description='The given keg could not be located')
            if keg.empty():
                raise InvalidParameterException(param='keg', value=keg_id, description='The given keg is reported empty')
            query = Keg.all(keys_only=True).filter('keg =', keg)
            keys = [key for key in query]
            if keys and not keg.key() in keys:
                raise InvalidParameterException(param='keg', value=keg_id, description='The given keg is already associated to another keg')
            keg.put()
            keg.keg = keg.key()
        keg.put()
        webapp2.redirect_to('keg', keg_id=keg_id)

class KegList(webapp2.RequestHandler):

    def get(self):
       full = self.request.GET.get('full', False)
       limit = self.request.params.get('limit', 20)
       offset = self.request.params.get('offset', 0)
       all_kegs = kegs.Keg.all(keys_only=not full)
       total = all_kegs.count(read_policy=db.EVENTUAL_CONSISTENCY, deadline=5)
       payload = [a_keg for a_keg in all_kegs.run(offset=offset, limit=min(limit, total))]
       if not payload:
          raise webob.exc.HTTPNotFound()
       data = {}
       if not full:
          data['kegs'] = [webapp2.uri_for('keg', keg_id=keg.name()) for keg in all_kegs]
       else:
          data['kegs'] = [funcs.convert_model(keg) for keg in all_kegs]
       data['meta'] = funcs.meta_ok()
       self.response.write(json.json.dumps(data))

    @require(params=['name', 'latitude', 'longitude'])
    def post(self):
       name = self.request.params['name']
       if kegs.Keg.get_by_key_name(name):
          raise Conflict(name, webapp2.uri_for('keg', keg_id=name))
       latitude = self.request.params['latitude']
       longitude = self.request.params['longitude']
       a_keg = kegs.Keg(key_name=name, geo_location=db.GeoPt(latitude, longitude))
       a_keg.put()
       webapp2.redirect_to('keg', keg_id=name)
