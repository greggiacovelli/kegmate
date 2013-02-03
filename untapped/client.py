
import httplib
import urllib
import json

class Client(object):

    _API_KEY = None
    _SECRET = None
    __API_HOST = 'api.untappd.com'
    __BASE_PATH = '/v4'

    def __init__(self, api_key, client_secret, *args, **kwargs):
        self._API_KEY = api_key
        self._SECRET = client_secret
        self.http = httplib.HTTPConnection(self.__API_HOST) 


    def make_request(self, endpoint, params, method='GET', access_token=None):
        query = {}
        if access_token is None:
           query ['client_id'] = self._API_KEY
           query ['client_secret'] = self._SECRET
        else:
           query ['access_token'] = access_token

        query.update(params)
        self.http.request(method, '%s/%s?%s' % (self.__BASE_PATH, endpoint, urllib.urlencode(query)))
        response = self.http.getresponse()
        status = response.status
        body = response.read()
        if status == 200:
           body = json.loads(body)
        return body

