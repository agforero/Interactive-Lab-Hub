import requests
from textwrap import dedent
from bs4 import BeautifulSoup
from collections import deque


def aggregate_nums(nums):
    actual = []
    for item in nums:
        for term in item.split():
            if term[-1] == "%":
                actual.append(int(term[:-1]))

            else:
                try:
                    actual.append(int(term))

                except ValueError:
                    continue

    if len(actual) == 0:
        return 0.0

    else:
        return round(sum(actual) / len(actual), 1)


def aggregate_classes(classes):
    d = {}
    for term in classes:
        if term not in d:
            d[term] = 1

        else:
            d[term] += 1

    mx = 0
    mx_term = None
    for key in d:
        if d[key] > mx:
            mx = d[key]
            mx_term = key

    return mx_term


class WeatherData:
    def __init__(self, date, past):
        self.date = date.strftime("%Y%m%d")

        if past:
            url = (
                "https://www.timeanddate.com/weather/usa/new-york/historic?hd="
                + self.date
            )
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            search = soup.find("table", {"id": "wt-his"})

            # Whitespace, Temp, Weather, Wind, Direction, Humidity, Barometer, Visibility
            children = search.findChildren("td")
            children_queue = deque([child.text for child in children])
            self.scraped_data = [[] for _ in range(8)]

            i = 0
            while children_queue:
                self.scraped_data[i].append(children_queue.popleft())
                i = (i + 1) % len(self.scraped_data)

            self.temp = aggregate_nums(self.scraped_data[1])
            self.forecast = aggregate_classes(self.scraped_data[2])
            self.wind = aggregate_nums(self.scraped_data[3])
            self.humidity = aggregate_nums(self.scraped_data[5])

            rained = False
            for forecast in self.forecast:
                if "rain" in forecast or "rain." in forecast:
                    rained = True

            self.chance_of_rain = 100.0 if rained else 0.0

            temps = []
            for entry in self.scraped_data[1]:
                for term in entry.split():
                    try:
                        temps.append(float(term))

                    except ValueError:
                        continue

            self.high = max(temps)
            self.low = min(temps)

        else:
            url = (
                "https://www.timeanddate.com/weather/usa/new-york/hourly?hd="
                + self.date
            )
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            search = soup.find("table", {"id": "wt-hbh"})

            # Whitespace, Temp, Weather, Feels Like, Wind, Direction, Humidity, Chance, Amount
            children = search.findChildren("td")
            children_queue = deque([child.text for child in children])
            self.scraped_data = [[] for _ in range(9)]

            i = 0
            while children_queue:
                self.scraped_data[i].append(children_queue.popleft())
                i = (i + 1) % len(self.scraped_data)

            self.temp = aggregate_nums(self.scraped_data[1])
            self.forecast = aggregate_classes(self.scraped_data[2])
            self.wind = aggregate_nums(self.scraped_data[4])
            self.humidity = aggregate_nums(self.scraped_data[6])
            self.chance_of_rain = aggregate_nums(self.scraped_data[7])

            temps = []
            for entry in self.scraped_data[1]:
                for term in entry.split():
                    try:
                        temps.append(float(term))

                    except ValueError:
                        continue

            self.high = max(temps)
            self.low = min(temps)

    def __str__(self):
        return dedent(
            f"""\
            The temperature averages at {self.temp} degrees fahrenheit.
            The high is {self.high} degrees.
            The low is {self.low} degrees.
            The forecast is {self.forecast}
            Wind travels at {self.wind} miles per hour on average.
            The humidity is an average of {self.humidity} percent.
            There is a {self.chance_of_rain} percent chance of rain.\
            """
        )
