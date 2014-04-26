import os
import webapp2
import jinja2
import cgi

import main

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):

  def get(self):
    template = JINJA_ENVIRONMENT.get_template('home.html')
    template_values = {} 
    self.response.write(template.render(template_values))

class SecondPage(webapp2.RequestHandler):

  def post(self):
    self.response.write('<!doctype html><html><body>Running simulation.<pre>')
    num_trials = int(cgi.escape(self.request.get('numTrials')))
    
    price, volatility, option_data = main.run(num_trials)
    template = JINJA_ENVIRONMENT.get_template('results.html')
    template_values = {
      'option_data': option_data,
      'price': price,
      'volatility': volatility}
    self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
	('/', MainPage),
  ('/run', SecondPage),
], debug = True)
