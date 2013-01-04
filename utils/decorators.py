from functools import wraps
from utils.exceptions import MissingParamException

def require(query=None, body=None):
    def decorator(func):
        @wraps(func) 
        def wrapper(self, *args, **kwargs):
            missing_body = []
            missing_queries = []
            if query:
                missing_queries = [param for param in query if not param in self.request.GET]
            if body:
	        missing_body = [param for param in body if not param in self.request.POST]

            if missing_body or missing_queries:
               raise MissingParamException(query_params=missing_queries, body_params=missing_body)
            return func(self, *args, **kwargs)
        return wrapper
    return decorator
