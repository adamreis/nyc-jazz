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
from models import User

import scrapers
import threading

# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)


def home():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        new_user = User(email=email)
        new_user.put()
        flash("You've signed up for weekly updates!")
        return redirect(url_for("home"))

    return render_template('index.html', form=form)


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

def signup():
    import pdb; pdb.set_trace()
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
    return 'woo'

def scrape_everything():
    return redirect(url_for('scrape_smoke'))

def scrape_smoke():
    scrapers.scrape_all(scrapers.SmokeScraper())
    return redirect(url_for('scrape_freetime'))

def scrape_freetime():
    scrapers.scrape_all(scrapers.FreeTimeScraper())
    return "you're scraped!"



