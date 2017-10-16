#CS496 Mobile and Web development HW3
# Cord Meados 2017

#-----------------------------------
#Slip Class and handler for main.py
#-----------------------------------

# [START imports]
from google.appengine.ext import ndb
import webapp2
import json


#slips
class Slip(ndb.Model):
	number = ndb.IntegerProperty(required=True)
	current_boat = ndb.StringProperty()
	arrival_date = ndb.StringProperty()
	departure_history = ndb.StringProperty(repeated=True)


class SlipHandler(webapp2.RequestHandler):
	def get(self, id=None):
		#if there is an id, respond with slip info corresponding to that id.
		#else, give a body response saying your're at the sliphandler page
		if id:
			s = ndb.Key(urlsafe=id).get() #get the object from the database
			s_d = s.to_dict() #turn s object (slip) into a dictionary
			s_d['self'] = "/slip/" + id
			self.response.write(json.dumps(s_d))
		else: 
			slip_dict = [] #dictionary to store slips in
			for s in Slip.query().fetch(): #fetch all slips from the database
				s_d = s.to_dict() #turn each slip instance into a dictionary
				s_d['self'] = '/slip/' + s.key.urlsafe() #add a "self" link to each slip dictionary
				slip_dict.append(s_d) #save slip dictionary in larger dictionary
			self.response.write(json.dumps(slip_dict)) #return slips with links to themselves.


	def post(self):
		#Create parent key so we can have a slip tree
		parent_key = ndb.Key(Slip, "parent_slip")
		#get json data from post, then use "loads" to turn json into object. assign to slip_data.
		slip_data = json.loads(self.request.body)
		
		#check if required data is good. If not throw bad data error or don't input data.
		#if good add data to new_slip
		if (isinstance(slip_data['number'], int) == False):
			webapp2.abort(400,"Bad user input")
		new_slip = Slip(number=slip_data['number'], parent=parent_key) #add required data
		
		if str(Slip.query(Slip.number == new_slip.number).fetch()) == "[]":	 #check if number already exists
			new_slip.put() #put slip object on database
		else:
			webapp2.abort(400,"That slip number is already in use.")
				
		#provide link to new slip object and return data for error testing
		slip_dict = new_slip.to_dict()
		slip_dict['self'] = '/slip/' + new_slip.key.urlsafe()
		self.response.write(json.dumps(slip_dict))		
						
			
	def patch(self, id=None):
		if id:
			s = ndb.Key(urlsafe=id).get() #get the object instance from the database
			if self.request.body: #check if user sent data. If not, abort error 400
				new_data = json.loads(self.request.body)
			else:
				webapp2.abort(400,"Bad user input")
			
			#replace data if it is there.
			if isinstance(new_data.get('number', None), int): 
				new_slip_number = Slip(number=new_data['number'])
				if str(Slip.query(Slip.number == new_slip_number.number).fetch()) == "[]":
					s.number = new_slip_number.number
				else:
					webapp2.abort(400,"That slip number is already in use.")

			s.put() #put new info on database

		else:
			self.response.write("patch to SlipHandler") #debugging
			
			
	def put(self, id=None):
		if id:	
			s = ndb.Key(urlsafe=id).get() #get the object instance from the database
			if self.request.body: #check if user sent data. If not, abort error 400
				new_data = json.loads(self.request.body)
			else:
				webapp2.abort(400,"Bad user input")
			
			#replace data if it is there.
			if isinstance(new_data.get('number', None), int): 
				new_slip_number = Slip(number=new_data['number'])
				if str(Slip.query(Slip.number == new_slip_number.number).fetch()) == "[]":
					s.number = new_slip_number.number
				else:
					webapp2.abort(400,"That slip number is already in use.")

			s.put() #put new info on database

		else:
			elf.response.write("put to SlipHandler") #debugging
					
				
	def delete(self, id=None):
		#if there is an id, delete it
		if id:
			s = ndb.Key(urlsafe=id).get()
			if s.current_boat != None:
				b = ndb.Key(urlsafe=s.current_boat).get() #get boat that is in the slip
				b.at_sea = True
				b.put()
			ndb.Key(urlsafe=id).delete()			
			
			
			
			
			
			
			
			
			
			
			
			
			