import webob.exc
from webapp2_extras import json

class KegMateException(webob.exc.WSGIHTTPException):

     code = 200

     def __init__(self, **kw):
        webob.exc.WSGIHTTPException.__init__(self, **kw)
        self.make_body()

     def make_body(self):
       self.content_type='text/plain'
       payload = {
           'code': self.meta_code,
           'message': self.message,
           }

       if self.detail:
          payload['detail'] = self.detail
       
       self.body = json.json.dumps({'meta': payload})


class MissingParamException(KegMateException):

   meta_code = 400
   message = 'Missing Parameters needed for request'

   def __init__(self, message=None, query_params=None, body_params=None):
      if message:
           self.message = message
      
      if query_params or body_params:
           self.detail = 'Missing Query Params: %s, Missing Body Params: %s' % (query_params, body_params)

      KegMateException.__init__(self)
      
      
