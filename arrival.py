#CS496 Mobile and Web development HW3
# Cord Meados 2017

#-----------------------------------
#arrival handler for main.py
#-----------------------------------

# [START imports]
from google.appengine.ext import ndb
import webapp2
import json
from boat import Boat
from slip import Slip

class ArrivalHandler(webapp2.RequestHandler):
	def get(self, id=None):
		s = ndb.Key(urlsafe=id).get() #get the slip object from the database
		#check if slip has a boat
		if s.current_boat == None:
			webapp2.abort(200,"Slip is empty.")
		
		b = ndb.Key(urlsafe=s.current_boat).get()
		self.response.write(json.dumps(b.to_dict()))
		#This is the get to ArrivalHandler. 
		#To add a boat, post to ArrivalHandler with the boat key in a json body with name 'key' and arrival date with name 'arrival'
		
	def post(self, id=None):
		s = ndb.Key(urlsafe=id).get() #get the slip object from the database
		boat_data = json.loads(self.request.body) #get key from json body for arriving boat
		b = ndb.Key(urlsafe=boat_data["key"]).get() #get the object from the database
		
		if s.current_boat != None:
			webapp2.abort(403,"Slip is already occupied.")
		
		#change data
		s.arrival_date = boat_data["arrival"]
		s.current_boat = boat_data["key"]
		b.at_sea = False
		
		s.put()
		b.put()
		

		
		
		
		
		