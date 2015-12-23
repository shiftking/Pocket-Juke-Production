import endpoints

import os
import urllib
import operator

from operator import itemgetter
from google.appengine.api import users
from google.appengine.ext import ndb


"""Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""


import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote


package = 'pocket_juke'
#NDB data type user
class User(ndb.Model):
    """Sub Model representing the user"""

    user_id = ndb.StringProperty(indexed=True)
    party_key_id = ndb.StringProperty(indexed=True)

#NDB data type party
class Party(ndb.Model):
    """main model to represent a party"""
    party_creator = ndb.KeyProperty(User,indexed=True)
    party_name = ndb.StringProperty(indexed=True)
    code = ndb.StringProperty(indexed=False)
    attending = ndb.IntegerProperty()

#this represents the entity for housing the party name and code
class Party_class(messages.Message):
  """Greeting that stores a message."""
  name = messages.StringField(1, required=True)
  pass_code = messages.StringField(2, required=False)
  party_id = messages.StringField(3)
class
#this holsd the entity that is used for the response for successful/not succesful additcion of a party
class add_response(messages.Message):
    response = messages.StringField(1,required=True)


#this hold the list of parties that will be passed back to the user when the query for a name of a party is successful
class Party_list(messages.Message):
  """Collection of Parties."""
  Parties = messages.MessageField(Party_class,1,repeated=True)






@endpoints.api(name='pocket_juke_api', version='v1')
class PocketJukeAPI(remote.Service):
  """Pocket Juke API v1."""
 #method for getting a list of parties with a specific offset
  QUANTITY = endpoints.ResourceContainer(
      Party_class,
      offset=messages.IntegerField(4, variant=messages.Variant.INT32))
  @endpoints.method(QUANTITY,Party_list,
                    path='party_api/get_parties', http_method='POST',
                    name='pocket_juke.get_parties')
                    #currently searches partys by thier namespace
                    #will add options for user name and other atributes

  def get_parties(self, request):
      party_list = []
      #check if the offset is bigger that 10
      keywords = []
      keywords.append(request.name)
      que = Party.query(Party.party_name.IN(keywords))


      if(request.offset > 10):
          for party in que.fetch(10,offset=request.offset):
              party_list.append(Party_class(name= request.party_name))

          return Party_list(Parties = party_list)

        #if we are only pulling the first ten Parties
      else:

          #need to break the query up into
          for party in que.fetch(10):
              party_list.append(Party_class(name= party.party_name))
          return Party_list(Parties = party_list)
#method for adding a party
  @endpoints.method(Party_class,add_response,
                    path='party_api/add_party', http_method='POST',
                    name='pocket_juke.add_party')
  def add_party(self, request):
      #checks to see if the party is already in the database

      q = Party.query(Party.party_name == request.name)


     #query.filter("name ==",request.name);
      if  q.get() :
          return add_response(response="name already taken")
      else:
          user = users.get_current_user()
          #getting the user key to put in the new party as the creator
          user_key = User.query(User.user_id==user.user_id()).get(keys_only=True)
          new_party = Party(party_name = request.name,code = request.pass_code,party_creator = user_key)
          if(new_party.put()):
              return add_response(response="add successfully")
          else:
              return add_response(response="not added successfully")
  @endpoints.method(Party_class,add_response,
                    path='party_api/leave_party',http_method = 'GET',
                    name='pocket_juke.leave_party')
  def leave_party(self,request):
      user = users.get_current_user()
      active_user = User.query(User.user_id == user.user_id())
      active_user.party_key_id = None
      return add_response(response="Removed from the party")
#method for joining a party
  @endpoints.method(Party_class,add_response,
                      path='party_api/join_party',http_method='GET',
                      name='pocket_juke.join_party')
  def join_party(self, request):
      que = Party.query(Party.party_name == request.name).get(keys_only=True)

      if que.get():
            user = users.get_current_user()
            active_user = User.query(User.user_id == user.user_id())
            active_user.party_key_id = que
            return add_response(response = "Joined the active party")
      else:
            return add_response(response = "Unable to join that Party")
  @endpoints.method()
  def add_seggestion(self,response)
APPLICATION = endpoints.api_server([PocketJukeAPI])
