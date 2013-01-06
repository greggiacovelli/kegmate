import webob.exc
from webapp2_extras import json

class KegMateException(webob.exc.WSGIHTTPException):

     code = 200

     def __init__(self, **kw):
        webob.exc.WSGIHTTPException.__init__(self, **kw)
        self._make_body()

     def update_payload(self, payload):
        pass

     def _make_body(self):
       self.content_type='text/plain'
       payload = {
           'code': self.code,
           'message': self.message
       }
       self.update_payload(payload)
       self.body = json.json.dumps({'meta': payload})

       
class InvalidParameterException(KegMateException):

    meta_code = 401
    message = 'One of the passed parameters is invalid'

    def __init__(self, description=None, param=None, value=None):
       self.__description = description
       self.__param = param
       self.__value = value
       KegMateException.__init__(self)

    def update_payload(self, payload):
       payload['value'] = self.__value
       payload['param'] = self.__param
       payload['descritpion'] = self.__description

  
class MissingParamException(KegMateException):

    meta_code = 400
    message = 'Missing Parameters needed for request'

    def __init__(self, message=None, query_params=None, body_params=None):
        if message:
            self.message = message
        self.missing_query = query_params
        self.missing_body = body_params
        KegMateException.__init__(self)
      
    def update_payload(self, payload):
        if self.missing_query:
            payload['missing_query'] = self.missing_query
        if self.missing_body:
            payload['missing_body'] = self.missing_body

class Conflict(KegMateException):

    meta_code = 409
    message = 'There was a conflict with another resource'

    def __init__(self, name, location, *args, **kwargs):
       self.__name = name
       self.__location = location
       KegMateException.__init__(self, *args, **kwargs)

    def update_payload(self, payload):
       payload['name'] = self.__name
       payload['location'] = self.__location
