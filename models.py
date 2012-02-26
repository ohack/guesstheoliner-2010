from google.appengine.ext import db

class Person(db.Model):
  name = db.StringProperty()
  gender = db.StringProperty() # eg "m" or "f". We try to select people of same gender.
  imageurl = db.StringProperty()  # generally try to populate from name.
  group = db.StringProperty()  # eg "staff", "faculty", "student-2010"