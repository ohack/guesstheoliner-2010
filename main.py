import cgi
import wsgiref.handlers

from google.appengine.ext import webapp

from views import Home, Audit, Picture, Guess

def main():
  application = webapp.WSGIApplication([('/', Guess),
                                        ('/audit', Audit),
                                        ('/picture', Picture),
                                        ('/guess', Guess)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()