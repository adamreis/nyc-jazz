from sendgrid import SendGridClient
from sendgrid import Mail
from markdown import markdown
from datetime import date
from dateutil.relativedelta import relativedelta

from secret_keys import SENDGRID_USER, SENDGRID_PASSWORD

from models import Show




def show_to_markdown(show):
    lines = []
    time_format = "%I:%M%p"

    lines.append("- ####[{} @ {}]({})".format(show.title, show.venue, show.url))
    if show.description:
        lines.append(show.description)
    for t, p, p_d in zip(show.times, show.prices, show.price_descriptions):
        time = t.strftime(time_format)
        lines.append("\t- **{}** ${} ({})".format(time, p, p_d))

    return lines

def week_interval():
    today = date.today()
    next_week = today + relativedelta(weeks=+1)
    return today, next_week

def shows_this_week():
    today, next_week = week_interval()
    qry = Show.query(Show.date > today, Show.date <= next_week)
    qry.order(Show.date, Show.earliest_time)
    return qry.fetch()

def all_shows_to_markdown(all_shows):
    time_format = "%A, %m/%d"
    lines = []
    last_date = None
    
    for show in all_shows:
        if show.date != last_date:
            lines.append("##{}".format(show.date.strftime(time_format)))
            last_date = show.date
        lines += show_to_markdown(show)

    return "\n".join(lines).encode('utf-8')

def test_emails():
    test_emails = ['adamhreis@gmail.com']

    all_shows = shows_this_week()
    text = all_shows_to_markdown(all_shows)
    html = markdown(text)

    today, next_week = week_interval()
    tomorrow = today + relativedelta(days=+1)
    date_format = "%m/%d"

    responses = []

    # make a secure connection to SendGrid
    sg = SendGridClient(SENDGRID_USER, SENDGRID_PASSWORD, secure=True)

    for email in test_emails:
        # make a message object
        message = Mail()
        message.set_subject('NYC Jazz Digest: {} to {}'.format(tomorrow.strftime(date_format), next_week.strftime(date_format)))
        message.set_html(html)
        message.set_text(text)
        message.set_from('NYC Jazz Digest <digest@jazzdigest.nyc>')

        # add a recipient
        message.add_to(email)

        # use the Web API to send your message
        responses.append(str(sg.send(message)))

    return '\n'.join(responses)