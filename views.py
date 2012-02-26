import os
import logging
import random

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from google.appengine.runtime.apiproxy_errors import OverQuotaError


from models import Person


class Home(webapp.RequestHandler):
    def get(self):
      people_query = Person.all()
      people = people_query #.fetch(10)

      template_values = {
        "people": people,
      }

      path = os.path.join(os.path.dirname(__file__), "index.html")
      self.response.out.write(template.render(path, template_values))

class Picture(webapp.RequestHandler):
  def get(self):
    template_values = {
      "imageurl": "/images/%s" % self.request.get('person')
    }
    path = os.path.join(os.path.dirname(__file__), "person_pic.html")
    self.response.out.write(template.render(path, template_values))

class Audit(webapp.RequestHandler):
  def get(self):
    people = Person.all()
    people = [p for p in people if not os.path.exists(os.path.join(os.path.dirname(__file__), "images", p.imageurl))]
    
    template_values = {
      "people": people,
    }

    path = os.path.join(os.path.dirname(__file__), "index.html")
    self.response.out.write(template.render(path, template_values))
    
class Guess(webapp.RequestHandler):
    def stringIfOn(self, test, string):
      if test == "on":
        return string
      else:
        return False

    def get(self):
      try:
        if not any([self.request.get("students2009"), self.request.get("students2010"), 
                    self.request.get("students2011"), self.request.get("students2012"),
                    self.request.get("students2013")]):
          checked_groups = {
            "students2009": "checked",
            "students2010": "checked",
            "students2011": "checked",
            "students2012": "checked",
            "students2013": "checked",
            }
        else:
          checked_groups = {
            "students2009": self.stringIfOn(self.request.get("students2009"), "checked"),
            "students2010": self.stringIfOn(self.request.get("students2010"), "checked"),
            "students2011": self.stringIfOn(self.request.get("students2011"), "checked"),
            "students2012": self.stringIfOn(self.request.get("students2012"), "checked"),
            "students2013": self.stringIfOn(self.request.get("students2013"), "checked"),
          }
          
        acceptable_groups = []
        if checked_groups["students2009"]:
          acceptable_groups.append("2009")
        if checked_groups["students2010"]:
          acceptable_groups.append("2010")
        if checked_groups["students2011"]:
          acceptable_groups.append("2011")
        if checked_groups["students2012"]:
          acceptable_groups.append("2012")
        if checked_groups["students2013"]:
          acceptable_groups.append("2013")
          
        template_values = {}
        template_values['checked_groups'] = checked_groups
        template_values['guessed'] = False
        
        # Process (if there was) an old guess
        if self.request.get('guess_key'):
          template_values['guessed'] = True
          template_values['old_guessed_person'] = db.get(self.request.get('guess_key'))
          template_values['old_correct_person'] = db.get(self.request.get('correct_key'))
          if self.request.get('correct_key') == self.request.get('guess_key'):
            template_values['correct_guess'] = True
          else:
            template_values['correct_guess'] = False
      
        # Set up the new guess
        people = []
        people_query = Person.all().fetch(500)  # I think "fetch" will get us a list of Objects, instead of an iterable, reducing DB calls a lott.
        filtered_people = [p for p in people_query if p.group in acceptable_groups]  # filter by group
        new_person = filtered_people[random.randint(0, len(filtered_people)-1)]
        filtered_people = [p for p in filtered_people if p.gender == new_person.gender]  # filter by gender
        query_length = len(filtered_people)
        for n in xrange(4):
          # This loop keeps picking until we get a non-duplicate person with image.
          # FIXME(gregmarra): The os.path.exists fails on the server.
          while not all([new_person.name != a.name for a in people]): # or not os.path.exists(os.path.join(os.path.dirname(__file__), "images", new_person.imageurl)):
            logging.info("trying new person for person number %s. %s rejected. os.path.exists('%s'): %s" % 
                         (len(people), 
                          new_person.name, 
                          os.path.join(os.path.dirname(__file__), "images", new_person.imageurl), 
                          os.path.exists(os.path.join(os.path.dirname(__file__), "images", new_person.imageurl))))
            new_person = filtered_people[random.randint(0, query_length-1)]
          people.append(new_person)

        template_values['choice_people'] = people
        template_values['correct_person'] = people[random.randint(0, len(people)-1)]

        path = os.path.join(os.path.dirname(__file__), "guess.html")
        self.response.out.write(template.render(path, template_values))
      except OverQuotaError:
        path = os.path.join(os.path.dirname(__file__), "failwhale.html")
        self.response.out.write(template.render(path, template_values))