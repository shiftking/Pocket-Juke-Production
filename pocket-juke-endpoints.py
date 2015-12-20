import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote



package = 'pocket-juke'


@endpoints.api(name ='pocket-juke',version='v1')

class pocket-juke-API(remote.Service):


    @endpoints.method(message_types.VoidMessage, Party,
                        path='/party/create/{name}',http_method='GET',
                        name='party.create-party')
    def create-party(self, unused_request): #not sure what unused_request is used for, I take its ment for if passing variable to the method

    ID_RESOURCE = endpoints.ResourceContainer(
      message_types.VoidMessage,       #message_types.VoidMessage is used for when there isnt any message being trasnmittied to the method, usfull for when pulling all of the parties
      id=messages.IntegerField(1, variant=messages.Variant.INT32))
