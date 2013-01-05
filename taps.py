#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import webapp2_extras.routes as routes
from taps_actions import taps

class Catch(webapp2.RequestHandler):
   def get(this):
      this.response.write('Wild: uri %s\n' % this.request.path_info)

app = webapp2.WSGIApplication([
                               routes.RedirectRoute('/tap/<tap_id>/', taps.TapInfo, name='tap', strict_slash=True), 
                               routes.RedirectRoute('/taps/', taps.TapList, name='taps', strict_slash=True),
                               webapp2.Route('/.*', Catch)],
                              debug=True)
