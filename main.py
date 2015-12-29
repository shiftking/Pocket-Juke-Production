import os
import urllib
import operator
from google.appengine.api import namespace_manager
from operator import itemgetter
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2
import jinja2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
class Party(ndb.Model):
    """Somthoing"""


#NDB data type user
class User(ndb.Model):
    """Sub Model representing the user"""

    user_id = ndb.StringProperty(indexed=True)
    party_key = ndb.KeyProperty(Party,indexed=True)


#NDB data type party
class Party(ndb.Model):
    """main model to represent a party"""
    party_creator = ndb.KeyProperty(User,indexed=True)
    party_name = ndb.StringProperty(indexed=True)
    code = ndb.StringProperty(indexed=False)
    attending = ndb.IntegerProperty()

#NDB datatype for a song
class Song(ndb.Model):
    song_name = ndb.StringProperty()
    track_id = ndb.StringProperty(indexed=True)
    user_suggest = ndb.KeyProperty(indexed=True)
    party_key_id = ndb.KeyProperty(Party,indexed=True)


#NDB datatype for an activity
class Activity(ndb.Model):
    song = ndb.KeyProperty(Song,indexed=True)
    user_vote = ndb.KeyProperty(User,indexed=True)
    time_stamp = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        # Checks for active Google account session
        user = users.get_current_user()

        if user:
            user_logged = User.query(User.user_id == user.user_id())
            if not user_logged.get():
                new_user = User(user_id=user.user_id(),party_key = None)
                new_user.put()
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

            template = JINJA_ENVIRONMENT.get_template('html_templates/index.html')

            namespace = namespace_manager.get_namespace()
            template_values = {

            'url': url,
            'url_linktext': url_linktext,
            'namespace': namespace,
            }
            self.response.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))



class Start(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

            template = JINJA_ENVIRONMENT.get_template('html_templates/add party.html')

            namespace = namespace_manager.get_namespace()
            template_values = {

            'url': url,
            'url_linktext': url_linktext,
            'namespace': namespace,
            }
            self.response.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))


class Join(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()


        if user:
            #res = Party.query()

            template = JINJA_ENVIRONMENT.get_template('html_templates/join.html')
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            #self.response.out.write(res)
            template_values = {

                'url': url,
                'url_linktext': url_linktext,

            }
            self.response.write(template.render(template_values))
        else:
            url = users.create_login_url(self.request.uri)

            url_linktext = 'Login'
            template = JINJA_ENVIRONMENT.get_template('html_templates/login.html')
            template_values = {

                'url': url,
                'url_linktext': url_linktext,

            }
            self.response.write(template.render(template_values))

    def post(self):
        user = users.get_current_user()

        if user:
            template = JINJA_ENVIRONMENT.get_template('html_templates/join.html')
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            #self.response.out.write(res)
            template_values = {

                'url': url,
                'url_linktext': url_linktext,

            }
            self.response.write(template.render(template_values))
        else:
            url = users.create_login_url(self.request.uri)

            url_linktext = 'Login'
            template = JINJA_ENVIRONMENT.get_template('html_templates/login.html')
            template_values = {

                'url': url,
                'url_linktext': url_linktext,

            }
            self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
        ('/', MainPage),
        ('/start',Start),
        ('/join',Join),

], debug=True)
