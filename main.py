#CS496 Mobile and Web development HW3
# Cord Meados 2017

# [START imports]
from google.appengine.ext import ndb
import webapp2
import json

from boat import Boat, BoatHandler
from slip import Slip, SlipHandler
from arrival import ArrivalHandler
from atSea import AtSeaHandler




# [START main_page]
class MainPage(webapp2.RequestHandler):
    def get(self):
		self.response.write("REST implementation main page")		
# [END main_page]


# [START app]

#allow patch() 
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
#end allow patch()

app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/boat', BoatHandler),
	('/slip', SlipHandler),
	('/boat/([\w-]+)/at_sea', AtSeaHandler),
	('/boat/([\w-]+)', BoatHandler),
	('/slip/([\w-]+)/arrival', ArrivalHandler),
	('/slip/([\w-]+)', SlipHandler),
	
	
], debug=True)
# [END app] 