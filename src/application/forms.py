"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

from flaskext import wtf
from flaskext.wtf import validators
from wtforms.ext.appengine.ndb import model_form

from .models import ExampleModel


class SignupForm(wtf.Form):
    email = wtf.TextField('Email Address', [validators.Length(min=6, max=35)])
    submit = wtf.SubmitField("Sign In")