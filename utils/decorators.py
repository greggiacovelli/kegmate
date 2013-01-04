from functools import wraps
import webapp2

def require(query=None, body=None):
    def decorator(func):
        @wraps(func) 
        def wrapper(self, *args, **kwargs):
            if query:
                missing_queries = [param for param in params if param in self.response.GET]
            if body:
	        missing_body = [param for param in params if param in self.response.POST]

            if missing_body or missing_queries:
               raise webapp2.HttpException('400 - missing params body=%s, query=%s' % (missing_body, missing_queries))
            return func(self, *args, **kwargs)
        return wrapper
    return decorator
