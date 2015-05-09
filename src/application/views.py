"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, render_template, flash, url_for, redirect

from flask_cache import Cache

from application import app
from decorators import login_required, admin_required
from forms import SignupForm
from models import ExampleModel, Show

from scrapers.smoke import SmokeScraper
from scrapers.freetime import FreeTimeScraper


# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)


def home():
    return render_template('index.html')


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

def signup():
    import pdb; pdb.set_trace()
    form = SignupForm(request.form)
    if form.validate():
        email = form.email.data
    return 'woo'

def scrape_everything():
    counter = 0
    scrapers = [SmokeScraper(), FreeTimeScraper()]
    for scraper in scrapers:
        for show in scraper.scrape():
            if Show.query(Show.url == show.get('url'), Show.date == show.get('date')).fetch():
                # import pdb; pdb.set_trace()
                continue
            new_show = Show(
                venue = show.get('venue'),
                title = show.get('title'),
                description = show.get('description'),
                date = show.get('date'),
                times = show.get('times'),
                prices = show.get('prices'),
                price_descriptions = show.get('price_descriptions'),
                url = show.get('url')
            )
            new_show.put()
            counter += 1
    return 'ayooo {}'.format(counter)

