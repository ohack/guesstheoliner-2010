# This replaces old loaders as of 8/25/09. Google changed stuff.
# see: http://code.google.com/appengine/docs/python/tools/uploadingdata.html

from google.appengine.ext import db
from google.appengine.tools import bulkloader

#DIRTY HACK BY GREG
class Person(db.Model):
  name = db.StringProperty()
  gender = db.StringProperty() # eg "m" or "f". We try to select people of same gender.
  imageurl = db.StringProperty()  # generally try to populate from name.
  group = db.StringProperty()  # eg "staff", "faculty", "student-2010"

class PersonLoader(bulkloader.Loader):
  def __init__(self):
    bulkloader.Loader.__init__(self, 'Person',
                               [('name', str),
                                ('gender', str),
                                ('imageurl', str),
                                ('group', str)
                               ])

loaders = [PersonLoader]