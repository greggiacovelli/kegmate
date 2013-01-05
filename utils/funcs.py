import datetime
from google.appengine.ext import db

def meta_ok():
    return {
           'code': 200,
           'message': 'Coolio'
           }

def convert_model(model, include_key=False):
    model_dict = {}
    if model:
        props = model.properties()
        for prop in props.keys():
            value = getattr(model, prop)
            if isinstance(value, datetime.datetime):
               value = value.ctime()
            if isinstance(value, db.GeoPt):
               model_dict['%s_latitude' % prop] = value.lat 
               model_dict['%s_longitude' % prop] = value.lon
               continue

            model_dict[prop] = value
            
        if model_dict and include_key:
            model_dict['id'] = model.key()
    return model_dict
