#CS496 Mobile and Web development HW3
# Cord Meados 2017

#-----------------------------------
#at_sea handler for main.py
#-----------------------------------

# [START imports]
from google.appengine.ext import ndb
import webapp2
import json
from boat import Boat
from slip import Slip

class AtSeaHandler(webapp2.RequestHandler):
	def post(self, id=None):
		if id:
			depart_date = json.loads(self.request.body) #get departure date from json body for departing boat
			b = ndb.Key(urlsafe=id).get() #get the boat object from the database
			if b.at_sea == True:
				webapp2.abort(400,"Boat is not in a slip.")
			for slip in Slip.query().fetch(): #fetch all slips from the database
				if slip.current_boat == str(id):
					s = slip
			
			#check data is correct type
			if isinstance(depart_date['depart'], basestring) == False:
				webapp2.abort(400,"Bad user input. Give json string with 'depart' and 'date' where date is a string")


			
			#add departure history to slip
			departure = "departed boat: " + str(s.current_boat) + ", departure date: " + str(depart_date["depart"])
			s.departure_history.append(departure)
			
			#update data
			s.current_boat = None
			s.arrival_date = None
			b.at_sea = True
			
			#update server
			s.put()
			b.put()
			
		
		

		
		