from helpers import make_soup, puncify
from pprint import pprint
from dateutil.parser import parse

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

if __name__ == "__main__":
    smoke = SmokeScraper()
    for thing in smoke.scrape():
        pprint(thing)