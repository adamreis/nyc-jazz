"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb


class ExampleModel(ndb.Model):
    """Example Model"""
    example_name = ndb.StringProperty(required=True)
    example_description = ndb.TextProperty(required=True)
    added_by = ndb.UserProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

class Show(ndb.Model):
    """A jazz show!"""
    venue = ndb.StringProperty()
    title = ndb.StringProperty()
    description = ndb.TextProperty()
    date = ndb.DateProperty()
    times = ndb.TimeProperty(repeated=True)
    prices = ndb.IntegerProperty(repeated=True)
    price_descriptions = ndb.StringProperty(repeated=True)
    url = ndb.StringProperty()

class User(ndb.Model):
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    email = ndb.StringProperty(required=True)
    opt_out = ndb.BooleanProperty(default=False)
    uuid = ndb.StringProperty(required=True)