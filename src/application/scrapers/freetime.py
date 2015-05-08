from helpers import make_soup, puncify
from pprint import pprint
from dateutil.parser import parse

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

if __name__ == "__main__":
    count = 0
    freetime = FreeTimeScraper()
    for thing in freetime.scrape():
        pprint(thing)
        count += 1
    print(count)