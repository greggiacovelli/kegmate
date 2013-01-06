from google.appengine.ext import db
import webapp2
import webob.exc
from webapp2_extras import json
from models import taps
from models import kegs
from utils import funcs
from utils.decorators import require
from utils.exceptions import Conflict, InvalidParameterException

class TapInfo(webapp2.RequestHandler):

    def get_tap_or_bust(self, tap_id):
        tap = taps.Tap.get_by_key_name(tap_id)
        if not tap:
           tap = taps.Tap.get(tap_id)
        if not tap:
           raise webob.exc.HTTPNotFound()
        return tap

    def get(self, tap_id, **kwargs):
        self.response.write(json.json.dumps(
            {'meta' : funcs.meta_ok(),
             'tap' : funcs.convert_model(self.get_tap_or_bust(tap_id))
            }
         ))

    def post(self, tap_id):
        tap = self.get_tap_or_bust(tap_id)
        tap.geo_location.lat = self.request.params.get('latitude', tap.geo_location.lat)
        tap.geo_location.lon = self.request.params.get('longitude', tap.geo_location.lon)
        tap.photo_url = self.request.params.get('photo_url', tap.photo_url)
        keg_id = self.request.params.get('keg')
        if keg_id:
            keg = kegs.Keg.get_by_key_name(keg_id)
            if not keg:
                raise InvalidParameterException(param='keg', value=keg_id, description='The given keg could not be located')
            if keg.empty():
                raise InvalidParameterException(param='keg', value=keg_id, description='The given keg is reported empty')
            query = Tap.all(keys_only=True).filter('keg =', keg)
            keys = [key for key in query]
            if keys and not tap.key() in keys:
                raise InvalidParameterException(param='keg', value=keg_id, description='The given keg is already associated to another tap')
            keg.put()
            tap.keg = keg.key()
        tap.put()
        webapp2.redirect_to('tap', tap_id=tap_id)

class TapList(webapp2.RequestHandler):

    def get(self):
       full = self.request.GET.get('full', False)
       limit = self.request.params.get('limit', 20)
       offset = self.request.params.get('offset', 0)
       all_taps = taps.Tap.all(keys_only=not full)
       total = all_taps.count(read_policy=db.EVENTUAL_CONSISTENCY, deadline=5)
       payload = [a_tap for a_tap in all_taps.run(offset=offset, limit=min(limit, total))]
       if not payload:
          raise webob.exc.HTTPNotFound()
       data = {}
       if not full:
          data['taps'] = [webapp2.uri_for('tap', tap_id=tap.name()) for tap in all_taps]
       else:
          data['taps'] = [funcs.convert_model(tap) for tap in all_taps]
       data['meta'] = funcs.meta_ok()
       self.response.write(json.json.dumps(data))

    @require(params=['name', 'latitude', 'longitude'])
    def post(self):
       name = self.request.params['name']
       if taps.Tap.get_by_key_name(name):
          raise Conflict(name, webapp2.uri_for('tap', tap_id=name))
       latitude = self.request.params['latitude']
       longitude = self.request.params['longitude']
       a_tap = taps.Tap(key_name=name, geo_location=db.GeoPt(latitude, longitude))
       a_tap.put()
       webapp2.redirect_to('tap', tap_id=name)
