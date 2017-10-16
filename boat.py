#CS496 Mobile and Web development HW3
# Cord Meados 2017

#-----------------------------------
#Boat Class and handler for main.py
#-----------------------------------

# [START imports]
from google.appengine.ext import ndb
import webapp2
import json
from slip import Slip

#Boats
class Boat(ndb.Model):
	name = ndb.StringProperty(required=True)
	type = ndb.StringProperty(required=True)
	length = ndb.IntegerProperty(required=True)
	at_sea = ndb.BooleanProperty(default=True)
	
class BoatHandler(webapp2.RequestHandler):
	def get(self, id=None):
		#if there is an id, respond with boat info corresponding to that id.
		#else, give a body response saying your're at the boathandler page
		if id:
			b = ndb.Key(urlsafe=id).get() #get the object from the database
			b_d = b.to_dict() #turn b object (boat) into a dictionary
			b_d['self'] = "/boat/" + id
			self.response.write(json.dumps(b_d))
		else:
			boat_dict = [] #dictionary to store boats in
			for b in Boat.query().fetch(): #fetch all boats from the database
				b_d = b.to_dict() #turn each boat instance into a dictionary
				b_d['self'] = '/boat/' + b.key.urlsafe() #add a "self" link to each boat dictionary
				boat_dict.append(b_d) #save boat dictionary in larger dictionary
			self.response.write(json.dumps(boat_dict)) #return boats with links to themselves.
		
		
	def post(self):
		#Create parent key so we can have a boat tree
		parent_key = ndb.Key(Boat, "parent_boat")
		#get json data from post, then use "loads" to turn json into object. assign to boat_data.
		boat_data = json.loads(self.request.body)
		
		#check if required data is good. If not throw bad data error or don't input data.
		#if good add data to new_boat
		if isinstance(boat_data['name'], basestring) == False:
			webapp2.abort(400,"Bad user input. Give json string with 'name', 'type', and 'length'")
		new_boat = Boat(name=boat_data['name'], parent=parent_key) #add required data
		if isinstance(boat_data.get('type', None), basestring) == False:
			webapp2.abort(400,"Bad user input. Give json string with 'name', 'type', and 'length'")
		new_boat.type = boat_data['type']
		if isinstance(boat_data.get('length', None), int) == False:
			webapp2.abort(400,"Bad user input. Give json string with 'name', 'type', and 'length'")
		new_boat.length = boat_data['length']
		
		#put boat object on database
		new_boat.put()
		
		#provide link to new boat object and return data for error testing
		boat_dict = new_boat.to_dict()
		boat_dict['self'] = '/boat/' + new_boat.key.urlsafe()
		self.response.write(json.dumps(boat_dict))
		
		

	def patch(self, id=None):
		if id:
			b = ndb.Key(urlsafe=id).get() #get the object instance from the database
			if self.request.body: #check if user sent data. If not, abort error 404
				new_data = json.loads(self.request.body)
			else:
				webapp2.abort(400,"Bad user input")
			
			#replace data if it is there.
			if isinstance(new_data.get('name', None), basestring): 
				b.name = new_data['name']
			if isinstance(new_data.get('type', None), basestring):
				b.type = new_data['type']
			if isinstance(new_data.get('length', None), int):
				b.length = new_data['length']
			
			b.put() #put new info on database
			
			b_d = b.to_dict() #debugging
			self.response.write(json.dumps(b_d)) #debugging
		else:
			self.response.write("patch to BoatHandler") #debugging

			
			
	def put(self, id=None):
		if id:
			b = ndb.Key(urlsafe=id).get() #get the object instance from the database
			if self.request.body: #check if user sent data. If not, abort error 404
				new_data = json.loads(self.request.body)
			else:
				webapp2.abort(400,"Bad user input")
			
			#check that all data is there
			if isinstance(new_data.get('name', None), basestring) == False:
				webapp2.abort(400,"Missing name")
			if isinstance(new_data.get('type', None), basestring) == False:
				webapp2.abort(400,"Missing type")
			if isinstance(new_data.get('length', None), int) == False:
				webapp2.abort(400,"missing length")
			
			#replace all data
			b.name = new_data['name']
			b.type = new_data['type']
			b.length = new_data['length']
			
			b.put() #put new info on database
			
			b_d = b.to_dict() #debugging
			self.response.write(json.dumps(b_d)) #debugging
			
		else:
			self.response.write("put to BoatHandler") #debugging
	
	
	def delete(self, id=None):
		#if there is an id, delete it
		if id:
			b = ndb.Key(urlsafe=id).get() #get the boat object from the database
			if b.at_sea == False:
				for slip in Slip.query().fetch(): #fetch all slips from the database
					if slip.current_boat == str(id):
						s = slip
				#add departure history to slip
				departure = "departed boat: " + str(s.current_boat) + ", departure date: deleted"
				s.departure_history.append(departure)
				s.current_boat = None
				s.arrival_date = None
				s.put()

			ndb.Key(urlsafe=id).delete()
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
