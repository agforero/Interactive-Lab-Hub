from datetime import timedelta
from datetime import date
from weatherdata import WeatherData


def look(terms, ls):
    for i, term in enumerate(terms):
        if term in ls:
            return ls.index(term)

    return -1


def tts(text):
    print(text)


class Query:
    def __init__(self):
        self.w = None
        self.flag = False
        self.past = False
        self.today = date.today()
        self.selected_day = "today"

        self.weekdays = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6,
        }

        self.warm_clothing = [
            "sweater",
            "jacket",
            "coat",
            "hoodie",
            "cardigan",
            "overcoat",
        ]

        self.forecasts = [
            "sun",
            "sunny",
            "rainy",
            "raining",
            "rain",
            "showers",
            "showering",
            "pouring",
            "storming",
            "storms",
            "storm",
            "thunderstorm",
            "thunderstorming",
            "lightning",
            "thunder",
            "cloudy",
            "clouds",
            "overcast",
            "grey",
            "gray",
            "snowy",
            "snowing",
            "snow",
            "hail",
            "hailing",
            "windy",
            "gusty",
            "humid",
            "humidity",
        ]

    def process_query(self, query):
        # we're going to assume query is a list of strings (tokens)
        # they are talking about yesterday

        if "yesterday" in query:
            self.past = True
            self.today -= timedelta(days=1)
            self.selected_day = "yesterday"

        elif "tomorrow" in query:
            self.today += timedelta(days=1)
            self.selected_day = "tomorrow"

        # they're talking about last wednesday or something
        elif "last" in query:
            self.past = True
            try:
                idx = query.index("last")
                rel_weekday = query[idx + 1]
                self.selected_day = "last " + rel_weekday

                # subtract today's weekday from the date
                self.today -= timedelta(days=self.today.weekday())

                # subtract another 7 to go back to last week
                self.today -= timedelta(days=7)

                # add the relevant weekday
                self.today += timedelta(days=self.weekdays[rel_weekday])

            # if the weekday isn't recognized, flag
            except IndexError:
                self.output_error(IndexError)
                return

            except KeyError:
                self.output_error(KeyError)
                return

        # similar to above, only moving forward in time
        elif "next" in query:
            try:
                idx = query.index("next")
                rel_weekday = query[idx + 1]
                self.selected_day = "next " + rel_weekday

                if self.today.weekday() < self.weekdays[rel_weekday]:
                    tts("Cannot look that far ahead.")
                    self.output_error(KeyError)
                    return

                # subtract today's weekday from the date
                self.today -= timedelta(days=self.today.weekday())

                # add another 7 to go forward to next week
                self.today += timedelta(days=7)

                # add the relevant weekday
                self.today += timedelta(days=self.weekdays[rel_weekday])

            # if the weekday isn't recognized, flag
            except IndexError:
                self.output_error(IndexError)
                return

            except KeyError:
                self.output_error(KeyError)
                return

        # at this point, it would recognize a weekday without "next" or "last"
        elif look(list(self.weekdays.keys()), query) != -1:
            try:
                idx = look(list(self.weekdays.keys()), query)
                rel_weekday = query[idx]
                self.selected_day = "this " + rel_weekday

                start = self.today

                # subtract today's weekday from the date
                self.today -= timedelta(days=self.today.weekday())

                # add the relevant weekday
                self.today += timedelta(days=self.weekdays[rel_weekday])

                if self.today < start:
                    self.past = True

            # if the weekday isn't recognized, flag
            except IndexError:
                self.output_error(IndexError)
                return

            except KeyError:
                self.output_error(KeyError)
                return

        # now, we know the day; we then need to see what we're actually doing with it
        self.w = WeatherData(self.today, self.past)

        # they're asking if they'll need an umbrella
        if "umbrella" in query:
            self.output_umbrella()

        # they're asking if they'll need something warm to wear
        elif look(self.warm_clothing, query) != -1:
            self.output_warm_clothing()

        # they're asking if a certain forecast occured/will occur
        elif look(self.forecasts, query) != -1:
            self.output_forecast()

        # they're just asking the normal weather
        else:
            self.output_normal()

    def output_umbrella(self):
        if self.w.chance_of_rain == 0.0:
            tts(
                f"The weather for {self.selected_day} does not necessitate an umbrella."
            )

        else:
            tts(f"The weather for {self.selected_day} may require an umbrella.")

    def output_warm_clothing(self):
        if self.w.temp <= 58.0:
            tts(
                f"The weather for {self.selected_day} does not necessitate warm clothes."
            )

        else:
            tts(f"The weather for {self.selected_day} calls for warm clothes.")

    def output_forecast(self):
        if self.past:
            tts(f"The forecast for {self.selected_day} was {self.w.forecast}")

    def output_normal(self):
        if self.past:
            tts(f"The weather for {self.selected_day} was as follows:")

        else:
            tts(f"The weather for {self.selected_day} will be as follows:")

        tts(str(self.w))

    def output_error(self, e):
        if e == IndexError:
            tts("IndexError. unknown command.")
        elif e == KeyError:
            tts("KeyError. unknown command.")

        self.flag = False
