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
import cgi
import urllib
import os
import jinja2


from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import security

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)




def username_key(username):
    return ndb.Key('User',username)

class User(ndb.Model):
    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()

    @classmethod
    def create_user(cls,candidate):
        entity = User.get_by_id(id = candidate)

        if entity is None:
            user = User()
            user.key  = username_key(candidate)
            user.put()

        else:
            return None

        return user
    # def get_user_by_ID(self,id):
    #     return User.
    def has_item(self,item):
       return Item.query(Item.name == item, ancestor = self.key)
    def add_item(self,item):
        return create_item(self,item)
    def all_items(self):
        return Item.query(ancestor = self.key).fetch()

def create_item(user,it):
    query = Item.query(Item.name == it, ancestor = user.key)
    if query.count():
        return None
    else:
        item = Item(parent = user.key)
        item.name = it
        item.put()
        return item

class Item(ndb.Model):
    name = ndb.StringProperty()

class Session(ndb.Model):
    session = ndb.KeyProperty()

    def deleteSession(self):
        self.delete()



def getStr(self):
    return  security.generate_random_string(length = 24)



class MainHandler(webapp2.RequestHandler):
    html=""""""

    def get(self):
        #self.html.format(var = )
        self.response.write(self.html)
        var = User.query().fetch(keys_only = True)
        c = self.request.cookies.get('name',None)
        user_id = self.request.get('user',None)
        #return self.response.write(self.request.get)
        if c :
            self.response.delete_cookie(c)
        #return self.response.write(self.request.get)
        if user_id :
            #return self.response.write(self.request.get)
            user_entry = User.get_by_id(user_id)
            self.response.set_cookie('name', user_id, path='/')

        template_values = { 'users': []}
        for i in var:
            template_values['users'] += [{'id':i.id() , 'entry':i.get(), 'items':i.get().all_items()}]
            #print template_values['users']
            #self.response.write(template_values['users'])
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


# class User(webapp2.RequestHandler):
#
#     def get(self):
#         var = User.query().fetch(keys_only = True)
#         template = JINJA_ENVIRONMENT.get_template('users.html')
#
#         template_values = {}
#
#         for i in var:
#             template_values.update({'id':i.id() , 'entry':i.get()})
#         #template = JINJA_ENVIRONMENT.get_template('index.html')
#         self.response.write(template.render(template_values))




class ItemRoute(webapp2.RequestHandler):


    def get (self):
        #var = User.query().fetch(keys_only = True)
        template_values = {}
        # for i in var:
        #     template_values.update({'id':i.id() , 'entry':i.get()})
        c = self.request.cookies.get('name','User')
        template = JINJA_ENVIRONMENT.get_template('item.html')

        self.response.write(template.render({'user':c}))



    def post(self):

        item = self.request.get("item")
        template = JINJA_ENVIRONMENT.get_template('item.html')

        template_values = {}
        user = self.request.cookies.get('name',None)

        if user is None:
            return self.response.write(template.render({'error':'Error choose a user on the main page'}))

        user  = User.get_by_id(user)
        if create_item(user, item):
            template_values = {'success': "Success, {item} created for {user}".format(user = user , item = item)}
        else:
            template_values ={'error': "Failed {item} not created for {user}. Already Exists".format(item = item, user = user) }

        self.response.write(template.render(template_values))




class userRoute(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('users.html')
        print "WOWe"
        return self.response.write(template.render())

    def post(self):

        info = self.validate(self.request.get("uname"), self.request.get("fname"),self.request.get("lname"))

        if info:
            self.redirect("/")
        else:
            template_values = {}
            template_values.update({'error': 'Failed'})
            template = JINJA_ENVIRONMENT.get_template('users.html')
            self.response.write(template.render(template_values))

    def validate(self, *dict):
        for str in dict:
            if not str:
                return None

        user = User.create_user(dict[0])
        if user:
            user.firstName = dict[1]
            user.lastName = dict[2]
            user.put()
            return user
        else:
            return None
		
		
		

app = webapp2.WSGIApplication([('/', MainHandler),('/users', userRoute), ('/items', ItemRoute) , ], debug=True)
