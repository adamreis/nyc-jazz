"""
urls.py

URL dispatch route mappings and error handlers

"""
from flask import render_template

from application import app
from application import views


## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'warmup', view_func=views.warmup)

# Home page
app.add_url_rule('/', 'home', view_func=views.home, methods=['GET', 'POST'])

# Download all the shit
app.add_url_rule('/scrape', view_func=views.scrape_everything, methods=['GET', 'POST'])
app.add_url_rule('/scrape-smoke', view_func=views.scrape_smoke, methods=['GET', 'POST'])
app.add_url_rule('/scrape-freetime', view_func=views.scrape_freetime, methods=['GET', 'POST'])

# Email all the shit
app.add_url_rule('/email-test', view_func=views.email_test, methods=['GET'])
app.add_url_rule('/digest-send', view_func=views.digest_send, methods=['GET'])

# Unsubscribe user
app.add_url_rule('/unsubscribe/<identifier>', view_func=views.unsubscribe, methods=['GET'])

## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

