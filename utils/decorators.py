from functools import wraps
from utils.exceptions import MissingParamException

def require(query=None, body=None, params=None):
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

            missing_params = []
            if params:
               missing_params = [param for param in params if not param in self.request.params]

            if missing_params:
               raise MissingParamException(query_params=missing_params, body_params=missing_params)

            return func(self, *args, **kwargs)

        return wrapper

    return decorator
