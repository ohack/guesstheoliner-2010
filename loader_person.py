import logging

from google.appengine.ext import bulkload
from google.appengine.api import datastore_types
from google.appengine.ext import search

from models import Person

class PersonLoader(bulkload.Loader):
  def __init__(self):
    bulkload.Loader.__init__(self, 'Person',
                             [('name', str),
                              ('gender', str),
                              ('imageurl', str),
                              ('group', str),
                              ])

  def HandleEntity(self, entity):
    ent = search.SearchableEntity(entity)
    return ent

if __name__ == '__main__':
  bulkload.main(PersonLoader())