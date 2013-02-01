#!/usr/bin/python

import optparse
import httplib
import urllib
import sys
import json

if __name__ == '__main__':
   parser = optparse.OptionParser(usage='usage: %prog [options] host')
   parser.add_option('--mode', type='choice', choices=['add', 'update'], default='add')
   parser.add_option('--name', help='Unique name of beer')
   parser.add_option('--description', help='Description of the beer')
   parser.add_option('--style', help='Style of beer')
   parser.add_option('--abv', type='float', help='Alcohol By Volume (%)')
   parser.add_option('--brewery', help='The name of the brewery that makes such a beer')
   parser.add_option('--photo_url', help='A Url to a photo of the beer label')
   parser.add_option('--vintage', type='int', help='Some beers are vintage, you can specify an optional one here')
   options, args = parser.parse_args()

   if not args:
      parser.error('Host argument is required')
   host = args[len(args)-1]

   http = httplib.HTTPConnection(host)
   path = '/beers/' if options.mode == 'add' else '/beer/%s/' % urllib.quote_plus(options.name)
   data = {
       'name': options.name,
       'description': options.description,
       'style': options.style,
       'abv': options.abv,
       'brewery': options.brewery,
   }
   if options.vintage:
     data['vintage'] = options.vintage
   if options.photo_url:
     data['photo_url'] = options.photo_url

   http.request('POST', path, urllib.urlencode(data))
   response = http.getresponse()
   status = response.status
   reason = response.reason
   response_data = response.read()

   print status, reason, response_data

   if status >= 400 and status < 500:
      http.request('GET', '/beer/%s' % urllib.quote_plus(options.name),)
      response = http.getresponse()
      print 'Conflict for that beer, maybe you want to update the beer. Try --mode=update.  %s' % response_data

