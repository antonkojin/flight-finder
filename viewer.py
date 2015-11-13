#!/usr/bin/env python3
# viewer.py

import logging
log = logging.getLogger(__name__)


class Viewer:
    def __init__(self, config):
        self.config = config
        from utils import ReadJson
        self.flights = ReadJson(self.config['db'])

    def _searchWeekendFlights(self):
        from weekend_search import WeekendSearch
        from utils import SortFlightsByPrice
        weekendFlights = SortFlightsByPrice(WeekendSearch(self.flights))
        return weekendFlights

    def printWeekendFlightsByPrice(self):
        weekendFlights = self._searchWeekendFlights()
        weekday = {5:'V', 6:'S', 7:'D'}
        s = []
        print('{:10}  {}  {:5}  {:>6}    {:10}  {}  {:5}  {:>6}  {:>6}'.format(
                'on', 'w', 'time', 'price', 'back', 'w', 'time', 'price', 'total'
                ))
        f = '{:10}  {}  {:5}  {:>6,.2f}    {:10}  {}  {:5}  {:>6,.2f}  {:>6,.2f}'
        for flight in weekendFlights:
            print(f.format(
                str(flight['on']),
                weekday[flight['on'].isoweekday()],
                str(flight['onTime'])[:-3],
                flight['onPrice'],
                str(flight['back']),
                weekday[flight['back'].isoweekday()],
                str(flight['backTime'])[:-3],
                flight['backPrice'],
                flight['totalPrice']
            ))

    def printHistogram(self):
        pass

    def printDateHistogram(self):
        pass
