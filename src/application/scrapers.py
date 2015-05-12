from bs4 import BeautifulSoup
from urllib2 import urlopen
from pprint import pprint
from dateutil.parser import parse

from models import Show

def make_soup(url):
    """Downloads the contents of the url and soupifies it"""
    try:
        html = urlopen(url).read()
    except:
        html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")

def puncify(s):
    """Replaces unicode characters with the appropriate ASCII punctuation"""
    return s.replace(u'\xa0', u' ').replace(u'\u201c', '"').replace(u'\u201d', '"').replace(u'\u2019', "'").replace(u"&amp;", '&').replace(u'\u2026', '...')

class SmokeScraper:
    def __init__(self):
        self.venue_name = "Smoke Jazz & Supper Club"
        self.base_url = "http://www.smokejazz.com"
        self.default_minimum = 20
        self.default_cover = 0

    def scrape(self):
        for date, link in self.get_show_dates_and_links():
            yield self.get_show_details(date, link)

    def get_show_dates_and_links(self):
        calendar_url = "http://www.smokejazz.com/index.php/calendar/"
        soup = make_soup(calendar_url)
        cal_entries = soup.find_all("div", "cal_entries")
        for entry in cal_entries:
            contents = entry.contents
            date = parse(contents[0].string).date()
            for event in contents[1::2]:
                link = self.base_url + event.find('a')['href']
                yield (date, link)

    def get_show_details(self, date, show_url):
        soup = make_soup(show_url)
        title = puncify(soup.find("h2", "uppercase").string)
        # date = parse(soup.find("nobr").string).date()
        table_stuff = soup.find_all("table", "set-times")[1].find_all("td")
        times = [parse(t.string).time() for t in table_stuff[::2]]
        info = table_stuff[1::2]
        prices, price_descriptions = zip(*self.figure_out_prices(info, show_url))
        description = puncify(''.join(soup.find("div", "col-sm-12 col-md-5 col-lg-5 txt-drk").strings))
        return {
            'url': show_url,
            'title': title,
            'date': date,
            'times': times,
            'prices': prices,
            'price_descriptions': price_descriptions,
            'venue': self.venue_name,
            'description': description
        }

    def figure_out_prices(self, table_entries, show_url):
        prices = [] #(price (int), description)
        for t in table_entries:
            cover = self.default_cover
            minimum = self.default_minimum
            t = list(t.strings)
            cover_string = t[0]
            if '$' in cover_string:
                cover = int(cover_string.strip('$').split(' ')[0])
            else:
                cover = 0
            if len(t) > 1:
                food_string = t[1]
                if '$' in food_string:
                    minimum = int(food_string.strip('$').split(' ')[0])

            prices.append((cover+minimum, '${} cover, ${} food minimum'.format(cover, minimum)))
            
        return prices

class FreeTimeScraper:
    def __init__(self):
        self.base_url = "http://www.clubfreetime.com"
        self.venue_name = "Unkown (but you should be able to find it with some Googling)"

    def scrape(self):
        for show in self.get_jazz_shows():
            yield self.get_show_details(show)

    def get_jazz_shows(self):
        calendar_url = "http://www.clubfreetime.com/new-york-city-nyc/free-classical-music-jazz-blues-concerts"
        soup = make_soup(calendar_url)
        events = soup.find_all(True, {'class':['eventItem', 'eventItem deal', 'eventItem pick']})
        for event in events:
            type = event.find(itemprop="eventType")
            if type and type.string == 'Jazz':
                yield event

    def get_show_details(self, show):
        url = self.base_url + show.find("a")["href"]
        title = show.find(itemprop="summary").string
        datetime = list(show.find(itemprop='startDate').stripped_strings)
        date = parse(datetime[0]).date()
        times = [parse(datetime[1]).time()]
        price = 0
        price_description = []
        for info in show.find_all(True, {'class':['innertube']})[1].stripped_strings:
            if info in datetime:
                continue
            price_description.append(info)
        price_description = ' '.join(price_description)
        description = show.find(itemprop="description")
        if description:
            description = puncify(' '.join(description.stripped_strings))
        
        return {
            'url': url,
            'title': title,
            'date': date,
            'times': times,
            'prices': [price],
            'price_descriptions': [price_description],
            'venue': self.venue_name,
            'description': description
        }

def scrape_all(venue):
    for show in venue.scrape():
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


