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

# this is some template "hello world" code

import webapp2
import BlockModels

from google.appengine.ext import db

# import the date module
from datetime import *
import datetime

# imports jinja2 and sets it up
import jinja2
import os


jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

# hardcode in the current block

class CST(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=-6)

    def tzname(self, dt):
        return "US/Central"

    def dst(self, dt):
        return timedelta(0)
        
cst = CST()

class MainHandler(webapp2.RequestHandler):
    
    def get(self):
        
        def checkDay(wday, now, sday, eday):
            q = BlockModels.Entry.all()
            q.filter("day =", wday)
            for block in q.run():
                name = block.block
                if block.sTime < now and block.eTime > now:
                    cname = name
                    break
                # elif sday < now and eday > now:
                #     return "Before/Between"
                elif eday.hour < now.hour or sday.hour > now.hour:
                    cname = "School is Out"
                    break
                elif wday > 5 or wday == 0:
                    cname = "No School"
                    break
                else:
                    cname = "Before/Between"
            return cname
        
        tlocal = datetime.datetime.now(cst)
        EndDay = datetime.time(14, 00, 00)
        StartDay = datetime.time(7, 50, 00)
        now = datetime.time(tlocal.hour, tlocal.minute, tlocal.second)
        formNow = datetime.datetime.strftime(tlocal, "%A, %b %d %I:%M:%S %p")
      
        # determine the current week day
        today = date.today()
        current_weekday = today.isoweekday()
        # one thing I'm not sure about is whether the above code needs to go in the request handler (calculated at very page load)
        
        # write variables to template
        
            
        current_block = checkDay(current_weekday, now, StartDay, EndDay)
        
        template_values = {
            'localtime': formNow,
            'block': current_block
        }

        template = jinja_environment.get_template('frontendproto.html')
        self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
